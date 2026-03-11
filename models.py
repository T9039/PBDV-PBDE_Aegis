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
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )

    # --- PUBLIC: Displayed on the Mentor Card for Students ---
    year_of_study = db.Column(db.String(255), nullable=True)
    subjects = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    experience = db.Column(
        db.Text, nullable=True
    )  # e.g., "Helped 1st-year students with Python, participated in 3 hackathons."

    # --- PRIVATE: Seen ONLY by Admins for Verification ---
    motivation = db.Column(db.Text, nullable=False)
    linkedin_url = db.Column(db.String(255), nullable=True)
    # github_url = db.Column(db.String(255), nullable=True)
    certifications = db.Column(
        db.String(255), nullable=True
    )  # e.g., "AWS Cloud Practitioner, CompTIA A+"

    # File Paths (We store the PDF file on the server and save the path here)
    cv_file_path = db.Column(db.String(255), nullable=True)
    transcript_file_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<MentorProfile for User ID {self.user_id}>"

    def __init__(
        self,
        user_id,
        experience,
        motivation,
        subjects,
        linkedin_url,
        # github_url,
        certifications,
        cv_file_path,
        transcript_file_path=None,
        bio=None,
        year_of_study=None,
    ):
        self.user_id = user_id
        self.experience = experience
        self.linkedin_url = linkedin_url
        self.certifications = certifications
        self.cv_file_path = cv_file_path
        self.transcript_file_path = transcript_file_path
        self.motivation = motivation
        self.subjects = subjects
        self.year_of_study = year_of_study
        self.bio = bio


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    # Enforce 1-to-1 relationship with the User table
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )

    # --- Academic Context ---
    # What are they studying? (e.g., "Diploma in ICT", "BSc Computer Science")
    degree_program = db.Column(db.String(150), nullable=False)
    # Helps mentors gauge the level of difficulty (e.g., "1st Year", "2nd Year")
    year_of_study = db.Column(db.String(50), nullable=False)

    # --- Matchmaking Data (The Algorithm's Bread & Butter) ---
    # Comma-separated list of what they are struggling with (e.g., "Python, Networking")
    # We will cross-reference this with the MentorProfile.subjects field!
    subjects_needing_help = db.Column(db.String(255), nullable=False)

    # What do they actually want to achieve? (e.g., "Exam Prep", "Career Advice", "Project Help")
    primary_goals = db.Column(db.String(255), nullable=True)

    # --- Personalization (For the Mentor to read) ---
    # Let them explain their situation in their own words
    bio = db.Column(db.Text, nullable=True)

    # E.g., "Visual learner", "I need hands-on coding help", "Just need concepts explained"
    preferred_learning_style = db.Column(db.String(100), nullable=True)

    # --- Timestamps ---
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationship back to the User model
    user = db.relationship("User", backref=db.backref("student_profile", uselist=False))

    def __repr__(self):
        return f"<StudentProfile for User ID {self.user_id}>"

    def __init__(
        self,
        user_id,
        degree_program,
        year_of_study,
        subjects_needing_help,
        primary_goals=None,
        bio=None,
        preferred_learning_style=None,
    ):
        self.user_id = user_id
        self.degree_program = degree_program
        self.year_of_study = year_of_study
        self.subjects_needing_help = subjects_needing_help
        self.primary_goals = primary_goals
        self.bio = bio
        self.preferred_learning_style = preferred_learning_style
