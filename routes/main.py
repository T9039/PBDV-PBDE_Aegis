from flask import Blueprint, jsonify, render_template, request, session

from models import MentorProfile, User, db

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
    return render_template("main/home.html")


# Route for the Mentor Profile View
@main_bp.route("/mentor")
def mentor_profile():
    return render_template("main/mentor-profile.html")


@main_bp.route("/mentor/complete-profile", methods=["POST"])
def complete_profile():
    # 1. Security Check: Are they actually logged in?
    email = session.get("email")
    if not email:
        return jsonify(
            {"success": False, "error": "You must be logged in to do this."}
        ), 401

    # 2. Get the JSON payload sent by our fetch request
    data = request.get_json()

    # 3. Find the user in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(
            {"success": False, "message": "User not found in database."}
        ), 404

    try:
        # 4. Update the core User table
        user.full_name = data.get("full_name", user.full_name)
        user.is_profile_complete = True

        # 5. Create their new MentorProfile record
        # Note: We link it to the user via user.id
        new_profile = MentorProfile(
            user_id=user.id,
            subjects_to_teach=data.get("subjects"),
            motivation=data.get("motivation"),
            bio=data.get("bio", ""),
        )

        # 6. Save everything to MariaDB safely
        db.session.add(new_profile)
        db.session.commit()

        # 7. Update the session variables so the UI knows they are complete!
        session["is_profile_complete"] = True
        session["full_name"] = user.full_name

        return jsonify(
            {"success": True, "message": "Profile completed successfully!"}
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving mentor profile: {e}")
        return jsonify({"success": False, "message": "A database error occurred."}), 500


@main_bp.route("/student")
def student_profile():
    return render_template("main/student-view.html")
