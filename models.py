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


# ==========================================
# TABLE 1: Active Users
# ==========================================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)

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
        self, email, password_hash, campus_role, mentor_status, full_name=None
    ):
        self.email = email
        self.password_hash = password_hash
        self.campus_role = campus_role
        self.mentor_status = mentor_status
        self.full_name = full_name

    def __repr__(self):
        return f"<User {self.email} | Role: {self.campus_role.value} | Mentor: {self.mentor_status.value}>"


# ==========================================
# TABLE 2: Mentor Profiles & Applications
# ==========================================
class MentorProfile(db.Model):
    __tablename__ = "mentor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    # Application Fields (Filled out when status is 'pending')
    motivation = db.Column(db.Text, nullable=True)
    subjects_to_teach = db.Column(
        db.String(255), nullable=True
    )  # e.g., "Math 101, Physics 201"
    year_of_study = db.Column(db.String(50), nullable=True)

    # Active Mentor Fields (Used on the dashboard once 'approved')
    bio = db.Column(db.Text, nullable=True)
    meeting_link = db.Column(db.String(255), nullable=True)  # Teams/Zoom link

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MentorProfile for User ID {self.user_id}>"

    def __init__(
        self,
        user_id,
        motivation,
        subjects_to_teach,
        bio=None,
        year_of_study=None,
        meeting_link=None,
    ):
        self.user_id = user_id
        self.motivation = motivation
        self.subjects_to_teach = subjects_to_teach
        self.year_of_study = year_of_study
        self.bio = bio
        self.meeting_link = meeting_link
