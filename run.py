import os
from app import create_app, db
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = create_app()

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Expose WSGI application for deployment
application = app

if __name__ == "__main__":
    app.run(debug=True)
