from flask import Flask, render_template
from flask_migrate import Migrate

# Create app without importing db to avoid circular imports
app = Flask(__name__)

# Load configuration
app.config.from_mapping(
    SECRET_KEY='dev',  # Change this in production!
    TESTING=False,
    DEBUG=True
)

# Home page route
@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

# Import db after creating app to avoid circular imports
from ww_crm.db import db, configure_db

# Configure database
configure_db(app)

# Setup migrations
migrate = Migrate(app, db)

# Import models to ensure they're known to SQLAlchemy
from ww_crm.models import Customer, Invoice

# Register blueprints
from ww_crm.routes.customers import bp as customers_bp
from ww_crm.routes.invoices import bp as invoices_bp
app.register_blueprint(customers_bp)
app.register_blueprint(invoices_bp)

# Create all tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
