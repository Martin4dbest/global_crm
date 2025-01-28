from flask import Blueprint

organizations_bp = Blueprint('organizations', __name__)

# Define your routes here
@organizations_bp.route('/')
def index():
    return 'Organizations Home'

