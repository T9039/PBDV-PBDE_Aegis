import random
import smtplib
import socket

from email_validator import EmailNotValidError, validate_email
from werkzeug.security import check_password_hash, generate_password_hash

# -------------------------------------------------------------------
# MOCK DATABASE SETUP
# -------------------------------------------------------------------

# We define the dictionary, but we will populate it using a function
# so the passwords get hashed properly when the app starts.
CAMPUS_DB = {}


def seed_database():
    """Populates the dummy database with initial users."""
    add_user(
        email="22012345@student.dut4life.ac.za",
        plain_password="password123",
        full_name="Thuto",
        role="student",
        department="ICT",
    )
    add_user(
        email="alex@dut.ac.za",
        plain_password="admin",
        full_name="Alex Johnson",
        role="mentor",
        department="Computer Science",
        is_profile_complete=True,  # Alex already set up their profile
    )


# -------------------------------------------------------------------
# DATABASE HELPER FUNCTIONS (CRUD & Auth)
# -------------------------------------------------------------------


def add_user(
    email,
    plain_password,
    full_name,
    role="student",
    department="",
    is_profile_complete=False,
):
    """Adds a new user to the mock database with a securely hashed password."""
    if email in CAMPUS_DB:
        return False, "User already exists"

    CAMPUS_DB[email] = {
        "password_hash": generate_password_hash(plain_password),
        "full_name": full_name,
        "role": role,
        "department": department,
        "is_profile_complete": is_profile_complete,
    }
    return True, "User created successfully"


def delete_user(email):
    """Removes a user from the mock database."""
    if email in CAMPUS_DB:
        del CAMPUS_DB[email]
        return True
    return False


def get_user(email):
    """Retrieves a user's data without exposing the password hash."""
    user = CAMPUS_DB.get(email)
    if not user:
        return None

    # Return a copy of the data WITHOUT the password hash for safety
    safe_user_data = user.copy()
    safe_user_data.pop("password_hash", None)
    return safe_user_data


def verify_credentials(email, plain_password):
    """Checks if the email exists and the password matches the hash."""
    user = CAMPUS_DB.get(email)
    if not user:
        return False  # Email not found

    # check_password_hash does the heavy lifting of comparing the plain text to the hash
    return check_password_hash(user["password_hash"], plain_password)


# FUNCTIONS
def generate_otp():
    return str(random.randint(100000, 999999))


def send_email(to_email, subject, body):
    try:
        socket.create_connection(("smtp.mailtrap.io", 587), timeout=5)
        print("Can reach Mailtrap SMTP!")
    except Exception as e:
        print("Cannot connect to Mailtrap:", e)

    """
    Simplest option: use Gmail SMTP or Mailtrap.io (free).
    For a school project you can hardcode Mailtrap credentials.
    """
    from_email = "aa66b1448e7173"
    from_password = "370f53b9a831dc"

    try:
        with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(from_email, to_email, message)
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


# Initialize the dummy data when this file is imported
seed_database()
