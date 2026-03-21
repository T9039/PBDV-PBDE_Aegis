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
from werkzeug.security import check_password_hash, generate_password_hash

from models import CampusRole, MentorProfile, MentorStatus, StudentProfile, User, db
from utils import (
    generate_otp,
    get_user,
    is_valid_dut_email,
    save_uploaded_file,
    send_email,
    update_password,
)

# Create the blueprint
auth_bp = Blueprint("auth", __name__)


# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
# if request.method == "POST":
#     # Handle JSON and form data
#     if request.is_json:
#         data = request.get_json()
#         email = data.get("email", "").strip().lower()
#         password = data.get("password", "")
#         remember_me = data.get("rememberMe", False)
#     else:
#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "")
#         remember_me = request.form.get("rememberMe", False)
#     # Validation
#     if not email or not password:
#         msg = "Email and password are required."
#         if request.is_json:
#             return jsonify({"success": False, "message": msg}), 400
#         return msg, 400
#
#     if not is_valid_dut_email(email):
#         msg = "Please use a valid DUT email (@dut.ac.za or @dut4life.ac.za)."
#         if request.is_json:
#             return jsonify({"success": False, "message": msg}), 400
#         return msg, 400
#
#     if not verify_credentials(email, password):
#         return jsonify(
#             {"success": False, "error": "Invalid campus email or password."}
#         ), 401
#
#     # 2. Fetch the user's details safely (Replaces your old User.query)
#     user = get_user(email) or {}
#
#     # 3. Store session data safely
#     session["email"] = user.get("email")
#     session["campus_role"] = user.get("campus_role")
#     session["mentor_status"] = user.get("mentor_status")
#     session["full_name"] = user.get("full_name")
#     session["is_profile_complete"] = user.get("is_profile_complete")
#     #
#     # # ✅ Decide redirect URL based on role
#     # role_value = user.user_role.value.lower()
#     #
#     # if role_value == "admin":
#     #     redirect_url = "/admin/dashboard"
#     # elif role_value == "technician":
#     #     redirect_url = "/technician/dashboard"
#     # else:
#     #     redirect_url = "/user/dashboard"
#
#     cookie_name = f"trusted_{email}"
#     is_trusted = request.cookies.get(cookie_name)
#
#     if is_trusted == "yes":
#         # BYPASS OTP! Log them straight in.
#         session["logged_in"] = True
#
#         campus_role = session.get("campus_role", "student").lower()
#         target_url = (
#             "/student/dashboard"
#             if campus_role == "student"
#             else "/mentor/dashboard"
#         )
#
#         return jsonify({"success": True, "redirect": target_url}), 200
#
#     # Generate OTP
#     otp_code = generate_otp()
#
#     session["otp_email"] = email
#     session["remember_device"] = remember_me
#     session["otp_code"] = otp_code
#     session["otp_expiry"] = (
#         int(time.time()) + 300
#     )  # Current time in seconds + 300 seconds (5 mins)
#     session["otp_attempts"] = 0
#     session["otp_round"] = 1
#
#     # Send OTP via email
#     send_email(
#         email, "Your OTP Code", f"Your OTP is {otp_code}. It expires in 5 minutes."
#     )
#
#     # ✅ JSON or form-based response
#     redirect_url = "/login/otp"
#     if request.is_json:
#         return jsonify(
#             {
#                 "success": True,
#                 "message": "Login successful",
#                 "redirect": redirect_url,
#             }
#         ), 200
#     else:
#         return redirect(redirect_url)
#
# return render_template("main/login.html")


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


@auth_bp.route("/signup", methods=["GET"])
def signup():
    """Serves the initial signup page."""
    return render_template("main/signup.html")


@auth_bp.route("/api/validate-signup", methods=["POST"])
def validate_signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not is_valid_dut_email(email):
        return jsonify({"error": "Please use a valid DUT email address"}), 400

    if get_user(email):
        return jsonify({"error": "An account with this email already exists"}), 409

    # THE NEW BACKEND LOGIC: Store in Flask Session
    session["reg_email"] = email
    session["reg_password_hash"] = generate_password_hash(password)  # Hash immediately!
    session["reg_is_staff"] = email.lower().endswith("@dut.ac.za")

    return jsonify({"redirect_url": url_for("auth.choose_role")}), 200


@auth_bp.route("/choose-role", methods=["GET", "POST"])
def choose_role():
    # Security check: If they skip step 1, kick them back
    if "reg_email" not in session:
        return redirect(url_for("auth.signup"))

    is_staff = session.get("reg_is_staff", False)

    # Handle the form submission from this page
    if request.method == "POST":
        data = request.get_json()
        role = data.get("role")

        if is_staff and role == "student":
            return jsonify({"error": "Staff accounts must register as mentors."}), 403

        # Save their chosen role to the session
        session["reg_role"] = role

        # Decide where they go next based on role
        if role == "student":
            next_url = url_for("auth.create_student_profile")  # We'll create this next
        else:
            next_url = url_for("auth.create_mentor_profile")  # We'll create this next

        return jsonify({"redirect_url": next_url}), 200

    # GET Request: Render page and pass the is_staff variable to Jinja
    return render_template("main/chooserole.html", is_staff=is_staff)


@auth_bp.route("/student/create-profile", methods=["GET"])
def create_student_profile():
    """Serves the initial signup page."""
    return render_template("main/create_student_profile.html")


@auth_bp.route("/api/register-student", methods=["POST"])
def register_student():
    if "reg_email" not in session:
        return jsonify({"error": "Session expired. Please start over."}), 400

    data = request.get_json()

    try:
        # 1. Create the base User
        new_user = User(
            email=session["reg_email"],
            password_hash=session["reg_password_hash"],
            campus_role=CampusRole.STAFF
            if session.get("reg_is_staff")
            else CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
            full_name=data.get("fullname"),
        )
        new_user.is_profile_complete = True
        db.session.add(new_user)
        db.session.flush()

        # 2. Create the precise Student Profile
        student_profile = StudentProfile(
            user_id=new_user.id,
            faculty=data.get("faculty"),
            degree_program=data.get("degree"),
            study_level=data.get("study_level"),
            year_of_study=data.get("year"),
            subjects_needing_help=data.get("subjects"),
            preferred_learning_style=data.get("style"),
            bio=data.get("bio"),
        )
        db.session.add(student_profile)
        db.session.commit()

        # 3. Clean up the registration session
        session.pop("reg_email", None)
        session.pop("reg_password_hash", None)
        session.pop("reg_role", None)
        session.pop("reg_is_staff", None)

        # Redirect them to the login page (or dashboard if you auto-login)
        return jsonify({"message": "Profile created!", "redirect_url": "/login"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error saving student: {e}")
        return jsonify({"error": "Database error occurred."}), 500


@auth_bp.route("/mentor/create-profile", methods=["GET"])
def create_mentor_profile():
    """Serves the initial signup page."""
    return render_template("main/create_mentor_profile.html")


@auth_bp.route("/api/register-mentor", methods=["POST"])
def register_mentor():
    if "reg_email" not in session:
        return jsonify({"error": "Session expired. Please start over."}), 400

    # 1. Grab text fields from FormData
    fullname = request.form.get("fullname")
    modules = request.form.get("modules")
    faculty = request.form.get("faculty")
    study_level = request.form.get("study_level")
    year_of_study = request.form.get("year_of_study")
    linkedin = request.form.get("linkedin")
    portfolio = request.form.get("portfolio")
    awards = request.form.get("awards")

    # 2. Grab the file object
    cv_file = request.files.get("cv_file")

    # Double-check the file exists before hitting the database
    if not cv_file or cv_file.filename == "":
        return jsonify({"error": "CV file is required."}), 400

    try:
        # 3. Create the base User
        new_user = User(
            email=session["reg_email"],
            password_hash=session["reg_password_hash"],
            campus_role=CampusRole.STAFF
            if session.get("reg_is_staff")
            else CampusRole.STUDENT,
            mentor_status=MentorStatus.PENDING,
            full_name=fullname,
        )
        new_user.is_profile_complete = True

        db.session.add(new_user)
        db.session.flush()  # Flushes to DB to generate the new_user.id WITHOUT committing yet

        # 4. Save the file securely using your utility function
        cv_path = save_uploaded_file(
            file_obj=cv_file,
            user_id=new_user.id,
            user_role="mentor",
            category="documents",
            sub_category="cvs",
        )

        if not cv_path:
            db.session.rollback()
            return jsonify({"error": "Failed to save the uploaded file."}), 500

        # 5. Create the Mentor Profile matching our newly optimized model
        mentor_profile = MentorProfile(
            user_id=new_user.id,
            modules=modules,
            faculty=faculty,
            study_level=study_level,
            year_of_study=year_of_study,
            cv_file_path=cv_path,
            awards=awards,
            linkedin_url=linkedin,
            portfolio_url=portfolio,
        )
        db.session.add(mentor_profile)

        # 6. If everything worked, commit the whole transaction!
        db.session.commit()

        # Wipe registration memory so they can't submit twice
        session.pop("reg_email", None)
        session.pop("reg_password_hash", None)
        session.pop("reg_role", None)
        session.pop("reg_is_staff", None)

        return jsonify(
            {
                "message": "Application submitted successfully!",
                "redirect_url": url_for("auth.login"),
            }
        ), 201

    except Exception as e:
        # If anything fails (file save, database error), roll everything back
        db.session.rollback()
        print(f"Error saving mentor: {e}")
        return jsonify(
            {"error": "A server error occurred while saving your profile."}
        ), 500


@auth_bp.route("/login", methods=["GET"])
def login():
    """Serves the initial signup page."""
    return render_template("main/login.html")


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # 1. Find the user in the database
    user = User.query.filter_by(email=email).first()

    # 2. Validate user exists AND password is correct
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Incorrect email or password. Please try again."}), 401

    # 3. Establish the persistent login session
    session.clear()  # Clear any lingering old sessions/registration data
    session["user_id"] = user.id
    session["user_email"] = user.email
    session["campus_role"] = user.campus_role.value
    session["mentor_status"] = user.mentor_status.value

    # 4. Determine their landing page based on their role
    if user.email == "Admin@dut.ac.za":
        redirect_url = "/admin-dashboard"
    elif user.campus_role == CampusRole.STAFF:
        redirect_url = "/mentor-dashboard"
    elif user.campus_role == CampusRole.STUDENT:
        # If they are an approved student-tutor, we can send them to the mentor dash,
        # or just default all students to the student dash.
        if user.mentor_status == MentorStatus.APPROVED:
            redirect_url = "/mentor-dashboard"
        else:
            redirect_url = "/student-dashboard"
    else:
        redirect_url = "/"

    return jsonify({"message": "Success", "redirect_url": redirect_url}), 200


@auth_bp.route("/logout")
def logout():
    user_email = session.get("email")

    session.clear()

    response = redirect("/")

    if user_email:
        cookie_name = f"trusted_{user_email}"
        response.delete_cookie(cookie_name)

    return response
