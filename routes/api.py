from datetime import date, datetime

from flask import Blueprint, jsonify, request, session
from sqlalchemy import func, text
from werkzeug.utils import secure_filename

from models import (
    Availability,
    CampusRole,
    MentorshipSession,
    MentorStatus,
    Message,
    Report,
    ReportStatus,
    Review,
    SessionDocument,
    SessionStatus,
    StudentProfile,
    User,
    db,
)
from utils import (  # Ensure this is imported at the top!
    get_year_value,
    save_uploaded_file,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def get_current_user_id():
    return session.get("user_id")


# 1. GET: Mentor Sessions
@api_bp.route("/sessions", methods=["GET"])
def get_sessions():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = (
        MentorshipSession.query.filter_by(mentor_id=user_id)
        .order_by(text("date ASC, time_slot ASC"))
        .all()
    )

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
# PROFILE UPDATES
# ==========================================


@api_bp.route("/mentor-profile", methods=["PUT"])
def update_mentor_profile():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user = User.query.get(user_id)

    if not user or user.campus_role != CampusRole.STAFF:
        return jsonify({"error": "Invalid user or role."}), 403

    # Update User table
    if "full_name" in data:
        user.full_name = data["full_name"]

    # Update MentorProfile table
    profile = user.mentor_profile
    if profile:
        if "modules" in data:
            profile.modules = data["modules"]
        if "faculty" in data:
            profile.faculty = data["faculty"]
        if "awards" in data:
            profile.awards = data["awards"]

    from models import db

    db.session.commit()

    return jsonify({"message": "Mentor profile updated successfully!"}), 200


@api_bp.route("/student-profile", methods=["PUT"])
def update_student_profile():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user = User.query.get(user_id)

    if not user or user.campus_role != CampusRole.STUDENT:
        return jsonify({"error": "Invalid user or role."}), 403

    # Update User table
    if "full_name" in data:
        user.full_name = data["full_name"]

    # Update StudentProfile table
    profile = user.student_profile
    if profile:
        if "subjects" in data:
            profile.subjects_needing_help = data["subjects"]
        if "bio" in data:
            profile.bio = data["bio"]

    from models import db

    db.session.commit()

    return jsonify({"message": "Student profile updated successfully!"}), 200


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


# 6. GET: Student Sessions
@api_bp.route("/student-sessions", methods=["GET"])
def get_student_sessions():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    sessions = (
        MentorshipSession.query.filter(text("student_id = :uid OR mentor_id = :uid"))
        .params(uid=user_id)
        .order_by(text("date ASC, time_slot ASC"))
        .all()
    )

    result = []

    for s in sessions:
        # Figure out who the "other person" in the workspace is
        is_student_role = s.student_id == user_id
        other_user = s.mentor if is_student_role else s.student
        other_name = other_user.full_name if other_user else "Unknown User"

        result.append(
            {
                "id": s.id,
                "mentorId": other_user.id if other_user else None,
                "mentorName": other_name,  # We keep this key so your frontend JS doesn't break!
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

    # --- NEW: Manually look up the mentor using their ID ---
    rev_data = []
    for r in reviews:
        mentor = User.query.get(r.mentor_id)
        rev_data.append(
            {
                "mentorName": mentor.full_name if mentor else "Unknown",
                "rating": r.rating,
                "text": r.review_text,
                "date": r.created_at.strftime("%Y-%m-%d"),
            }
        )
    # -------------------------------------------------------

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


# 8. GET: Search Mentors & Peers
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
                reviews = Review.query.filter_by(mentor_id=m.id).all()
                review_count = len(reviews)
                avg_rating = (
                    sum(r.rating for r in reviews) / review_count
                    if review_count > 0
                    else 0
                )
                badges = (
                    [b.strip() for b in prof.badges.split(",")] if prof.badges else []
                )

                results.append(
                    {
                        "id": m.id,
                        "name": m.full_name,
                        "faculty": prof.faculty,
                        "modules": prof.modules,
                        "awards": prof.awards,
                        "rating": round(avg_rating, 1),
                        "reviewCount": review_count,
                        "badges": badges,
                        "profilePicture": m.profile_picture,  # <-- FIXED: Added this!
                    }
                )
    else:
        students = User.query.filter_by(campus_role=CampusRole.STUDENT).all()
        for s in students:
            if s.id == user_id:
                continue

            prof = s.student_profile
            if prof and (q in s.full_name.lower() or q in prof.degree_program.lower()):
                results.append(
                    {
                        "id": s.id,
                        "name": s.full_name,
                        "program": prof.degree_program,
                        "profilePicture": s.profile_picture,  # <-- FIXED: Added this!
                    }
                )

    return jsonify(results), 200


@api_bp.route("/connect-peer", methods=["POST"])
def connect_peer():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    peer_id = data.get("peerId")

    # 1. Check if a Peer Study workspace already exists between these two exact users
    existing = (
        MentorshipSession.query.filter(
            text(
                "module = 'Peer Study' AND ((student_id = :uid AND mentor_id = :pid) OR (student_id = :pid AND mentor_id = :uid))"
            )
        )
        .params(uid=user_id, pid=peer_id)
        .first()
    )

    if existing:
        return jsonify(
            {"message": "Workspace already exists!", "sessionId": existing.id}
        ), 200

    # 2. Create a new instant workspace!
    now = datetime.now()
    new_session = MentorshipSession(
        mentor_id=peer_id,  # We temporarily store the peer in the mentor slot
        student_id=user_id,
        date=now.date(),
        time_slot=now.strftime("%H:%M"),
        module="Peer Study",
        status=SessionStatus.BOOKED,  # Automatically open and active
    )

    from models import db

    db.session.add(new_session)
    db.session.commit()

    return jsonify(
        {"message": "Peer workspace created!", "sessionId": new_session.id}
    ), 201


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

    try:
        proper_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 1. Create the session
        new_session = MentorshipSession(
            mentor_id=mentor_id,
            student_id=user_id,
            date=proper_date,  # <-- Use the converted date here!
            time_slot=time_slot,
            module=data.get("module", "General Support"),
        )
        db.session.add(new_session)

        # --- NEW: Flush to generate the new_session.id ---
        db.session.flush()

        # 2. Mark the availability slot as booked
        # (Using proper_date here as well to keep SQLite happy)
        avail = Availability.query.filter_by(
            mentor_id=mentor_id, date=proper_date, time_slot=time_slot
        ).first()
        if avail:
            avail.is_booked = True

        # 3. Attach the notes as the very first message in the new Workspace
        notes = data.get("notes")
        if notes:
            msg = Message(
                session_id=new_session.id,
                sender_id=user_id,
                receiver_id=mentor_id,
                content=f"Booking Notes: {notes}",
            )
            db.session.add(msg)

        db.session.commit()
        return jsonify({"message": "Session booked successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error booking session: {e}")
        return jsonify({"error": "Failed to book session."}), 500


@api_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
def cancel_session(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # 1. Find the session
        session = MentorshipSession.query.get(session_id)
        if not session:
            return jsonify({"error": "Session not found."}), 404

        # Security Check: Only allow the mentor or student involved to cancel it
        if session.student_id != user_id and session.mentor_id != user_id:
            return jsonify({"error": "Unauthorized to cancel this session."}), 403

        # 2. Update the session status to the strict Enum
        session.status = SessionStatus.CANCELLED

        # 3. Free up the mentor's availability slot!
        avail = Availability.query.filter_by(
            mentor_id=session.mentor_id, date=session.date, time_slot=session.time_slot
        ).first()

        if avail:
            avail.is_booked = False

        db.session.commit()
        return jsonify({"message": "Session cancelled successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error cancelling session: {e}")
        return jsonify({"error": "A server error occurred while cancelling."}), 500


# ==========================================
# GET: Load the Session Workspace
# ==========================================
@api_bp.route("/workspace/<int:session_id>", methods=["GET"])
def get_workspace(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # 1. Fetch the specific booking
    session = MentorshipSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    # 2. Security Check: Only the student or mentor in THIS session can view it
    if user_id not in [session.student_id, session.mentor_id]:
        return jsonify(
            {"error": "You do not have permission to view this workspace."}
        ), 403

    # 3. Figure out who the "other person" is for the UI header
    is_student = user_id == session.student_id
    other_user = session.mentor if is_student else session.student

    # 4. Format the Chat History
    # We order by created_at so the oldest messages are at the top, newest at the bottom
    messages = (
        Message.query.filter_by(session_id=session_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    msg_data = []
    for m in messages:
        msg_data.append(
            {
                "id": m.id,
                "senderId": m.sender_id,
                "senderName": m.sender.full_name,
                "senderAvatar": m.sender.profile_picture,
                "content": m.content,
                "timestamp": m.created_at.strftime("%I:%M %p"),  # E.g., "02:30 PM"
                "rating": m.performance_rating,
            }
        )

    # 5. Check if a review exists for this session
    review_data = None
    if session.review:
        review_data = {
            "rating": session.review.rating,
            "text": session.review.review_text,
            "date": session.review.created_at.strftime("%Y-%m-%d"),
        }

    # 5. Check if a review exists for this session
    review_data = None
    if session.review:
        review_data = {
            "rating": session.review.rating,
            "text": session.review.review_text,
            "date": session.review.created_at.strftime("%Y-%m-%d"),
        }

    # ==========================================
    # --- NEW: Fetch Shared Documents ---
    # ==========================================
    docs = (
        SessionDocument.query.filter_by(session_id=session_id)
        .order_by(SessionDocument.uploaded_at.desc())
        .all()
    )
    doc_data = []
    for d in docs:
        doc_data.append(
            {
                "id": d.id,
                "fileName": d.file_name,
                "filePath": d.file_path,
                "uploaderName": d.uploader.full_name,
                "uploadedAt": d.uploaded_at.strftime(
                    "%b %d, %I:%M %p"
                ),  # e.g., "Oct 24, 02:30 PM"
            }
        )
    # ==========================================

    # 6. Return the entire Workspace Package
    return jsonify(
        {
            "sessionDetails": {
                "id": session.id,
                "module": session.module,
                "date": session.date.strftime("%Y-%m-%d")
                if isinstance(session.date, datetime)
                else session.date,
                "time": session.time_slot,
                "status": session.status.value,
                "otherPartyName": other_user.full_name,
                "otherPartyAvatar": other_user.profile_picture,
                "otherPartyRole": "Mentor" if is_student else "Student",
            },
            "messages": msg_data,
            "review": review_data,
            "documents": doc_data,
        }
    ), 200


# ==========================================
# POST: Send a Message in the Workspace
# ==========================================
@api_bp.route("/workspace/<int:session_id>/messages", methods=["POST"])
def send_workspace_message(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    session = MentorshipSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    if user_id not in [session.student_id, session.mentor_id]:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    content = data.get("message", "").strip()
    rating = data.get("rating")  # Mentors might pass a rating, students won't

    if not content:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Determine who gets the message
    receiver_id = (
        session.mentor_id if user_id == session.student_id else session.student_id
    )

    try:
        new_msg = Message(
            session_id=session_id,
            sender_id=user_id,
            receiver_id=receiver_id,
            content=content,
            performance_rating=rating,
        )
        db.session.add(new_msg)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Message sent",
                "newMessage": {
                    "id": new_msg.id,
                    "senderId": user_id,
                    "content": content,
                    "timestamp": new_msg.created_at.strftime("%I:%M %p"),
                    "rating": rating,
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error sending message: {e}")
        return jsonify({"error": "Failed to send message."}), 500


# ==========================================
# POST: Upload a File to the Workspace
# ==========================================
@api_bp.route("/workspace/<int:session_id>/upload", methods=["POST"])
def upload_workspace_file(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    session = MentorshipSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    # Security: Only participants can upload files to this workspace
    if user_id not in [session.student_id, session.mentor_id]:
        return jsonify({"error": "Access denied."}), 403

    # Check if a file is actually in the request
    if "file" not in request.files:
        return jsonify({"error": "No file part provided."}), 400

    uploaded_file = request.files["file"]

    if not uploaded_file.filename:
        return jsonify({"error": "No file selected."}), 400

    try:
        # Use your existing utility function to securely save the file
        # We use the session_id to group files together in the directory
        saved_path = save_uploaded_file(
            file_obj=uploaded_file,
            user_id=session_id,
            user_role="workspace",
            category="documents",
            sub_category="shared",
        )

        if not saved_path:
            return jsonify({"error": "Failed to save file to server."}), 500

        safe_filename = secure_filename(str(uploaded_file.filename))

        # Save the record in the database
        new_doc = SessionDocument(
            session_id=session_id,
            uploader_id=user_id,
            file_name=safe_filename,
            file_path=saved_path,
        )
        db.session.add(new_doc)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "File uploaded successfully!",
                "document": {
                    "id": new_doc.id,
                    "fileName": new_doc.file_name,
                    "filePath": new_doc.file_path,
                    "uploaderId": user_id,
                    "uploadedAt": new_doc.uploaded_at.strftime("%I:%M %p"),
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error uploading file: {e}")
        return jsonify({"error": "A server error occurred during upload."}), 500


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


# 12. GET: Manage Users & Pending Mentors
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
# Cancel a Mentorship Session (Booking)
# ==========================================
@api_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
def cancel_mentorship_session(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # 1. Find the booked meeting in the database
    booking = MentorshipSession.query.get(session_id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # 2. Security Check: Only the student who booked it, or the mentor hosting it, can cancel it.
    if booking.student_id != user_id and booking.mentor_id != user_id:
        return jsonify(
            {"error": "You do not have permission to cancel this booking."}
        ), 403

    try:
        # 3. Change the status to cancelled instead of hard-deleting the row
        booking.status = "cancelled"
        db.session.commit()

        # (Optional) You could import send_email here and notify the other person!

        return jsonify({"message": "Booking successfully cancelled."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error cancelling booking: {e}")
        return jsonify({"error": "A server error occurred."}), 500


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


# ==========================================
# 18. GET: Admin View All Reviews
# ==========================================
@api_bp.route("/admin/all-reviews", methods=["GET"])
def admin_all_reviews():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    reviews = Review.query.order_by(Review.created_at.desc()).all()
    res = []
    for r in reviews:
        student = User.query.get(r.student_id)
        mentor = User.query.get(r.mentor_id)
        res.append(
            {
                "id": r.id,
                "studentName": student.full_name if student else "Unknown",
                "mentorName": mentor.full_name if mentor else "Unknown",
                "mentorId": mentor.id if mentor else None,  # <--- ADD THIS LINE!
                "rating": r.rating,
                "text": r.review_text,
                "date": r.created_at.strftime("%Y-%m-%d"),
            }
        )
    return jsonify(res), 200


# ==========================================
# 19. POST: Admin Award Badge
# ==========================================
@api_bp.route("/admin/award-badge", methods=["POST"])
def award_badge():
    if not is_admin():
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    mentor_id = data.get("mentorId")
    new_badge = data.get("badge")  # e.g. "Top IT Tutor"

    mentor = User.query.get(mentor_id)
    if mentor and mentor.mentor_profile:
        current_badges = mentor.mentor_profile.badges or ""
        # Append the new badge with a comma
        if current_badges:
            mentor.mentor_profile.badges = f"{current_badges}, {new_badge}"
        else:
            mentor.mentor_profile.badges = new_badge

        db.session.commit()
        return jsonify(
            {"message": f"Badge '{new_badge}' awarded to {mentor.full_name}!"}
        ), 200

    return jsonify({"error": "Mentor not found"}), 404


@api_bp.route("/recommended-mentors", methods=["GET"])
def get_recommended_mentors():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # 1. Get the current student's baseline data
    student_profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not student_profile:
        return jsonify([])

    student_year_val = get_year_value(student_profile.year_of_study)
    student_subjects = [
        s.strip().lower() for s in student_profile.subjects_needing_help.split(",")
    ]
    student_style = student_profile.preferred_learning_style

    # 2. Get all approved mentors
    approved_mentors = User.query.filter_by(mentor_status=MentorStatus.APPROVED).all()
    recommendations = []

    for mentor in approved_mentors:
        # Don't recommend the student to themselves!
        if mentor.id == user_id:
            continue

        profile = mentor.mentor_profile
        if not profile:
            continue

        score = 0

        # ==========================================
        # LEVEL 1: The Hard Filter (Seniority)
        # ==========================================
        mentor_year_val = get_year_value(profile.year_of_study)

        if mentor_year_val < student_year_val:
            continue

        # ==========================================
        # LEVEL 2: Fuzzy Module Overlap
        # ==========================================
        mentor_modules = [m.strip().lower() for m in profile.modules.split(",")]
        overlap = []

        for s_sub in student_subjects:
            for m_mod in mentor_modules:
                if (
                    s_sub in m_mod or m_mod in s_sub
                ):  # E.g., "math" matches "mathematics"
                    if m_mod not in overlap:
                        overlap.append(m_mod)

        if not overlap:
            continue  # Discard if absolutely zero module overlap

        score += len(overlap) * 10

        # ==========================================
        # LEVEL 3: The Collaborative Filter (Review Bonus)
        # ==========================================
        high_reviews = (
            Review.query.filter(text("mentor_id = :m_id AND rating >= 4"))
            .params(m_id=mentor.id)
            .all()
        )

        for review in high_reviews:
            past_student = StudentProfile.query.filter_by(
                user_id=review.student_id
            ).first()
            if past_student and past_student.preferred_learning_style == student_style:
                score += 20

        # ==========================================
        # LEVEL 4: The Availability Bonus
        # ==========================================
        has_slots = (
            Availability.query.filter(
                text("mentor_id = :m_id AND is_booked = 0 AND date >= :today")
            )
            .params(m_id=mentor.id, today=date.today())
            .first()
        )

        if has_slots:
            score += 10

        # ==========================================
        # Package the Data
        # ==========================================
        initials = (
            "".join([n[0] for n in mentor.full_name.split() if n]).upper()[:2]
            if mentor.full_name
            else "M"
        )

        # Capitalize the overlap modules nicely for the UI
        display_modules = ", ".join([mod.title() for mod in overlap])

        recommendations.append(
            {
                "mentorId": mentor.id,
                "name": mentor.full_name,
                "initials": initials,
                "profilePicture": mentor.profile_picture,
                "matchedModules": display_modules,
                "yearOfStudy": profile.year_of_study,
                "score": score,
            }
        )

    # 3. Sort by highest score, slice top 6
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    top_6 = recommendations[:6]

    return jsonify(top_6), 200


@api_bp.route("/workspace/<int:session_id>/complete", methods=["POST"])
def complete_session(session_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    session = MentorshipSession.query.get_or_404(session_id)

    # 1. Logic Check: Who is allowed to close this?
    is_mentor = session.mentor_id == user_id
    is_peer_study = session.module == "Peer Study" and (
        session.student_id == user_id or session.mentor_id == user_id
    )

    if not (is_mentor or is_peer_study):
        return jsonify(
            {"error": "Only the Mentor can mark this session as complete."}
        ), 403

    # 2. Update the status
    session.status = SessionStatus.COMPLETED
    from models import db

    db.session.commit()

    return jsonify(
        {"message": "Session marked as complete! Reviews are now unlocked."}
    ), 200
