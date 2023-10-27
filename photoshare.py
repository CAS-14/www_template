from flask import request

import tools

bp = tools.MyBlueprint("photos", "photoshare", host="photoshare.act25.com")

@bp.route("/")
@bp.route("/home")
def home():
    return bp.render("home.html")