#establishes routes for website
from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_session import Session
from .db import *
from .helpers import current

from .api import api

# Configure application
app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# @app.route("/")
# def index():
#     return render_template("index.html")
@app.route("/<int:generation>/")
def index(generation):
    template_name = f"index/index_{generation}.html"
    return render_template(template_name)

# @app.route("/consent")
# def consent():
#     player = current()
#     if player and player.consent:
#         return redirect("/play")

#     return render_template("consent.html")

@app.route("/<int:generation>/consent")
def consent(generation):
    player = current()
    if player and player.consent:
        return redirect("/play")
    
    template_name = f"consent/consent_{generation}.html"
    return render_template(template_name)


# @app.route("/Introduction0")
# def introduction0():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("Introduction0.html", player=player)


@app.route("/<int:generation>/Introduction0")
def introduction0(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"introduction0/Introduction0_{generation}.html"
    return render_template(template_name, player=player)


# @app.route("/Introduction1")
# def introduction1():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("Introduction1.html", player=player)

@app.route("/<int:generation>/Introduction1")
def introduction1(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"introduction1/Introduction1_{generation}.html"
    return render_template(template_name, player=player)


# @app.route("/Introduction2")
# def introduction2():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("Introduction2.html", player=player)

@app.route("/<int:generation>/Introduction2/")
def introduction2(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"introduction2/Introduction2_{generation}.html"
    return render_template(template_name, player=player)


# @app.route("/introduction")
# def introduction():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("introduction.html", player=player)
@app.route("/<int:generation>/introduction")
def introduction(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"introduction/introduction_{generation}.html"
    return render_template(template_name, player=player)


# @app.route("/play")
# def play():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")
#     return render_template("play.html")

# @app.route("/play")
@app.route("/<int:generation>/play")
def play(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")
    
    template_name = f"play/play_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/tutorials")
def tutorials(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")
    
    template_name = f"tutorials/tutorials{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/chooseTutorials")
def chooseTutorials(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")
    
    template_name = f"chooseTutorials/chooseTutorials{generation}.html"
    return render_template(template_name, player=player)

# @app.route("/rules")
# def rules():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules.html", player=player)
@app.route("/<int:generation>/rules")
def rules(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules/rules_{generation}.html"
    return render_template(template_name, player=player)

# @app.route("/rules1")
# def rules1():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules1.html", player=player)
@app.route("/<int:generation>/rules1")
def rules1(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules1/rules1_{generation}.html"
    return render_template(template_name, player=player)


# @app.route("/rules2")
# def rules2():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules2.html", player=player)
@app.route("/<int:generation>/rules2")
def rules2(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules2/rules2_{generation}.html"
    return render_template(template_name, player=player)


@app.route("/<int:generation>/rules21")
def rules21(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules21/rules21_{generation}.html"
    return render_template(template_name, player=player)




#NEW: Linas
@app.route("/<int:generation>/rules22")
def rules22(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules22/rules22_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/rules23")
def rules23(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules23/rules23_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/textContinuityImportance")
def textContinuityImportance(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"textContinuityImportance/textContinuityImportance_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/rules3")
def rules3(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules3/rules3_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/rules4")
def rules4(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules4/rules4_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/finish")
def finish(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    #NEW
    print("================Update keep column================")
    print("Current player : ", player.id)
    update_keep_column(player)
    print("================Update done================")

    template_name = f"finish/finish_{generation}.html"
    return render_template(template_name, player=player)

@app.route("/<int:generation>/terminate")
def terminate(generation):
    player = current()
    template_name = f"terminate/terminate_{generation}.html"
    return render_template(template_name, player=player)

@app.route('/api/collect-item', methods=['POST'])
def collect_item():
    try:
        item_data = request.get_json()
        itemType = item_data.get('itemType')
        print(f"Received itemType: {itemType}")  # Debug print

        player = current()
        print(f"Current player ID: {player.id}")  # Debug print if 'current' function correctly retrieves the player

        success = store_collected_item(player.id, itemType)
        print(f"Store operation success: {success}")  # Verify if true or false

        if success:
            return jsonify({"message": "Item stored successfully"}), 200
        else:
            return jsonify({"message": "Error storing item"}), 500
    except Exception as e:
        print(f"Error in collect_item: {e}")  # Log any exceptions
        return jsonify({"message": f"Server error: {e}"}), 500

@app.route('/api/collected-items/<int:player_id>')
def get_collected_items(player_id):
    try:
        # Retrieve items ordered by collection time
        collected_items = CollectedItem.select().where(CollectedItem.player_id == player_id).order_by(CollectedItem.collected_at)
        original_player = Player.get_or_none(Player.id == player_id)
        current_player = current()

        if not original_player or not current_player:
            return jsonify({"error": "Player not found"}), 404

        original_player_colors = original_player.color_combination.to_dict()["colors"]
        current_player_colors = current_player.color_combination.to_dict()["colors"]

        items = []
        for item in collected_items:
            original_color_id = next((color_id for color_id, color in original_player_colors.items() if color == item.color), None)
            if original_color_id is None:
                continue

            mapped_color = current_player_colors.get(original_color_id)
            if mapped_color:
                item_data = {
                    "color": mapped_color,
                    "original_color": original_color_id,
                    "collected_at": item.collected_at.strftime("%Y-%m-%d %H:%M:%S"),
                    # Remove the special markers for items 5 and 6
                }
                items.append(item_data)

        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<int:generation>/PipedText")
def PipedText(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"PipedText/PipedText_{generation}.html"
    return render_template(template_name, player=player)










# if __name__ == "__main__":
#    app.run(debug=True)

