from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Migrate
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()

# Load environment variables from .env file
load_dotenv()

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Initialize the app
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Set up login manager
    login_manager.login_view = 'auth.login'  # The login page endpoint

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.organizations import organizations_bp
    from .routes.reports import reports_bp
    from .routes.payments import payments_bp

    # Import models here to avoid circular import
    from .models import Tenant, User, Donation, Attendance, Invoice

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(organizations_bp, url_prefix='/organizations')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(payments_bp, url_prefix='/payments')

    return app
