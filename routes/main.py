from flask import Blueprint, redirect, render_template, session, url_for

from models import CampusRole, MentorStatus, User

# Create the blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    # Show the beautiful public marketing page
    return render_template("main/index.html")


@main_bp.route("/mentor-dashboard")
def mentor_dashboard():
    # 1. Security: Are they logged in?
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

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
    if user.email != "Admin@dut.ac.za":
        # Kick unauthorized users back to their respective dashboards
        if user.campus_role == CampusRole.STAFF:
            return redirect(url_for("main.mentor_dashboard"))
        return redirect(url_for("main.student_dashboard"))

    return render_template("main/admin_dashboard.html", user=user)
