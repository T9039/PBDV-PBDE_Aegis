import os
import random
import smtplib
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv
from email_validator import EmailNotValidError, validate_email
from werkzeug.security import check_password_hash, generate_password_hash

from models import CampusRole, MentorStatus, User, db

BASE_UPLOAD_FOLDER = "uploads"

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


def send_email(to_email, subject, body, sender_name="StudySphere Admin"):
    """
    The Triple-Threat Email Router:
    Tier 1: SendGrid REST API (Primary)
    Tier 2: Real SMTP (Fallback)
    Tier 3: Mailtrap (Sandbox / Emergency Fallback)
    """
    # 1. Intercept Dummy Accounts immediately
    dummy_emails = [
        "student1@dut4life.ac.za",
        "student2@dut4life.ac.za",
        "mentor@dut.ac.za",
        "admin@dut.ac.za",
    ]

    if to_email.lower() in dummy_emails:
        print(f"🧪 [SANDBOX] Routing {to_email} directly to Mailtrap.")
        return send_via_mailtrap(to_email, subject, body, sender_name)

    # 2. Attempt TIER 1: SendGrid REST API
    print(f"🚀 [API] Attempting to send to {to_email} via SendGrid API...")
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    real_sender = os.getenv("REAL_SENDER_ADDRESS", "auth@aegis.local")

    if sendgrid_key:
        try:
            headers = {
                "Authorization": f"Bearer {sendgrid_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": real_sender, "name": sender_name},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}],
            }

            # Make the web request (Timeout after 5 seconds so the user isn't kept waiting)
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                json=payload,
                headers=headers,
                timeout=5,
            )

            if response.status_code in [200, 201, 202]:
                print("✅ [API] Success! Email sent via SendGrid.")
                return True
            else:
                print(f"⚠️ [API] SendGrid rejected the request: {response.text}")

        except Exception as e:
            print(f"⚠️ [API] Network error hitting SendGrid: {e}")
    else:
        print("⚠️ [API] No SENDGRID_API_KEY found in .env.")

    # 3. Attempt TIER 2: Real SMTP Fallback (If API failed or key is missing)
    print("🔄 [SMTP] Falling back to Real SMTP Server...")
    smtp_host = os.getenv("REAL_SMTP_HOST")
    smtp_user = os.getenv("REAL_SMTP_USER")
    smtp_pass = os.getenv("REAL_SMTP_PASS")

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["To"] = to_email
            msg["From"] = f"{sender_name} <{real_sender}>"
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(
                smtp_host, int(os.getenv("REAL_SMTP_PORT", 587)), timeout=5
            ) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

            print("✅ [SMTP] Success! Email sent via Real SMTP.")
            return True

        except Exception as e:
            print(f"⚠️ [SMTP] Real SMTP failed: {e}")
    else:
        print("⚠️ [SMTP] Real SMTP credentials missing in .env.")

    # 4. Attempt TIER 3: Emergency Sandbox Fallback
    print("🚨 [EMERGENCY] All real services failed. Diverting to Mailtrap...")
    return send_via_mailtrap(to_email, subject, body, sender_name)


def send_via_mailtrap(to_email, subject, body, sender_name):
    """Helper function to handle Mailtrap routing cleanly."""
    try:
        msg = MIMEMultipart()
        msg["Subject"] = f"[TEST] {subject}"
        msg["To"] = to_email
        msg["From"] = f"{sender_name} <auth@aegis.local>"
        msg.attach(MIMEText(body, "plain"))

        # Grab the variables
        user = os.getenv("MAILTRAP_USERNAME")
        password = os.getenv("MAILTRAP_PASSWORD")

        # The Type-Safe Guard: Tell the linter we won't proceed if they are None
        if not user or not password:
            print("❌ [FATAL] Mailtrap credentials missing in .env.")
            return False

        with smtplib.SMTP("smtp.mailtrap.io", 587, timeout=5) as server:
            server.starttls()
            server.login(user, password)  # Linter is happy now!
            server.send_message(msg)

        print("✅ [MAILTRAP] Email successfully caught in sandbox.")
        return True
    except Exception as e:
        print(f"❌ [FATAL] Total system failure. Mailtrap also down: {e}")
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


def save_uploaded_file(file_obj, user_id, user_role, category, sub_category):
    """
    Saves a file into a structured directory: uploads/<category>/<sub_category>/
    Example Output: uploads/documents/cvs/staff_5_20260310_a1b2c3_resume.pdf
    """
    if not file_obj or file_obj.filename == "":
        return None

    # 1. Build the nested directory path (e.g., "uploads/documents/cvs")
    target_dir = os.path.join(BASE_UPLOAD_FOLDER, category, sub_category)
    os.makedirs(target_dir, exist_ok=True)

    # 2. Extract ONLY the file extension (e.g., '.pdf') and make it lowercase
    _, ext = os.path.splitext(file_obj.filename)
    ext = ext.lower()

    # 3. Create the strictly controlled filename
    # Format: {role}_{id}_{date}_{uuid}{extension}
    date_str = datetime.now().strftime("%Y%m%d")
    unique_hash = uuid.uuid4().hex[:8]

    new_filename = f"{user_role}_{user_id}_{date_str}_{unique_hash}{ext}"

    # 4. Build the full save path
    file_path = os.path.join(target_dir, new_filename)

    # 5. Save the file
    file_obj.save(file_path)

    # 6. Return the clean path for the database
    db_path = f"{category}/{sub_category}/{new_filename}"

    return db_path
