import time
import uuid

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models import User
from utils import (
    generate_otp,
    get_user,
    is_valid_dut_email,
    send_email,
    update_password,
    verify_credentials,
)

# Create the blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle JSON and form data
        if request.is_json:
            data = request.get_json()
            email = data.get("email", "").strip().lower()
            password = data.get("password", "")
            remember_me = data.get("rememberMe", False)
        else:
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            remember_me = request.form.get("rememberMe", False)
        # Validation
        if not email or not password:
            msg = "Email and password are required."
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 400
            return msg, 400

        if not is_valid_dut_email(email):
            msg = "Please use a valid DUT email (@dut.ac.za or @dut4life.ac.za)."
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 400
            return msg, 400

        if not verify_credentials(email, password):
            return jsonify(
                {"success": False, "error": "Invalid campus email or password."}
            ), 401

        # 2. Fetch the user's details safely (Replaces your old User.query)
        user = get_user(email) or {}

        # 3. Store session data safely
        session["email"] = user.get("email")
        session["campus_role"] = user.get("campus_role")
        session["mentor_status"] = user.get("mentor_status")
        session["full_name"] = user.get("full_name")
        session["is_profile_complete"] = user.get("is_profile_complete")
        #
        # # ✅ Decide redirect URL based on role
        # role_value = user.user_role.value.lower()
        #
        # if role_value == "admin":
        #     redirect_url = "/admin/dashboard"
        # elif role_value == "technician":
        #     redirect_url = "/technician/dashboard"
        # else:
        #     redirect_url = "/user/dashboard"

        cookie_name = f"trusted_{email}"
        is_trusted = request.cookies.get(cookie_name)

        if is_trusted == "yes":
            # BYPASS OTP! Log them straight in.
            session["logged_in"] = True

            campus_role = session.get("campus_role", "student").lower()
            target_url = (
                "/student/dashboard"
                if campus_role == "student"
                else "/mentor/dashboard"
            )

            return jsonify({"success": True, "redirect": target_url}), 200

        # Generate OTP
        otp_code = generate_otp()

        session["otp_email"] = email
        session["remember_device"] = remember_me
        session["otp_code"] = otp_code
        session["otp_expiry"] = (
            int(time.time()) + 300
        )  # Current time in seconds + 300 seconds (5 mins)
        session["otp_attempts"] = 0
        session["otp_round"] = 1

        # Send OTP via email
        send_email(
            email, "Your OTP Code", f"Your OTP is {otp_code}. It expires in 5 minutes."
        )

        # ✅ JSON or form-based response
        redirect_url = "/login/otp"
        if request.is_json:
            return jsonify(
                {
                    "success": True,
                    "message": "Login successful",
                    "redirect": redirect_url,
                }
            ), 200
        else:
            return redirect(redirect_url)

    return render_template("auth/login.html")


@auth_bp.route("/login/otp", methods=["POST", "GET"])
def login_otp():
    if request.method == "GET":
        return render_template("auth/login_otp.html")

    # Safely grab the JSON data
    data = request.get_json(silent=True) or {}
    otp_input = data.get("otp") or request.form.get("otp")

    otp_code = session.get("otp_code")
    otp_expiry_timestamp = session.get("otp_expiry")

    # 1. Catch dropped sessions
    if otp_expiry_timestamp is None:
        return jsonify(
            {
                "error": "Session expired or invalid. Please log in again.",
                "success": False,
                "server_time": int(time.time()),  # Current time
                "expiry": otp_expiry_timestamp,
            }
        ), 400

    # 2. Increment attempts exactly ONCE
    current_attempts = session.get("otp_attempts", 0) + 1
    session["otp_attempts"] = current_attempts
    round_num = session.get("otp_round", 1)
    session.modified = True

    # 3. Timezone-proof expiry check
    if int(time.time()) > otp_expiry_timestamp:
        return jsonify(
            {"success": False, "error": "OTP expired. Please request a new one."}
        )

    # 4. Handle Max Attempts
    if current_attempts >= 3:
        if round_num >= 3:
            session.clear()  # Kick them out
            return jsonify({"success": False, "redirect": "/login"})

        # Resend new OTP
        new_otp = generate_otp()
        session["otp_code"] = new_otp
        session["otp_expiry"] = int(time.time()) + 300
        session["otp_attempts"] = 0
        session["otp_round"] = round_num + 1
        session.modified = True

        send_email(session["otp_email"], "Your OTP Code", f"Your OTP is {new_otp}")
        return jsonify(
            {"success": False, "error": "Too many attempts. A new OTP has been sent."}
        )

    # 5. Check Code (Cast both to strings just in case JS sends an int)
    if str(otp_input).strip() == str(otp_code).strip():
        campus_role = session.get("campus_role", "student").lower()

        session.pop("otp_code", None)
        session.pop("otp_expiry", None)
        session.pop("otp_attempts", None)
        session.pop("otp_round", None)
        session["logged_in"] = True

        # Role based redirect
        target_url = (
            "/student/dashboard" if campus_role == "student" else "/mentor/dashboard"
        )

        response = jsonify({"success": True, "redirect": target_url})

        if session.pop("remember_device", False):
            cookie_name = f"trusted_{session['otp_email']}"
            # max_age=2592000 is exactly 30 days in seconds (30 * 24 * 60 * 60)
            # httponly=True prevents malicious JavaScript from stealing the cookie
            response.set_cookie(cookie_name, "yes", max_age=2592000, httponly=True)

        return response, 200

    # 6. Wrong code
    return jsonify(
        {
            "success": False,
            "error": f"Incorrect code. Attempt {current_attempts} of 3.",
        }
    )


@auth_bp.route("/login/otp/resend", methods=["POST"])
def login_otp_resend():
    otp_email = session.get("otp_email")
    if not otp_email:
        return jsonify(
            {"success": False, "message": "No email in session. Please log in again."}
        ), 400

    new_otp = generate_otp()
    session["otp_code"] = new_otp
    session["otp_expiry"] = (
        int(time.time()) + 300
    )  # Current time in seconds + 300 seconds (5 mins)
    session["otp_attempts"] = 0
    session["otp_round"] = session.get("otp_round", 1) + 1

    # Capture the return value (True or False)
    email_sent = send_email(
        otp_email, "Your OTP Code", f"Your OTP is {new_otp}. It expires in 5 minutes."
    )

    # If send_email returned False, tell the frontend it failed!
    if not email_sent:
        return jsonify(
            {"success": False, "message": "Failed to send OTP email. Please try again."}
        ), 500

    return jsonify({"success": True, "message": f"New OTP sent to {otp_email}"}), 200


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("auth/forgot-password.html")

    data = request.get_json(silent=True) or {}
    email = data.get("email")

    # Security Best Practice: Never tell the user if the email exists or not.
    # It prevents attackers from "guessing" which students have accounts.
    success_message = "If an account matches that email, a reset link has been sent."

    # --- REAL DATABASE QUERY START ---
    user = User.query.filter_by(email=email).first()

    if user:
        # 1. Generate a unique, random token
        reset_token = str(uuid.uuid4())

        # 2. Store it in the session so we can verify it later
        session["reset_token"] = reset_token
        session["reset_email"] = email
        session.modified = True

        # 3. Create the fully qualified URL to send in the email
        # _external=True ensures it includes http://127.0.0.1:5000 in the link
        reset_link = url_for("auth.reset_password", token=reset_token, _external=True)

        # 4. Send it to Mailtrap
        email_body = f"Hello {user.full_name},\n\nYou requested a password reset for Aegis.\n\nClick the link below to set a new password:\n{reset_link}\n\nIf you did not request this, please ignore this email."
        send_email(email, "Aegis - Password Reset Request", email_body)
    # --- REAL DATABASE QUERY END ---

    # We return the exact same success message regardless of if the email was in the DB
    return jsonify({"success": True, "message": success_message})


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # 1. Verify the token against what we saved in the session
    session_token = session.get("reset_token")
    email = session.get("reset_email")

    # If the token doesn't match or is missing, they are using an invalid/expired link
    if not session_token or session_token != token or not email:
        if request.method == "GET":
            # You can redirect to login or render an error page here
            return render_template(
                "auth/login.html", error="Invalid or expired reset link."
            )
        return jsonify(
            {"success": False, "message": "Invalid or expired reset link."}
        ), 400

    # 2. Handle the GET request (Show the form)
    if request.method == "GET":
        return render_template("auth/reset-password.html", token=token)

    # 3. Handle the POST request (Save the new password)
    data = request.get_json(silent=True) or {}
    new_password = data.get("password")

    # This now safely writes to MariaDB because we updated it in utils.py!
    if update_password(email, new_password):
        # Security: Destroy the token so it can't be used twice
        session.pop("reset_token", None)
        session.pop("reset_email", None)
        session.modified = True

        return jsonify(
            {
                "success": True,
                "redirect_url": "/login",
                "message": "Password updated successfully!",
            }
        )

    return jsonify(
        {"success": False, "message": "Failed to update password. User not found."}
    ), 500


@auth_bp.route("/logout")
def logout():
    user_email = session.get("email")

    session.clear()

    response = redirect("/")

    if user_email:
        cookie_name = f"trusted_{user_email}"
        response.delete_cookie(cookie_name)

    return response
