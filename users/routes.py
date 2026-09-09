from flask import Blueprint

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)

@users_bp.route("/")
def users():
    return "Users Page"

@users_bp.route("/profile")
def profile():
    return "profile Page"