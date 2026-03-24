import os

from dotenv import load_dotenv
from flask import Flask

from models import db
from routes.api import api_bp
from routes.auth import auth_bp
from routes.main import main_bp

# from utils import seed_database

load_dotenv(override=True)

app = Flask(__name__)

# Development secret key (change for production!)
app.secret_key = "secret_super_development_key_for_testing"

# --- SECURITY ENHANCEMENTS ---
# Prevents JavaScript from reading the session cookie (Stops XSS attacks)
app.config["SESSION_COOKIE_HTTPONLY"] = True

# Prevents the browser from sending your cookie to StudySphere if the request came from a different website (Stops CSRF attacks)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# Grab the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- SQLITE PIVOT ---
# This creates a file called 'studysphere.db' right inside your project folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'studysphere.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# 4. Create the tables before the first request
with app.app_context():
    db.create_all()
    print("✅ Database tables checked/created successfully!")

# Registering blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    # debug=True automatically reloads the server when you make changes to your Python code
    app.run(debug=True)
