from flask import Blueprint, redirect, render_template, session

# Create the blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    # If they are ALREADY logged in and happen to visit the homepage,
    # politely escort them back to their dashboard so they don't have to log in again.
    if session.get("logged_in"):
        role = session.get("role", "student")
        return redirect("/mentor" if role == "mentor" else "/student")

    # Otherwise, show the beautiful public marketing page
    return render_template("main/home.html")


# Route for the Mentor Profile View
@main_bp.route("/mentor")
def mentor_profile():
    return render_template("main/mentor-profile.html")


@main_bp.route("/student")
def student_profile():
    return render_template("main/student-view.html")
