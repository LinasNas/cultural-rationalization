# #establishes routes for website
# from flask import Flask, redirect, request, session, url_for, render_template
# from flask_session import Session

# from .db import *
# from .helpers import current

# from .api import api

# # Configure application
# app = Flask(__name__)
# app.register_blueprint(api, url_prefix="/api")
# app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

# # Ensure templates are auto-reloaded
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/consent")
# def consent():
#     player = current()
#     if player and player.consent:
#         return redirect("/play")

#     return render_template("consent.html")


# @app.route("/play")
# def play():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")
#     return render_template("play.html")



# @app.route("/rules")
# def rules():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules.html", player=player)


# @app.route("/finish")
# def finish():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("finish.html", player=player)


# @app.route("/introduction")
# def introduction():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("introduction.html", player=player)

# @app.route("/terminate")
# def terminate():
#     player = current()

#     return render_template("terminate.html", player=player)

# @app.route("/rules1")
# def rules1():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules1.html", player=player)


# @app.route("/rules2")
# def rules2():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules2.html", player=player)

# @app.route("/rules3")
# def rules3():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules3.html", player=player)

# @app.route("/Introduction0")
# def introduction0():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("Introduction0.html", player=player)

# @app.route("/Introduction1")
# def introduction1():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("Introduction1.html", player=player)


# # if __name__ == "__main__":
# #    app.run(debug=True)




#establishes routes for website
from flask import Flask, redirect, request, session, url_for, render_template
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

# @app.route("/rules3")
# def rules3():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("rules3.html", player=player)
@app.route("/<int:generation>/rules3")
def rules3(generation):
    player = current()
    if not (player and player.consent):
        return redirect("/consent")

    template_name = f"rules3/rules3_{generation}.html"
    return render_template(template_name, player=player)

# @app.route("/finish")
# def finish():
#     player = current()
#     if not (player and player.consent):
#         return redirect("/consent")

#     return render_template("finish.html", player=player)
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


# @app.route("/terminate")
# def terminate():
#     player = current()

#     return render_template("terminate.html", player=player)

@app.route("/<int:generation>/terminate")
def terminate(generation):
    player = current()
    template_name = f"terminate/terminate_{generation}.html"
    return render_template(template_name, player=player)

# if __name__ == "__main__":
#    app.run(debug=True)