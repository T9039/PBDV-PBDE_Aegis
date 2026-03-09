from werkzeug.security import generate_password_hash

from app import app
from models import CampusRole, MentorProfile, MentorStatus, User, db


def seed_database():
    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()

        print("🏗️  Rebuilding tables from models.py...")
        db.create_all()

        print("🌱 Seeding database with dummy users...")

        # ==========================================
        # 1. CREATE USERS
        # ==========================================

        # --- The Original 2 Users ---
        student1 = User(
            email="22012345@dut4life.ac.za",
            password_hash=generate_password_hash("password123"),
            full_name="Original Student",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )
        staff1 = User(
            email="alex@dut.ac.za",
            password_hash=generate_password_hash("admin"),
            full_name="Alex Admin",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.APPROVED,  # Approved Mentor
        )

        # --- The 3 New Students ---
        student2 = User(
            email="22100001@dut4life.ac.za",
            password_hash=generate_password_hash("password123"),
            full_name="Sarah Connor",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )
        student3 = User(
            email="22100002@dut4life.ac.za",
            password_hash=generate_password_hash("password123"),
            full_name="John Doe",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )
        student4 = User(
            email="22100003@dut4life.ac.za",
            password_hash=generate_password_hash("password123"),
            full_name="Emily PeerTutor",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.APPROVED,  # Student who is also an approved mentor!
        )

        # --- The 2 New Staff ---
        staff2 = User(
            email="dr.smith@dut.ac.za",
            password_hash=generate_password_hash("staff_alan"),
            full_name="Dr. Alan Smith",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.PENDING,  # Applied, waiting for approval
        )
        staff3 = User(
            email="prof.jones@dut.ac.za",
            password_hash=generate_password_hash("staff_indiana"),
            full_name="Prof. Indiana Jones",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.NONE,  # Just a regular staff member, hasn't applied
        )

        # Add all users to the session and commit to generate their IDs
        users = [student1, staff1, student2, student3, student4, staff2, staff3]
        db.session.add_all(users)
        db.session.commit()

        # ==========================================
        # 2. CREATE MENTOR PROFILES
        # ==========================================

        # Profile for Alex (Staff Mentor)
        profile_alex = MentorProfile(
            user_id=staff1.id,
            motivation="I want to help students pass.",
            subjects_to_teach="Computer Science 101, Web Development",
            bio="Experienced developer and IT lecturer.",
            meeting_link="https://teams.microsoft.com/l/meetup-join/...",
        )

        # Profile for Emily (Student Peer Tutor)
        profile_emily = MentorProfile(
            user_id=student4.id,
            motivation="I did really well in Math and want to help others.",
            subjects_to_teach="Mathematics I",
            year_of_study="3rd Year",
            bio="Third-year ICT student who loves calculus. I explain things simply!",
            meeting_link="https://zoom.us/j/123456789",
        )

        # Profile for Dr. Smith (Pending Staff Mentor)
        profile_smith = MentorProfile(
            user_id=staff2.id,
            motivation="Setting up my digital office hours for the semester.",
            subjects_to_teach="Information Systems 201",
        )

        db.session.add_all([profile_alex, profile_emily, profile_smith])
        db.session.commit()

        print("✅ Successfully seeded 4 Students and 3 Staff members!")


if __name__ == "__main__":
    seed_database()
