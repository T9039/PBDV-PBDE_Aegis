from flask import Blueprint, jsonify, request, session
from sqlalchemy import func

from models import (
    Availability,
    CampusRole,
    MentorshipSession,
    MentorStatus,
    Message,
    Report,
    ReportStatus,
    Review,
    StudentProfile,
    User,
    db,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def get_current_user_id():
    return session.get("user_id")


# ==========================================
# 1. GET: Mentor Sessions
# ==========================================
@api_bp.route("/sessions", methods=["GET"])
def get_sessions():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = MentorshipSession.query.filter_by(mentor_id=user_id).all()
    result = []

    for s in sessions:
        student = s.student
        student_profile = StudentProfile.query.filter_by(user_id=student.id).first()
        program = (
            student_profile.degree_program if student_profile else "Unknown Program"
        )

        result.append(
            {
                "id": s.id,
                "studentName": student.full_name,
                "studentEmail": student.email,
                "program": program,
                "module": s.module,
                "date": s.date.strftime("%Y-%m-%d"),
                "time": s.time_slot,
                "status": s.status.value,
            }
        )

    return jsonify(result), 200


# ==========================================
# 2. GET & PUT: Mentor Availability
# ==========================================
@api_bp.route("/availability", methods=["GET", "PUT"])
def handle_availability():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == "GET":
        avails = Availability.query.filter_by(mentor_id=user_id).all()
        avail_dict = {}
        for a in avails:
            d_str = a.date.strftime("%Y-%m-%d")
            if d_str not in avail_dict:
                avail_dict[d_str] = []
            # Append to the day's array
            avail_dict[d_str].append(a.time_slot)
        return jsonify(avail_dict), 200

    data = request.get_json()
    date_str = data.get("date")
    slots = data.get("slots", [])

    # 1. Get existing slots so we don't accidentally delete a booked slot!
    existing = Availability.query.filter_by(mentor_id=user_id, date=date_str).all()
    booked_slots = [e.time_slot for e in existing if e.is_booked]

    # 2. Delete all UNBOOKED slots for this date
    Availability.query.filter_by(
        mentor_id=user_id, date=date_str, is_booked=False
    ).delete()

    # 3. Add the new slots (skipping any that are already safely booked)
    for slot in set(slots):
        if slot not in booked_slots:
            new_avail = Availability(
                mentor_id=user_id, date=date_str, time_slot=slot, is_booked=False
            )
            db.session.add(new_avail)

    db.session.commit()
    return jsonify({"message": "Availability updated"}), 200


# ==========================================
# 3. GET: Feedback & Messages
# ==========================================
@api_bp.route("/feedback", methods=["GET"])
def get_feedback():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Get reviews left FOR this mentor
    reviews = Review.query.filter_by(mentor_id=user_id).all()
    rev_data = [
        {
            "rating": r.rating,
            "text": r.review_text,
            "date": r.created_at.strftime("%Y-%m-%d"),
        }
        for r in reviews
    ]

    # Get messages sent TO this mentor (from students)
    msgs = Message.query.filter_by(receiver_id=user_id).all()
    msg_data = [
        {
            "fromName": m.sender.full_name,
            "date": m.created_at.strftime("%Y-%m-%d"),
            "message": m.content,
        }
        for m in msgs
    ]

    return jsonify({"reviews": rev_data, "messages": msg_data}), 200


# ==========================================
# 4. POST: Send Message to Student
# ==========================================
@api_bp.route("/messages", methods=["POST"])
def send_message():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    to_email = data.get("toEmail")

    student = User.query.filter_by(email=to_email).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    msg = Message(
        sender_id=user_id,
        receiver_id=student.id,
        content=data.get("message"),
        performance_rating=data.get("rating"),
    )
    db.session.add(msg)
    db.session.commit()

    return jsonify({"message": "Message sent successfully!"}), 201


# ==========================================
# 5. POST: Submit Moderation Report
# ==========================================
@api_bp.route("/reports", methods=["POST"])
def submit_report():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    target_email = data.get("targetEmail")

    target = User.query.filter_by(email=target_email).first()
    if not target:
        return jsonify({"error": "User not found"}), 404

    report = Report(
        reporter_id=user_id, reported_user_id=target.id, reason=data.get("message")
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "Report submitted to admin."}), 201


# ==========================================
# 6. GET: Student Sessions
# ==========================================
@api_bp.route("/student-sessions", methods=["GET"])
def get_student_sessions():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = MentorshipSession.query.filter_by(student_id=user_id).all()
    result = []

    for s in sessions:
        # Gracefully handle if mentor gets deleted
        mentor_name = s.mentor.full_name if s.mentor else "Unknown Mentor"
        result.append(
            {
                "id": s.id,
                "mentorId": s.mentor_id,
                "mentorName": mentor_name,
                "module": s.module,
                "date": s.date.strftime("%Y-%m-%d"),
                "time": s.time_slot,
                "status": s.status.value,
            }
        )

    return jsonify(result), 200


# ==========================================
# 7. GET: Student Feedback & Messages
# ==========================================
@api_bp.route("/student-feedback", methods=["GET"])
def get_student_feedback():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Get reviews written BY this student
    reviews = Review.query.filter_by(student_id=user_id).all()
    rev_data = [
        {
            "mentorName": r.mentor.full_name if r.mentor else "Unknown",
            "rating": r.rating,
            "text": r.review_text,
            "date": r.created_at.strftime("%Y-%m-%d"),
        }
        for r in reviews
    ]

    # Get messages sent TO this student
    msgs = Message.query.filter_by(receiver_id=user_id).all()
    msg_data = [
        {
            "id": m.id,
            "fromName": m.sender.full_name if m.sender else "System",
            "date": m.created_at.strftime("%Y-%m-%d"),
            "message": m.content,
            "rating": m.performance_rating,
        }
        for m in msgs
    ]

    return jsonify({"reviews": rev_data, "messages": msg_data}), 200


# ==========================================
# 8. GET: Search Mentors & Peers
# ==========================================
@api_bp.route("/search", methods=["GET"])
def search_users():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    search_type = request.args.get("type", "mentor")
    q = request.args.get("q", "").lower()

    results = []
    if search_type == "mentor":
        mentors = User.query.filter_by(mentor_status=MentorStatus.APPROVED).all()
        for m in mentors:
            prof = m.mentor_profile
            if prof and (
                q in m.full_name.lower()
                or q in prof.modules.lower()
                or q in prof.faculty.lower()
            ):
                results.append(
                    {
                        "id": m.id,
                        "name": m.full_name,
                        "faculty": prof.faculty,
                        "modules": prof.modules,
                        "awards": prof.awards,
                    }
                )
    else:
        # Use filter_by to keep Pylance happy
        students = User.query.filter_by(campus_role=CampusRole.STUDENT).all()
        for s in students:
            # Exclude the current user!
            if s.id == user_id:
                continue

            prof = s.student_profile
            if prof and (q in s.full_name.lower() or q in prof.degree_program.lower()):
                results.append(
                    {"id": s.id, "name": s.full_name, "program": prof.degree_program}
                )

    return jsonify(results), 200


# ==========================================
# 9. GET: Specific Mentor Availability
# ==========================================
@api_bp.route("/mentor-availability/<int:mentor_id>", methods=["GET"])
def get_mentor_avail(mentor_id):
    # Only pull slots that are NOT booked yet
    avails = Availability.query.filter_by(mentor_id=mentor_id, is_booked=False).all()
    avail_dict = {}

    for a in avails:
        d_str = a.date.strftime("%Y-%m-%d")
        if d_str not in avail_dict:
            avail_dict[d_str] = []
        avail_dict[d_str].append(a.time_slot)

    return jsonify(avail_dict), 200


# ==========================================
# 10. POST: Book a Session & Submit Review
# ==========================================
@api_bp.route("/book-session", methods=["POST"])
def book_session():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    mentor_id = data.get("mentorId")
    date_str = data.get("date")
    time_slot = data.get("time")

    # 1. Create the session
    new_session = MentorshipSession(
        mentor_id=mentor_id,
        student_id=user_id,
        date=date_str,
        time_slot=time_slot,
        module=data.get("module", "General Support"),
    )
    db.session.add(new_session)

    # 2. Mark the availability slot as booked
    avail = Availability.query.filter_by(
        mentor_id=mentor_id, date=date_str, time_slot=time_slot
    ).first()
    if avail:
        avail.is_booked = True

    # 3. Optional: Send the booking notes as a direct message
    notes = data.get("notes")
    if notes:
        msg = Message(
            sender_id=user_id, receiver_id=mentor_id, content=f"Booking Notes: {notes}"
        )
        db.session.add(msg)

    db.session.commit()
    return jsonify({"message": "Session booked successfully!"}), 201


@api_bp.route("/reviews", methods=["POST"])
def submit_review():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    rev = Review(
        student_id=user_id,
        mentor_id=data.get("mentorId"),
        rating=data.get("rating"),
        review_text=data.get("text"),
    )
    db.session.add(rev)
    db.session.commit()

    return jsonify({"message": "Review submitted successfully!"}), 201


# ==========================================
# ADMIN HELPER: Security Check
# ==========================================
def is_admin():
    user_id = get_current_user_id()
    if not user_id:
        return False
    user = User.query.get(user_id)
    return user and user.email == "Admin@dut.ac.za"


# ==========================================
# 11. GET: Admin Platform Stats & Analytics
# ==========================================
@api_bp.route("/admin/stats", methods=["GET"])
def admin_stats():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    student_count = User.query.filter_by(campus_role=CampusRole.STUDENT).count()
    mentor_count = User.query.filter_by(
        campus_role=CampusRole.STAFF, mentor_status=MentorStatus.APPROVED
    ).count()
    session_count = MentorshipSession.query.count()

    return jsonify(
        {
            "students": student_count,
            "approved_mentors": mentor_count,
            "total_sessions": session_count,
        }
    ), 200


@api_bp.route("/admin/analytics", methods=["GET"])
def admin_analytics():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    # Group by module and count the requests to feed the Chart.js graph
    results = (
        db.session.query(
            MentorshipSession.module,
            func.count(MentorshipSession.id).label("total"),  # type: ignore
        )
        .group_by(MentorshipSession.module)  # type: ignore
        .order_by(db.desc("total"))
        .limit(5)
        .all()
    )

    data = [{"module": r.module, "count": r.total} for r in results]
    return jsonify(data), 200


# ==========================================
# 12. GET: Manage Users & Pending Mentors
# ==========================================
@api_bp.route("/admin/users", methods=["GET"])
def admin_users():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    # Get everyone except the Admin
    all_users = User.query.all()
    users = [u for u in all_users if u.email != "Admin@dut.ac.za"]
    res = []
    for u in users:
        res.append(
            {
                "id": u.id,
                "name": u.full_name,
                "email": u.email,
                "role": u.campus_role.value,
                "mentor_status": u.mentor_status.value.title(),
            }
        )
    return jsonify(res), 200


@api_bp.route("/admin/pending-mentors", methods=["GET"])
def pending_mentors():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    pending = User.query.filter_by(mentor_status=MentorStatus.PENDING).all()
    res = []
    for m in pending:
        prof = m.mentor_profile
        if prof:
            res.append(
                {
                    "id": m.id,
                    "name": m.full_name,
                    "email": m.email,
                    "faculty": prof.faculty,
                    "modules": prof.modules,
                    "cvPath": prof.cv_file_path,
                    "submittedDate": m.created_at.strftime("%Y-%m-%d"),
                }
            )
    return jsonify(res), 200


# ==========================================
# 13. GET: Moderation Reports
# ==========================================
@api_bp.route("/admin/reports", methods=["GET"])
def admin_reports():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    reports = Report.query.all()
    res = []
    for r in reports:
        reporter = User.query.get(r.reporter_id)
        reported = User.query.get(r.reported_user_id)

        res.append(
            {
                "id": r.id,
                "reporterName": reporter.full_name if reporter else "Unknown",
                "reportedName": reported.full_name if reported else "Unknown",
                "reason": r.reason,
                "status": r.status.value,
                "date": r.created_at.strftime("%Y-%m-%d"),
            }
        )
    return jsonify(res), 200


# ==========================================
# 14. PUT/DELETE: Admin Actions
# ==========================================
@api_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"{user.full_name} removed from platform."}), 200


@api_bp.route("/admin/approve-mentor/<int:user_id>", methods=["PUT"])
def approve_mentor(user_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.mentor_status = MentorStatus.APPROVED
    db.session.commit()
    return jsonify({"message": "Mentor approved successfully."}), 200


@api_bp.route("/admin/reject-mentor/<int:user_id>", methods=["PUT"])
def reject_mentor(user_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.mentor_status = MentorStatus.REJECTED
    db.session.commit()
    return jsonify({"message": "Mentor application rejected."}), 200


@api_bp.route("/admin/resolve-report/<int:report_id>", methods=["PUT"])
def resolve_report(report_id):
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    report = Report.query.get(report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    report.status = ReportStatus.RESOLVED
    db.session.commit()
    return jsonify({"message": "Report resolved."}), 200
