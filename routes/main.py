from flask import Blueprint, render_template

# Create the blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def student_view():
    return render_template("main/student-view.html")


# Route for the Mentor Profile View
@main_bp.route("/mentor")
def mentor_profile():
    return render_template("main/mentor-profile.html")
