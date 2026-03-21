from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models import CampusRole, MentorProfile, MentorStatus, StudentProfile, User, db
from utils import save_uploaded_file  # Import your new function!

# Create the blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    # If they are ALREADY logged in and happen to visit the homepage,
    # politely escort them back to their dashboard so they don't have to log in again.
    # if session.get("logged_in"):
    #     campus_role = session.get("campus_role", "student").lower()
    #     target_url = "/student" if campus_role == "student" else "/mentor"
    #
    #     return jsonify({"success": True, "redirect": target_url}), 200

    # Otherwise, show the beautiful public marketing page
    return render_template("main/index.html")


# Route for the Mentor Profile View
@main_bp.route("/mentor-dashboard")
def mentor_dashboard():
    # 1. Security: Are they logged in?
    if "user_id" not in session:
        return redirect(url_for("auth.login"))  # Adjust route name as needed

    # 2. Fetch the user and their mentor profile
    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    # 3. Security: Are they allowed here? (Staff or Approved Student-Mentors)
    is_staff = user.campus_role == CampusRole.STAFF
    is_approved_student = (
        user.campus_role == CampusRole.STUDENT
        and user.mentor_status == MentorStatus.APPROVED
    )

    if not (is_staff or is_approved_student):
        # Kick them to the student dashboard if they don't belong here
        return redirect(url_for("main.student_dashboard"))

    # 4. Render template and pass the database objects directly to Jinja
    return render_template(
        "main/mentor_dashboard.html", user=user, profile=user.mentor_profile
    )


@main_bp.route("/mentor/complete-profile", methods=["POST"])
def complete_profile():
    # 1. Security Check: Are they actually logged in?
    email = session.get("email")
    if not email:
        return jsonify(
            {"success": False, "error": "You must be logged in to do this."}
        ), 401

    # 2. Get the form data AND the files (No more JSON!)
    data = request.form
    cv_file = request.files.get("cv_file")
    transcript_file = request.files.get("transcript_file")

    # 3. Find the user in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "error": "User not found in database."}), 404

    # 4. Process the File Uploads
    # Get the role string (e.g., 'student' or 'staff') for the filename
    role_str = user.campus_role.value

    # Save the CV securely
    cv_path = save_uploaded_file(
        file_obj=cv_file,
        user_id=user.id,
        user_role=role_str,
        category="documents",
        sub_category="cvs",
    )

    # Save the Transcript securely
    transcript_path = save_uploaded_file(
        file_obj=transcript_file,
        user_id=user.id,
        user_role=role_str,
        category="documents",
        sub_category="transcripts",
    )

    if not cv_path:
        return jsonify({"success": False, "error": "A CV (PDF) is required."}), 400

    try:
        # 5. Update the core User table
        user.full_name = data.get("full_name", user.full_name)
        user.is_profile_complete = True

        # 6. Create their new MentorProfile record
        new_profile = MentorProfile(
            user_id=user.id,
            modules=data.get("modules"),
            faculty=data.get("faculty"),
            study_level=data.get("study_level"),
            year_of_study=data.get("year_of_study", ""),
            cv_file_path=cv_path,  # Real path saved here!
            awards=data.get("awards"),
            linkedin_url=data.get("linkedin_url"),
            portfolio_url=data.get("portfolio_url"),
        )

        # 7. Save everything to MariaDB safely
        db.session.add(new_profile)
        db.session.commit()

        # 8. Update the session variables so the UI knows they are complete!
        session["is_profile_complete"] = True
        session["full_name"] = user.full_name

        return jsonify(
            {"success": True, "message": "Profile completed successfully!"}
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving mentor profile: {e}")
        return jsonify({"success": False, "error": "A database error occurred."}), 500


@main_bp.route("/mentor/profile", methods=["GET"])
def mentor_profile():
    # 1. Ensure they are logged in
    email = session.get("email")
    if not email:
        return redirect("/")  # Or redirect to your login route

    # 2. Fetch the User and their Profile
    user = User.query.filter_by(email=email).first()

    # If they are logged in but somehow deleted, kick them out
    if not user:
        return redirect("/")

    # Fetch the linked mentor profile
    profile = MentorProfile.query.filter_by(user_id=user.id).first()

    # 3. Render the new page, passing the data to Jinja
    return render_template("mentor/mentor-profile.html", user=user, profile=profile)


@main_bp.route("/mentor/edit-profile", methods=["POST"])
def edit_profile():
    email = session.get("email")
    if not email:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    profile = MentorProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        return jsonify({"success": False, "error": "Profile not found"}), 404

    # 1. Get the incoming data
    data = request.form
    cv_file = request.files.get("cv_file")
    transcript_file = request.files.get("transcript_file")

    try:
        # 2. Update the User model
        user.full_name = data.get("full_name", user.full_name)
        session["full_name"] = (
            user.full_name
        )  # Update session so navbar changes instantly

        # 3. Update the MentorProfile model
        profile.year_of_study = data.get("year_of_study", profile.year_of_study)
        profile.subjects = data.get("subjects", profile.subjects)
        profile.experience = data.get("experience", profile.experience)
        profile.bio = data.get("bio", profile.bio)
        profile.motivation = data.get("motivation", profile.motivation)
        profile.linkedin_url = data.get("linkedin_url", profile.linkedin_url)
        profile.certifications = data.get("certifications", profile.certifications)

        # 4. Handle Optional File Replacements
        role_str = (
            user.campus_role.value
            if hasattr(user.campus_role, "value")
            else str(user.campus_role)
        )

        if cv_file and cv_file.filename != "":
            profile.cv_file_path = save_uploaded_file(
                cv_file, user.id, role_str, "documents", "cvs"
            )

        if transcript_file and transcript_file.filename != "":
            profile.transcript_file_path = save_uploaded_file(
                transcript_file, user.id, role_str, "documents", "transcripts"
            )

        # 5. Commit to database
        db.session.commit()
        return jsonify(
            {"success": True, "message": "Profile updated successfully!"}
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating profile: {e}")
        return jsonify({"success": False, "error": "Database error occurred."}), 500


# @main_bp.route("/student/dashboard")
# def student_dashboard():
#     email = session.get("email")
#     if not email:
#         return redirect("/")
#
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return redirect("/")
#
#     # Fetch mentors for the cards
#     mentors = db.session.query(MentorProfile, User).join(User).all()
#
#     has_profile = StudentProfile.query.filter_by(user_id=user.id).first() is not None
#
#     # --- ADD THIS PRINT STATEMENT ---
#     print(f"DEBUG: User {user.email} | Profile Found: {has_profile}")
#     # --------------------------------
#
#     return render_template(
#         "student/dashboard.html", mentors=mentors, has_profile=has_profile
#     )


@main_bp.route("/student/complete-profile", methods=["POST"])
def complete_student_profile():
    email = session.get("email")
    if not email:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"success": False, "error": "User account not found."}), 404

    # Check if they already have one to prevent duplicates
    if StudentProfile.query.filter_by(user_id=user.id).first():
        return jsonify({"success": False, "error": "Profile already exists."}), 400

    data = request.form

    try:
        new_profile = StudentProfile(
            user_id=user.id,
            faculty=data.get("faculty"),
            degree_program=data.get("degree_program"),
            study_level=data.get("study_level"),
            year_of_study=data.get("year_of_study"),
            subjects_needing_help=data.get("subjects_needing_help"),
            preferred_learning_style=data.get("preferred_learning_style"),
            bio=data.get("bio"),
        )
        db.session.add(new_profile)
        db.session.commit()

        return jsonify(
            {"success": True, "message": "Welcome to Aegis! Profile saved."}
        ), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error saving student profile: {e}")
        return jsonify({"success": False, "error": "Database error occurred."}), 500


@main_bp.route("/student/profile", methods=["GET"])
def student_profile_view():
    email = session.get("email")
    if not email:
        return redirect("/")

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect("/")

    profile = StudentProfile.query.filter_by(user_id=user.id).first()

    # We still want to pass has_profile so the base template's navbar works correctly
    return render_template(
        "student/student-profile.html",
        user=user,
        profile=profile,
        has_profile=(profile is not None),
    )


@main_bp.route("/student/edit-profile", methods=["POST"])
def edit_student_profile():
    email = session.get("email")
    if not email:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "error": "User not found."}), 404

    profile = StudentProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        return jsonify({"success": False, "error": "Profile not found."}), 404

    data = request.form

    try:
        # Update User data
        user.full_name = data.get("full_name", user.full_name)
        session["full_name"] = user.full_name  # Keep the session in sync

        # Update Profile data
        profile.degree_program = data.get("degree_program", profile.degree_program)
        profile.year_of_study = data.get("year_of_study", profile.year_of_study)
        profile.subjects_needing_help = data.get(
            "subjects_needing_help", profile.subjects_needing_help
        )
        profile.primary_goals = data.get("primary_goals", profile.primary_goals)
        profile.preferred_learning_style = data.get(
            "preferred_learning_style", profile.preferred_learning_style
        )
        profile.bio = data.get("bio", profile.bio)

        db.session.commit()
        return jsonify(
            {"success": True, "message": "Profile updated successfully!"}
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating student profile: {e}")
        return jsonify({"success": False, "error": "Database error occurred."}), 500


@main_bp.route("/student-dashboard")
def student_dashboard():
    # 1. Security: Are they logged in?
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # 2. Fetch the user
    user = User.query.get(session["user_id"])

    # Safety catch in case the session cookie outlived the database record
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    # 3. Security: Are they a student? (Or staff acting as a student)
    if user.campus_role != CampusRole.STUDENT and user.campus_role != CampusRole.STAFF:
        return redirect(url_for("auth.login"))

    # 4. Pass the user and their specific profile to Jinja
    return render_template(
        "main/student_dashboard.html", user=user, profile=user.student_profile
    )


@main_bp.route("/admin-dashboard")
def admin_dashboard():
    # 1. Security: Are they logged in?
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    # 2. Strict Admin Check
    # (You can change this to check a specific 'is_admin' boolean if you add one later)
    if user.email != "Admin@dut.ac.za":
        # Kick unauthorized users back to their respective dashboards
        if user.campus_role == CampusRole.STAFF:
            return redirect(url_for("main.mentor_dashboard"))
        return redirect(url_for("main.student_dashboard"))

    return render_template("main/admin_dashboard.html", user=user)
