from flask import Blueprint

products_bp = Blueprint(
    "products",
    __name__
)

@products_bp.route("/products")
def products():
    return "products Page"