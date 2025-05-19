"""
Main entry point for the Window Wash CRM application.
This file allows running the app as a standalone application.
"""

from ww_crm.app import app
from ww_crm.db import db

# Ensure database tables exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
