from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

# Define your routes here
@dashboard_bp.route('/')
def index():
    return 'Dashboard Home'
