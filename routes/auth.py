import time

from flask import Blueprint, jsonify, redirect, render_template, request, session

from utils import generate_otp, is_valid_dut_email, send_email

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

        # user = User.query.filter_by(user_email=email).first()
        #
        # # Check credentials
        # if not user or not user.check_pass_hash(password):
        #     msg = "Invalid email or password."
        #     if request.is_json:
        #         return jsonify({"success": False, "message": msg}), 401
        #     return msg, 401
        #
        # # ✅ Store session data safely
        # session["user_id"] = user.user_id
        # session["email"] = user.user_email
        # session["role"] = user.user_role.value  # <-- FIXED HERE
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
            return jsonify({"success": True, "redirect": "/"}), 200

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
                "message": "Session expired or invalid. Please log in again.",
                "success": False,
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
            {"success": False, "message": "OTP expired. Please request a new one."}
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
            {"success": False, "message": "Too many attempts. A new OTP has been sent."}
        )

    # 5. Check Code (Cast both to strings just in case JS sends an int)
    if str(otp_input).strip() == str(otp_code).strip():
        session.pop("otp_code", None)
        session.pop("otp_expiry", None)
        session.pop("otp_attempts", None)
        session.pop("otp_round", None)
        session["logged_in"] = True

        response = jsonify({"success": True, "redirect": "/"})

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
            "message": f"Incorrect code. Attempt {current_attempts} of 3.",
        }
    )


@auth_bp.route("/login/otp/resend", methods=["POST"])
def login_otp_resend():
    otp_email = session.get("otp_email")
    if not otp_email:
        return jsonify({"success": False, "message": "No email in session"}), 400

    new_otp = generate_otp()
    session["otp_code"] = new_otp
    session["otp_expiry"] = (
        int(time.time()) + 300
    )  # Current time in seconds + 300 seconds (5 mins)
    session["otp_attempts"] = 0
    session["otp_round"] = session.get("otp_round", 1) + 1

    send_email(otp_email, "Your OTP Code", f"Your OTP is {new_otp}")

    return jsonify({"success": True, "message": f"New OTP sent to {otp_email}"}), 200


# @auth_bp.route("/forgot-password", methods=["GET", "POST"])
# def forgot_password():
#     if request.method == "GET":
#         return render_template("auth/forgot_password.html")
#     # Logic for verifying email and sending reset link goes here
#     return jsonify({"success": True, "message": "Reset link sent if email exists."})
