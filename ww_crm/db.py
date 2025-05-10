import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database instance
db = SQLAlchemy()


def configure_db(app: Flask):
    """
    Configure database connection for the Flask application.

    Args:
        app: The Flask application instance

    This function sets up the SQLAlchemy database URI and initializes
    the database with the application.
    """
    # Get the path to the database file
    db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database with app
    db.init_app(app)
