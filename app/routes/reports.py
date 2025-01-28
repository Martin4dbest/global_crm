from flask import Blueprint

reports_bp = Blueprint('reports', __name__)

# Define your routes for reports here
@reports_bp.route('/')
def index():
    return 'Reports Home'
