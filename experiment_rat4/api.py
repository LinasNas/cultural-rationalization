from flask import Blueprint, request, session, request
from random import choice, shuffle, randint

import datetime
import random
import numpy as np

from .db import *
from .helpers import current, current_board, api_error, weighted_sample_without_replacement, softmax

# Configure application
api = Blueprint("api", __name__)  

# PLAYER FUNCTIONS
@api.route("/player")
def current_player():
    """Get current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    return {"player": player.to_dict()}

@api.route("/player/tabswitch", methods=["POST"])
def tab_switch():
    """Increment tab switch count for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    player.tab_switch_count += 1
    player.save()

    return {"success": True}

@api.route("/player/create")
def create_player():
    """Create new player and assign to current session"""
    player = current()
    if player:
        return {"player": player.to_dict()}

    # choose a color combination for player
    #combination = random.choice(ColorCombination.select())
    #CHANGE FOR EACH MICROCULTURE 0-11
    combination = ColorCombination.get(ColorCombination.id == 0)
    player = Player.create(color_combination=combination)
    session["user"] = player.id
    return {"player": player.to_dict()}


@api.route("/player/update", methods=["POST"])
def update_player():
    """Update current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)
    
    to_update = ["total_score", "total_time"]
    for t in to_update:
        if request.form.get(t) is not None:
            setattr(player, t, request.form.get(t))

    player.save()
    return {"player": player.to_dict()}


@api.route("/<int:generation_ID>/player/consent")
def consent_player(generation_ID):
    """Update consent to current timestamp"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    # NEW
    # Extract the generation_ID from the URL
    print("======== CONSENT FORM ==========")
    print("request.path", request.path)
    generation_ID = request.path.strip('/').split('/')[1]
    generation_ID = int(generation_ID)
    print("GENERATION_ID", generation_ID)

    worker_id = request.args.get('workerId')

    #save consent time
    player.consent = datetime.datetime.now()
    player.worker_id = worker_id
    print(worker_id)

    # SAVE GENERATION
    player.Generation = generation_ID

    # =====================BEGIN=======================
    # NEW FOR MULTIPLE Microcultures

    # I. ESSENTIAL: SPECIFY THREE KEY PARAMS:
    NUM_MICROCULTURES = 1
    PLAYERS_PER_MICROCULTURE = 40     #players per gen per microculture
    INACTIVITY_LIMIT = datetime.timedelta(minutes=100000) # 15 minutes inactivity considered

    # II. find the microculture to assign the player to 
    # 1. get all players from the current generation
    current_players = Player.select().where(Player.id != player.id, Player.Generation == generation_ID)

    print("current_players", current_players)
    print("len(current_players)", len(current_players))

    # Current time, assumed to be datetime.datetime.now()
    current_time = datetime.datetime.now()

    # Start a dict to keep track of the number of reservations for each microculture
    # Initialize counts for provisional and confirmed players
    provisional_counts = {i: 0 for i in range(NUM_MICROCULTURES + 1)}  # Include '0' as a possible key
    confirmed_counts = {i: 0 for i in range(1, NUM_MICROCULTURES + 1)}

    # Adjust the counting logic to account for inactivity
    for p in current_players:
        if p.Finished:
            if p.keep == 1:
                confirmed_counts[p.Microculture] += 1
            # no other condition: will ignore those who finished, but keep==0

        # if not finished, but exceeded inactivity limit (inactive player):
        # delete the reservation
        elif p.consent is None or (current_time - p.consent) > INACTIVITY_LIMIT:
            p.Reserved_microculture = 0
            print(f"Reservation reset due to inactivity for player ID: {p.id}")
            p.save()

        else:
            # If not finished and within inactivity limit (active player)
            # count in the provisional counts (i.e. reserved the microculture, but haven't finished the experiment)
            # this way, count only active reservations
            if p.Reserved_microculture not in provisional_counts:
                provisional_counts[p.Reserved_microculture] = 0
            provisional_counts[p.Reserved_microculture] += 1 if p.Reserved_microculture != 0 else 0

    print("provisional_counts", provisional_counts)
    print("confirmed_counts", confirmed_counts)

    # Combine confirmed and provisional counts for stricter control
    total_counts = {mc: provisional_counts[mc] + confirmed_counts.get(mc, 0) for mc in range(1, NUM_MICROCULTURES + 1)}
    print("total_counts", total_counts)

    # Find microcultures that are still under the limit when combining both provisional and confirmed
    available_microcultures = [mc for mc in total_counts if total_counts[mc] < PLAYERS_PER_MICROCULTURE]
    if available_microcultures:
        # assign to the microculture with the fewest players or reservations
        min_total = min(total_counts[mc] for mc in available_microcultures)
        microculture = min((mc for mc in available_microcultures if total_counts[mc] == min_total), default=None)
    else:
        microculture = 1  # Or handle more dynamically

    # III. Assign microculture and handle the rest of the logic
    player.Microculture = microculture
    player.Reserved_microculture = microculture

    player.save()
    print("SAVED: player.Generation", player.Generation)
    print("SAVED: player.Microculture", player.Microculture)
    print("===== END CONSENT ======")
    return {"success": True}

@api.route("/player/delete")
def delete_player():
    """Delete instance of current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)
    player.delete_instance()

    return True


@api.route("/player/moves")
def current_player_moves():
    """Get moves of current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    return {"moves": [move.to_dict() for move in player.get_moves()]}


# @api.route("/player/tutorial")
# def current_player_tutorial():
@api.route("/<int:generation_ID>/player/tutorial")
def current_player_tutorial(generation_ID):
    """Get previous players' moves to show to current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    #NEW
    # Extract the generation_ID from the URL
    print("==========PLAYER TUTORIAL===========")
    # print("request.path", request.path)
    generation_ID = request.path.strip('/').split('/')[1]
    generation_ID = int(generation_ID)
    print("GENERATION_ID", generation_ID)
    #SAVE GENERATION ID HERE
    player.Generation = generation_ID
    # player.save()
    # print("SAVED: player.Generation", player.Generation)
        
    #HERE: if gen_ID is 0: no tutorials
    #NEW
    prev_gen_ID = generation_ID - 1
    print("prev_gen_ID", prev_gen_ID)
    if prev_gen_ID < 0:
        is_gen_0 = True
    else:
        is_gen_0 = False

    # check if previously assigned players
    pc_assigned = PlayersShown.select().where(PlayersShown.shown_to == player.id)

    #if not, assign players for tutorial
    if pc_assigned:
        pc_assigned = [p.shown_id for p in pc_assigned]
        players_chosen = Player.select().where(Player.id.in_(pc_assigned))
        players_chosen = [p for p in players_chosen]
        print("players chosen", players_chosen)

    else:
        #NEW: V2: LINAS: Add microcultures
        previous_players = Player.select().where(Player.id != player.id, Player.keep == 1, Player.Generation == prev_gen_ID, Player.Microculture == player.Microculture)
        print("filtering previous players by microculture:", player.Microculture)
        print("previous_players", previous_players)
        print("len(previous_players)", len(previous_players))
        print("type(previous_players)", type(previous_players))

        manual_tutorial = 0
        GENERATION_SIZE = 6
        max_tuts = 3
        players_chosen = []

        # get all previous players
        players, weights = [], []
        for p in previous_players:
            players.append(p)
            weights.append(p.total_score)

        # there are enough previous players to return one from each generation to show
        #if len(players) >= GENERATION_SIZE*1000:
        #
        #if len(players) >= GENERATION_SIZE:
        #NEW
        if (len(players) >= GENERATION_SIZE) & (is_gen_0 == False):

            #this will sort out all people from previous generation only
            players = sorted(players, key=lambda x: x.created)

            print("players", players)
            print('len(players)', len(players))

            gen = players
            print("gen", gen)
            print('len(gen)', len(gen))

            gen_sorted = sorted(gen, key=lambda p: p.total_score, reverse=True)
            top_six = gen_sorted[:6]

            gen_players = random.sample(top_six, k=min(3, len(top_six)))

            for gen_player in gen_players:
                players_chosen.append(gen_player)
        elif manual_tutorial == 1:
            specific_players = []
            players_chosen = Player.select().where(Player.id.in_(specific_players))
            players_chosen = [p for p in players_chosen]

        else:
            print(f"not enough players for tutorials, have {len(players)} but need {max_tuts}")
            #NEW
            print("OR this is gen 0")
 
        # save chosen players to database
        for pc in players_chosen:
            x = PlayersShown(shown=pc.id, shown_to=player.id)
            x.save()

    responses = [p.PipedText for p in players_chosen]
    return {
        "tutorial": [
            {
                "player": p.to_dict(),
                "moves": [move.to_dict() for move in p.get_moves("asc")],
                "board": p.get_board().to_dict(),
                "rules": p.PipedText,  # <-- this is the text response
            }
            for p in players_chosen
        ],
        "colors": player.color_combination.colors(),
    }
# MOVE FUNCTIONS
@api.route("/move/create", methods=["POST"])
def create_move():
    """Create move for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["move_x", "move_y", "total_score"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for move {key}", status=400)

    # validate values
    x, y = [int(request.form.get(f"move_{i}")) for i in ["x", "y"]]
    if (x, y) not in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        return api_error(f"Invalid move: ({(x, y)})", status=400)

    # check max number of moves
    if Move.select().where(Move.player == player).count() >= player.number_of_moves:
        return api_error("Max number of moves reached", status=400)

    move = Move.create(player=player, **{key: request.form.get(key) for key in keys})
    move.save()

    return {"move": move.to_dict()}

@api.route("/move/end", methods=["POST"])
def end_game():
    """End the game for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["total_score", "total_time"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for move {key}", status=400)

    player.total_score = int(request.form.get("total_score"))
    player.total_time = int(request.form.get("total_time"))

    player.save()

    # print("================")
    # print("PLAYER ID", player.id)
    # print("================")
    # update_keep_column(player)
    
    print(f"direction_time for player {player.id}: {player.direction_time}")



    return {"player": player.to_dict()}

#OLD
@api.route("/board/create")
def create_board():
#NEW
# @api.route("/<int:generation_ID>/board/create")
# def create_board(generation_ID):
    """Create board for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    #NEW
    # Extract the generation_ID from the URL
    # print("SET")
    # print("request.path", request.path)
    # generation_ID = request.path.strip('/').split('/')[1]
    # generation_ID = int(generation_ID)
    # print("GENERATION_ID", generation_ID)

    board = current_board()
    if board:
        return {"board": board.to_dict()}

    # choose a color combination
    grey, pink, blue, yellow, green, brown, white = player.color_combination.colors()

    number_to_color = {0: grey, 1: pink, 2: blue, 3: yellow, 4: green, 5: brown, 6: white}
    color_to_idx = {c: i for i, c in enumerate([grey, pink, blue, yellow, green, brown, white])}

    # variable for toggling between manual and random board creation
    #LEAVE AT 1
    manual_creation = 1  # set to 1 for manual creation, 0 for random

    #THIS WAS MANUALLY SET
    #EVEN GENS: SET 1
    #ODD GENS: SET 2
    #Change so this line would be based on generation ID

    #OLD
    #board_set = 2 # set to 1 to choose from board set one, 2 for board set two
    #NEW
    generation_ID = player.Generation
    print("======== BOARD ==========")
    print("generation_ID", generation_ID)
    if generation_ID % 2 == 0:
        board_set = 1
    else:
        board_set = 2
    print("board_set", board_set)
    
    if manual_creation:
        # Board set one
        board_1 =[0, 0, 0, 0, 0, 0, 6,
            0, 1, 4, 0, 2, 3, 0,
            0, 4, 4, 0, 2, 2, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 3, 3, 0, 1, 1, 0,
            0, 2, 3, 0, 1, 4, 0,
            5, 0, 0, 0, 0, 0, 0]

        board_2 = [0, 0, 0, 0, 0, 0, 5,
            0, 4, 1, 0, 3, 2, 0,
            0, 1, 1, 0, 3, 3, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 2, 2, 0, 4, 4, 0,
            0, 3, 2, 0, 4, 1, 0,
            6, 0, 0, 0, 0, 0, 0]

        
        # Board set two
        board_3 = [5, 0, 0, 0, 0, 0, 0,
            0, 3, 2, 0, 4, 1, 0,
            0, 2, 2, 0, 4, 4, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 1, 1, 0, 3, 3, 0,
            0, 4, 1, 0, 3, 2, 0,
            0, 0, 0, 0, 0, 0, 6]

        board_4 = [6, 0, 0, 0, 0, 0, 0,
            0, 2, 3, 0, 1, 4, 0,
            0, 3, 3, 0, 1, 1, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 4, 4, 0, 2, 2, 0,
            0, 1, 4, 0, 2, 3, 0,
            0, 0, 0, 0, 0, 0, 5]


        if board_set == 1:
            chosen_board = random.choice([board_1, board_2])
            chosen_board_id = 1 if chosen_board == board_1 else 2
            print(f"Chosen board is {chosen_board_id}")
        else:
            chosen_board = random.choice([board_3, board_4])
            chosen_board_id = 3 if chosen_board == board_3 else 4
            print(f"Chosen board is {chosen_board_id}")

        board_colors = [number_to_color[num] for num in chosen_board]
        pos = 24  # manually set initial position

    else:
        # create random board
        board_colors = np.concatenate([np.tile([c], n) for c, n in [(grey, 33), (pink, 4), (blue, 4), (yellow, 4), (green, 4)]])
        np.random.shuffle(board_colors)
        # determine initial position
        pos = int(np.random.choice(np.where(board_colors == grey)[0]))

    image_paths = {
        1: '/static/graphics/m1.png',
        2: '/static/graphics/m2.png',
        3: '/static/graphics/m3.png',
        4: '/static/graphics/m4.png',
        5: '/static/graphics/pot.png',
        6: '/static/graphics/grinder.png'
    }
   
    # save board
    board = Board.create(player=player, inital_pos=pos, chosen_board_id=chosen_board_id)
    board.save()

    player.chosen_board_id = chosen_board_id
    player.save()

    # save board colors
    for i, c in enumerate(board_colors):
        board_slot = BoardSlot.create(board=board, slot=i, color=color_to_idx.get(c), image=image_paths.get(color_to_idx.get(c)))
        board_slot.save()

    return {"board": board.to_dict()}





# QUESTIONNAIRE FUNCTIONS
@api.route("/guess", methods=["POST"])
def save_guesses():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["rules"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.rules = request.form.get("rules")
    player.save()
    return {"player": player.to_dict()}


@api.route("/guess/2", methods=["POST"])
def save_color_guesses():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["optSQ0", "optSQ1", "optSQ2", "optSQ3"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.color_guess_0 = request.form.get("optSQ0")
    player.color_guess_1 = request.form.get("optSQ1")
    player.color_guess_2 = request.form.get("optSQ2")
    player.color_guess_3 = request.form.get("optSQ3")
    player.save()
    
    return {"player": player.to_dict()}

@api.route("/guess/21", methods=["POST"])
def save_process_guess():
    """Save process guess for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    key = "process"
    if not request.form.get(key):
        return api_error("Missing argument for process", status=400)

    player.process_guess = request.form.get(key)
    player.save()
    return {"player": player.to_dict()}

#NEW:LINAS
@api.route("/guess/22", methods=["POST"])
def save_grind_guesses():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["radio1"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.Ignorance_Knowledge = request.form.get("radio1")
    player.save()
    
    return {"player": player.to_dict()}

@api.route("/PipedTextGuess", methods=["POST"])
def save_PipedTextGuess():
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["PipedText"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.PipedText = request.form.get("PipedText")
    player.save()
    return {"player": player.to_dict()}


@api.route("/guess/1", methods=["POST"])
def save_valuesYN():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    # Define the expected keys
    expected_keys = ["valuesYN", "processYN"]
    
    # Check if all required keys are present in the request
    for key in expected_keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for {key}", status=400)

    # Update player object with received values
    player.valuesYN = request.form.get("valuesYN")
    player.processYN = request.form.get("processYN")
    
    # Save the player object
    player.save()
    
    return {"player": player.to_dict()}


@api.route("/guess/3", methods=["POST"])
def save_attention_check():
    """Save attention check value for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    key = "attention_check"
    if not request.form.get(key):
        return api_error(f"Missing argument {key}", status=400)

    player.attention_check = request.form.get(key)
    player.save()


    return {"player": player.to_dict()}



# New API route to set the timestamp for the Introduction0.html page
@api.route("/set_intro_timestamp", methods=["POST"])
def set_intro_timestamp():
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)
    
    # Store the current timestamp for introduction page
    player.intro_timestamp = datetime.datetime.now()
    print(f"Setting intro timestamp for player {player.id} at {player.intro_timestamp}")

    player.save()
    
    return {"success": True}

# New API route to set the timestamp for the play.html page and calculate direction_time
@api.route("/set_play_timestamp", methods=["POST"])
def set_play_timestamp():
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    # Store the current timestamp for play page and calculate direction_time
    play_timestamp = datetime.datetime.now()
    if player.consent:
        player.direction_time = int((play_timestamp - player. consent).total_seconds())
        print(f"Setting play timestamp for player {player.id}. Time difference: {player.direction_time} seconds")
    player.save()
    
    return {"success": True}

@api.route("/guess/23", methods=["POST"])
def guess_23():
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)
    
    key = "importance"
    if not request.form.get(key):
        return api_error("Missing argument for importance", status=400)

    player.Conformity_Importance = request.form.get(key)
    player.save()
    return {"player": player.to_dict()}

@api.route("/textContinuityImportance", methods=["POST"])
def textContinuityImportance():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["textContinuityImportance"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.textContinuityImportance = request.form.get("textContinuityImportance")
    player.save()
    return {"player": player.to_dict()}

@api.route("/endCheck", methods=["POST"])
def save_endCheck():
    """Save guesses for current player"""
    player = current()
    if not player:
        return api_error("Unauthorized", status=403)

    keys = ["points_choice", "name_choice", "players_choice", "feedback"]
    for key in keys:
        if not request.form.get(key):
            return api_error(f"Missing argument for guesses {key}", status=400)

    player.valueChoice = request.form.get("points_choice")
    player.nameChoice = request.form.get("name_choice")
    player.tutorialChoice = request.form.get("players_choice")
    player.endFreeText = request.form.get("feedback")
    player.save()
    return {"player": player.to_dict()}

