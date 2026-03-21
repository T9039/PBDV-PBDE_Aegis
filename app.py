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

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///fallback.db"
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
