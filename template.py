from flask import request

import tools

bp = tools.MyBlueprint("BP_NAME", "REPO_NAME", host="DOMAIN")

@bp.route("/")
@bp.route("/home")
def home():
    return bp.render("home.html")