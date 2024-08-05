import datetime
from hashlib import blake2b
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = SqliteDatabase("game/cult_ev.db", pragmas={"foreign_keys": 1})
#db = SqliteDatabase("cult_ev.db", pragmas={"foreign_keys": 1})

class Base(Model):
    class Meta:
        database = db

class ColorCombination(Base):
    name = CharField(max_length=256, default=None)
    description = CharField(max_length=512, default=None)

    def colors(self):
        return [
            f"{c.color_code}" 
            for c in Color.select()
                .where(Color.color_combination == self)
                .order_by(Color.color_number.asc())
        ]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "colors": {
                c.color_number: f"{c.color_code}"
                for c in Color.select().where(Color.color_combination == self).order_by(Color.color_number.asc())
            }
        }

class Player(Base):
    tab_switch_count = IntegerField(default=0)
    keep = IntegerField(default=0)
    consent = DateTimeField(null=True)
    demographic_identifier = CharField(max_length=8, default=None)
    rules = TextField(default=None)
    created = DateTimeField(default=datetime.datetime.now)
    total_score = IntegerField(default=0)
    total_time = IntegerField(default=0) # in seconds
    number_of_moves = IntegerField(default=500) # total number of moves allowed
    color_combination = ForeignKeyField(ColorCombination, on_delete="CASCADE", on_update="CASCADE")
    direction_time = IntegerField(default=0)  # Time in seconds
    chosen_board_id = IntegerField(null=True)
    attention_check = CharField(max_length=256, default=None, null=True)
    worker_id = CharField(max_length=256, default=None, null=True)

    color_guess_0 = CharField(max_length=16, default=None)
    color_guess_1 = CharField(max_length=16, default=None)
    color_guess_2 = CharField(max_length=16, default=None)
    color_guess_3 = CharField(max_length=16, default=None)

    process_guess = CharField(max_length=16, default=None)
    #NEW:Linas
    grinding_guess_0 = CharField(max_length=16, default=None)
    grinding_guess_1 = CharField(max_length=16, default=None)
    grinding_guess_2 = CharField(max_length=16, default=None)
    grinding_guess_3 = CharField(max_length=16, default=None)

    #NEW: LINAS
    Microculture = IntegerField(default=0)
    Reserved_microculture = IntegerField(default=0)
    Finished = IntegerField(default=0)

    valuesYN = CharField(max_length=15, default=None)
    processYN = CharField(max_length=15, default=None)
    
    #NEW
    Generation = IntegerField(default=0)
    collected_items = TextField(default="[]")


    def to_dict(self):
        return {k: getattr(self, k) for k in ["id", "consent", "total_score", "total_time", "number_of_moves"]}

    def get_moves(self, order="desc"):
        order_by = Move.timestamp.desc() if order == "desc" else Move.timestamp.asc()
        return Move.select().where(Move.player_id == self).order_by(order_by)

    @property
    def identifier(self):
        if not self.demographic_identifier:
            id_ = blake2b(digest_size=4)
            id_.update(str(self.id).encode())
            self.demographic_identifier = id_.hexdigest()
            self.save()

        return self.demographic_identifier

    def get_board(self):
        return Board.select().where(Board.player == self).get_or_none()


class PlayersShown(Base):
    shown = ForeignKeyField(Player, on_delete="CASCADE", on_update="CASCADE")
    shown_to = ForeignKeyField(Player, on_delete="CASCADE", on_update="CASCADE")


class Move(Base):
    player = ForeignKeyField(Player, on_delete="CASCADE", on_update="CASCADE")
    timestamp = DateTimeField(default=datetime.datetime.now)
    move_x = IntegerField(default=0)
    move_y = IntegerField(default=0)
    total_score = IntegerField(default=0)

    def to_dict(self):
        return {k: getattr(self, k) for k in ["id", "timestamp", "move_x", "move_y", "total_score"]}


class Color(Base):
    color_combination = ForeignKeyField(ColorCombination, on_delete="CASCADE", on_update="CASCADE")
    color_number = IntegerField(default=0) # 0: pink, 1: blue, 2: brown
    color_code = CharField(max_length=6, default=None)

    def hex(self):
        return f"{self.color_code}"


class Board(Base):
    player = ForeignKeyField(Player, on_delete="CASCADE", on_update="CASCADE")
    inital_pos = IntegerField(default=0)

    def board(self, return_indices=False):
        colors = self.player.color_combination.colors()
        board_slots = BoardSlot.select().where(BoardSlot.board == self)

        if not return_indices:
                return [colors[b.color] for b in board_slots]


        return [b.color for b in board_slots]

    def previous_moves(self):
        return [
            {"x": move.move_x, "y": move.move_y} 
            for move in Move.select().where(Move.player == self.player).order_by(Move.timestamp.asc())
        ]

    def current_pos(self):
        # load moves
        current = self.inital_pos
        moves = Move.select().where(Move.player == self.player).order_by(Move.timestamp.asc())
        for move in moves:
            current += move.move_x + round(len(self.board()) ** 0.5) * move.move_y
        
        return current

    def moves_remaining(self):
        return self.player.number_of_moves - Move.select().where(Move.player == self.player).count()

    def current_score(self):
        last_move = Move.select().where(Move.player == self.player).order_by(Move.timestamp.desc()).get_or_none()
        if not last_move:
            return 0
        return last_move.total_score

    def to_dict(self):
        return {
            "id": self.id,
            "board": self.board(),
            "board_idx": self.board(True),
            "initial_pos": self.inital_pos,
            "current_pos": self.current_pos(),
            "previous_moves": self.previous_moves(),
            "current_score": self.current_score(),
            "moves_remaining": self.moves_remaining(),
            "colors": self.player.color_combination.to_dict(),
        }


class BoardSlot(Base):
    board = ForeignKeyField(Board, on_delete="CASCADE", on_update="CASCADE")
    slot = IntegerField(default=0)
    color = IntegerField(default=0)

# OLD
# def update_keep_column():
#     for player in Player.select():
#         print(f"Processing player with ID: {player.id}, total_time: {player.total_time}, tab_switch_count: {player.tab_switch_count}")
#         has_null_values = any(getattr(player, field.name) is None and field.name != 'worker_id' for field in Player._meta.fields.values())
#         if not has_null_values and player.total_time < 900 and player.tab_switch_count < 2 and player.direction_time > 25 and player.attention_check == "Ferngrove":
#             player.keep = 1
#             print(f"Setting keep to 1 for player with ID: {player.id}")
#         else:
#             player.keep = 0
#             print(f"Setting keep to 0 for player with ID: {player.id}")
#         player.save()

# NEW
#IMPORTANT: Please dont move this function to anwyhere else but the end of the experiment! 
#Otherwise, the Reserved_Microculture will be set to 0 before the player is finished
def update_keep_column(player):
    print(f"Processing player with ID: {player.id}, total_time: {player.total_time}, tab_switch_count: {player.tab_switch_count}")
    #and player.worker_id is not None
    if player.total_time <= 900 and player.total_time > 0 and player.tab_switch_count <= 1 and player.direction_time >= 25 and player.attention_check == "Ferngrove" and player.worker_id is not None:
        player.keep = 1
        print(f"Setting keep to 1 for player with ID: {player.id}")
    else:
        player.keep = 0
        #BUT: we dont set Microculture to 0, because 
        print(f"Setting keep to 0 for player with ID: {player.id}")

    #LINAS:
    #update_keep_column(player) is only called at the end
    #so we can set Reserved_Microculture to 0 here, because a player is finished
    player.Reserved_microculture = 0
    player.Finished = 1
    print(f"Setting Reserved_Microculture to 0 for player with ID: {player.id}")
    print(f"Setting Finished to 1 for player with ID: {player.id}")

    player.save()

Player.assigned_board = ForeignKeyField(Board, backref='player', null=True)

class CollectedItem(Base):
    player = ForeignKeyField(Player, backref='collected_items')
    color = CharField()
    collected_at = DateTimeField(default=datetime.datetime.now)

def store_collected_item(player_id, color):
    try:
        player = Player.get_by_id(player_id)
        CollectedItem.create(player=player, color=color)
        return True
    except Exception as e:
        print(f"Database operation failed: {e}")  # Debug log
        return False



# Drop tables if they exist
db.connect()
db.create_tables([Player, PlayersShown, Move, ColorCombination, Color, Board, BoardSlot, CollectedItem])
