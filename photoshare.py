from flask import request, redirect, url_for, flash, g, session
from werkzeug import check_password_hash

import tools

bp = tools.MyBlueprint("photos", "photoshare", host="photoshare.act25.com")

def check_user():
    user_id = session.get("user_id")
    if user_id:
        user = tools.select_to_orm(g.cur, "users", f"WHERE id = {user_id}")
        if user:
            return False # all good
    session.clear()
    flash("You must be logged in! ")
    return redirect(url_for("photos.home"))

@bp.route("/")
@bp.route("/home")
def home():
    user_id = session.get("user_id")

    if user_id:
        user = tools.select_to_orm(g.cur, "users", f"WHERE id = {user_id}")
        if user:
            return bp.render("dashboard.html", user=user)

    return bp.render("login.html")

@bp.route("/post/login", methods=["POST"])
def login_handler():
    username = request.form.get("username")
    password = request.form.get("password")

    end = redirect(url_for("photos.home"))

    user = tools.select_to_orm(g.cur, "users", f"WHERE username = '{username}'")
    if user:
        if check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}.", "pos")
            return end

    flash("Incorrect username or password.", "neg")
    return end

@bp.route("/group/<group_id>/albums")
def albums(group_id: int):
    if ue := check_user(): return ue

    group = tools.select_to_orm(g.cur, "groups", f"WHERE id = {group_id}")
    albums = tools.select_to_orm(g.cur, "albums", f"WHERE group = {group_id}", fetch=-1)

    return bp.render("albums.html", group=group, albums=albums)

@bp.route("/group/<group_id>/albums/<album_id>")
def album(group_id: int, album_id: int):
    if ue := check_user(): return ue

    album = tools.select_to_orm(g.cur, "albums", f"WHERE id = {album_id} AND group = {group_id}")
    