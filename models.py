import enum
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy (we will bind it to the app later)
db = SQLAlchemy()


# Define our Enums for clean, restricted data choices
class CampusRole(enum.Enum):
    STUDENT = "student"
    STAFF = "staff"


class MentorStatus(enum.Enum):
    NONE = "none"  # Has not applied
    PENDING = "pending"  # Submitted application, waiting for admin
    APPROVED = "approved"  # Can access mentor dashboard
    REJECTED = "rejected"  # Denied


class SessionStatus(enum.Enum):
    PENDING = "pending"
    BOOKED = "booked"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReportStatus(enum.Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


# ==========================================
# TABLE 1: Active Users
# ==========================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)

    # --- NEW: Neutral Profile Picture for all users ---
    profile_picture = db.Column(
        db.String(255), nullable=True, default="default_avatar.png"
    )

    # Identity: Are they a student or staff member?
    campus_role = db.Column(db.Enum(CampusRole), nullable=False)

    # Privilege: Are they allowed to mentor? (Defaults to NONE)
    mentor_status = db.Column(
        db.Enum(MentorStatus), default=MentorStatus.NONE, nullable=False
    )

    is_profile_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: Links the User to their Mentor Profile
    mentor_profile = db.relationship(
        "MentorProfile", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def __init__(
        self,
        email,
        password_hash,
        campus_role,
        mentor_status,
        full_name=None,
        profile_picture="default_avatar.png",
    ):
        self.email = email
        self.password_hash = password_hash
        self.campus_role = campus_role
        self.mentor_status = mentor_status
        self.full_name = full_name
        self.profile_picture = profile_picture

    def __repr__(self):
        return f"<User {self.email} | Role: {self.campus_role.value} | Mentor: {self.mentor_status.value}>"


# TABLE 2: Mentor Profiles & Applications
class MentorProfile(db.Model):
    __tablename__ = "mentor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )

    # --- Academic Details ---
    modules = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(150), nullable=False)
    study_level = db.Column(db.String(50), nullable=False)
    year_of_study = db.Column(db.String(100), nullable=False)

    # --- Extras & Links ---
    awards = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    badges = db.Column(db.String(255), nullable=True, default="")

    # --- Mandatory File ---
    cv_file_path = db.Column(db.String(255), nullable=False)

    def __init__(
        self,
        user_id,
        modules,
        faculty,
        study_level,
        year_of_study,
        cv_file_path,
        awards=None,
        linkedin_url=None,
        portfolio_url=None,
        badges=None,  # <-- ADD THIS
    ):
        self.user_id = user_id
        self.modules = modules
        self.faculty = faculty
        self.study_level = study_level
        self.year_of_study = year_of_study
        self.cv_file_path = cv_file_path
        self.awards = awards
        self.linkedin_url = linkedin_url
        self.portfolio_url = portfolio_url

        # Only assign it if a value was actually passed
        if badges is not None:
            self.badges = badges


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )

    # --- Academic Context ---
    faculty = db.Column(db.String(150), nullable=False)
    degree_program = db.Column(db.String(150), nullable=False)
    study_level = db.Column(db.String(50), nullable=False)
    year_of_study = db.Column(db.String(100), nullable=False)

    # --- Matchmaking Data ---
    subjects_needing_help = db.Column(db.String(255), nullable=False)
    preferred_learning_style = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    user = db.relationship("User", backref=db.backref("student_profile", uselist=False))

    # --- Timestamps ---
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __init__(
        self,
        user_id,
        faculty,
        degree_program,  # <-- This was missing!
        study_level,
        year_of_study,
        subjects_needing_help,
        preferred_learning_style=None,
        bio=None,
    ):
        self.user_id = user_id
        self.faculty = faculty
        self.degree_program = degree_program  # <-- And this!
        self.study_level = study_level
        self.year_of_study = year_of_study
        self.subjects_needing_help = subjects_needing_help
        self.preferred_learning_style = preferred_learning_style
        self.bio = bio


# ==========================================
# TABLE 4: Mentor Availability
# ==========================================
class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Store date as a string (YYYY-MM-DD) or Date object. Date object is better for sorting.
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(10), nullable=False)  # e.g., '10:00'
    is_booked = db.Column(db.Boolean, default=False)

    # Relationship to easily pull a mentor's user data
    mentor = db.relationship("User", foreign_keys=[mentor_id], backref="availabilities")

    def __init__(self, mentor_id, date, time_slot, is_booked=False):
        self.mentor_id = mentor_id
        self.date = date
        self.time_slot = time_slot
        self.is_booked = is_booked


# ==========================================
# TABLE 5: Mentorship Sessions (Bookings) -> THE NEW HUB
# ==========================================
class MentorshipSession(db.Model):
    __tablename__ = "mentorship_sessions"

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(10), nullable=False)
    module = db.Column(
        db.String(150), nullable=False
    )  # What subject are they studying?

    status = db.Column(
        db.Enum(SessionStatus), default=SessionStatus.BOOKED, nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships to easily pull user data for the dashboard cards
    mentor = db.relationship(
        "User", foreign_keys=[mentor_id], backref="sessions_as_mentor"
    )
    student = db.relationship(
        "User", foreign_keys=[student_id], backref="sessions_as_student"
    )

    # --- NEW: Workspace Relationships ---
    messages = db.relationship(
        "Message", backref="session", cascade="all, delete-orphan", lazy=True
    )
    review = db.relationship(
        "Review", backref="session", uselist=False, cascade="all, delete-orphan"
    )
    documents = db.relationship(
        "SessionDocument", backref="session", cascade="all, delete-orphan", lazy=True
    )
    reports = db.relationship(
        "Report", backref="session", cascade="all, delete-orphan", lazy=True
    )

    def __init__(
        self,
        mentor_id,
        student_id,
        date,
        time_slot,
        module,
        status=SessionStatus.BOOKED,
    ):
        self.mentor_id = mentor_id
        self.student_id = student_id
        self.date = date
        self.time_slot = time_slot
        self.module = module
        self.status = status


# ==========================================
# NEW TABLE: Session Documents
# ==========================================
class SessionDocument(db.Model):
    __tablename__ = "session_documents"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer, db.ForeignKey("mentorship_sessions.id"), nullable=False
    )
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploader = db.relationship("User", foreign_keys=[uploader_id])

    def __init__(self, session_id, uploader_id, file_name, file_path):
        self.session_id = session_id
        self.uploader_id = uploader_id
        self.file_name = file_name
        self.file_path = file_path


# ==========================================
# TABLE 6: Messages & Feedback Notes
# ==========================================
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    # --- NEW: Ties the message directly to a meeting ---
    session_id = db.Column(
        db.Integer, db.ForeignKey("mentorship_sessions.id"), nullable=False
    )

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)
    performance_rating = db.Column(
        db.String(50), nullable=True
    )  # e.g. "excellent", "good", "attention"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_messages"
    )

    def __init__(
        self, session_id, sender_id, receiver_id, content, performance_rating=None
    ):
        self.session_id = session_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.performance_rating = performance_rating


# ==========================================
# TABLE 7: Mentor Reviews
# ==========================================
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    # --- NEW: Forces 1 Review per Booking ---
    session_id = db.Column(
        db.Integer, db.ForeignKey("mentorship_sessions.id"), nullable=False, unique=True
    )

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # 1 to 5 stars
    review_text = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, session_id, student_id, mentor_id, rating, review_text=None):
        self.session_id = session_id
        self.student_id = student_id
        self.mentor_id = mentor_id
        self.rating = rating
        self.review_text = review_text


# ==========================================
# TABLE 8: Moderation Reports
# ==========================================
class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    # --- NEW: Contextualizes the report to a specific meeting ---
    session_id = db.Column(
        db.Integer, db.ForeignKey("mentorship_sessions.id"), nullable=True
    )

    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    reason = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, reporter_id, reported_user_id, reason, session_id=None):
        self.reporter_id = reporter_id
        self.reported_user_id = reported_user_id
        self.reason = reason
        self.session_id = session_id
