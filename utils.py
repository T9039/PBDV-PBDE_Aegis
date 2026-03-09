import os
import random
import smtplib
import socket

from dotenv import load_dotenv
from email_validator import EmailNotValidError, validate_email
from werkzeug.security import check_password_hash, generate_password_hash

from models import CampusRole, MentorStatus, User, db

# -------------------------------------------------------------------
# MOCK DATABASE SETUP
# -------------------------------------------------------------------

# We define the dictionary, but we will populate it using a function
# so the passwords get hashed properly when the app starts.
CAMPUS_DB = {}


# def seed_database():
#     """Populates the dummy database with initial users."""
#     add_user(
#         email="22012345@dut4life.ac.za",
#         plain_password="password123",
#         full_name="Thuto",
#         role="student",
#         department="ICT",
#     )
#     add_user(
#         email="alex@dut.ac.za",
#         plain_password="admin",
#         full_name="Alex Johnson",
#         role="mentor",
#         department="Computer Science",
#         is_profile_complete=True,  # Alex already set up their profile
#     )


# -------------------------------------------------------------------
# DATABASE HELPER FUNCTIONS (CRUD & Auth)
# -------------------------------------------------------------------


def add_user(
    email,
    plain_password,
    full_name,
    role="student",
    is_profile_complete=False,
):
    """Adds a new user to the MariaDB database with a securely hashed password."""

    # 1. Check if the user already exists to prevent duplicate entries
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False, "User already exists"

    # 2. Convert the string role into our strict CampusRole Enum
    mapped_role = CampusRole.STAFF if role.lower() == "staff" else CampusRole.STUDENT

    # 3. Create the SQLAlchemy User object
    new_user = User(
        email=email,
        password_hash=generate_password_hash(plain_password),
        full_name=full_name,
        campus_role=mapped_role,
        mentor_status=MentorStatus.NONE,
    )

    # Manually set fields not handled by the __init__ constructor
    new_user.is_profile_complete = is_profile_complete

    # 4. Save to the database safely
    try:
        db.session.add(new_user)
        db.session.commit()
        return True, "User created successfully"
    except Exception as e:
        db.session.rollback()  # Cancel the transaction if it crashes
        print(f"Error adding user to DB: {e}")
        return False, "Database error occurred"


def delete_user(email):
    """Removes a user from the MariaDB database."""
    user = User.query.filter_by(email=email).first()

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user from DB: {e}")
            return False

    return False


def get_user(email):
    """Fetches a user from the DB and returns their data as a dictionary."""
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            "email": user.email,
            "campus_role": user.campus_role.value,  # student or staff
            "mentor_status": user.mentor_status.value,  # none, pending, approved
            "full_name": user.full_name,
            "is_profile_complete": user.is_profile_complete,
        }
    return None


def verify_credentials(email, password):
    """Checks if the email exists in the DB and the password matches the hash."""
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return True
    return False


def update_password(email, new_plain_password):
    """Updates a user's password with a fresh hash in the database."""
    user = User.query.filter_by(email=email).first()

    if user:
        try:
            # 1. Generate the new hash and assign it to the user object
            user.password_hash = generate_password_hash(new_plain_password)

            # 2. Commit the transaction to save it permanently in MariaDB
            db.session.commit()
            return True

        except Exception as e:
            # If the database crashes during the save, roll back the transaction
            # so we don't accidentally corrupt the table.
            db.session.rollback()
            print(f"Error updating password in DB: {e}")
            return False

    return False


# FUNCTIONS
def generate_otp():
    return str(random.randint(100000, 999999))


load_dotenv(override=True)


def send_email(to_email, subject, body):
    # 1. Pull credentials dynamically from the .env file
    mailtrap_user = os.getenv("MAILTRAP_USERNAME")
    mailtrap_pass = os.getenv("MAILTRAP_PASSWORD")

    print(f"🔥 DEBUG: Sending as user -> {mailtrap_user}")
    if not mailtrap_user or not mailtrap_pass:
        print("Error: Mailtrap credentials missing from .env file!")
        return False

    try:
        socket.create_connection(("smtp.mailtrap.io", 587), timeout=5)
    except Exception as e:
        print("Cannot connect to Mailtrap:", e)

    try:
        with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
            server.starttls()
            # 2. Authenticate using the dynamic credentials
            server.login(mailtrap_user, mailtrap_pass)

            # 3. Format proper email headers
            sender_email = "auth@aegis.local"
            message = (
                f"Subject: {subject}\nFrom: {sender_email}\nTo: {to_email}\n\n{body}"
            )

            server.sendmail(sender_email, to_email, message)

        return True
    except Exception as e:
        print("Email send failed:", e)
        return False


def is_valid_dut_email(email: str) -> bool:
    """
    Checks if the email has valid format and DUT domain.
    """
    try:
        v = validate_email(email)
        email_normalized = v.email.lower()
        if not (
            email_normalized.endswith("@dut.ac.za")
            or email_normalized.endswith("@dut4life.ac.za")
        ):
            return False
        return True
    except EmailNotValidError:
        return False
