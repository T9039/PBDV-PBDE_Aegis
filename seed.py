import os
import shutil

from werkzeug.security import generate_password_hash

from app import app
from models import CampusRole, MentorProfile, MentorStatus, User, db


def seed_database():
    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()

    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()

        print("Creating all tables...")
        db.create_all()

        # --- NEW: WIPE AND RESET UPLOADS FOLDER ---
        upload_dir = "uploads"
        print(f"Resetting '{upload_dir}' directory...")

        # 1. Delete the entire folder and everything inside it
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)

        # 2. Recreate the core folder structure we decided on
        cv_dir = os.path.join(upload_dir, "documents", "cvs")
        transcript_dir = os.path.join(upload_dir, "documents", "transcripts")
        os.makedirs(cv_dir, exist_ok=True)
        os.makedirs(transcript_dir, exist_ok=True)

        # 3. Create actual dummy PDF files for our seed data so the UI doesn't break
        dummy_cv_path_alex = "documents/cvs/staff_1_mock_cv.pdf"
        dummy_cv_path_emily = "documents/cvs/student_4_mock_cv.pdf"
        dummy_transcript_path_emily = (
            "documents/transcripts/student_4_mock_transcript.pdf"
        )

        # Write a tiny bit of text into these files so they physically exist on your hard drive
        with open(os.path.join(upload_dir, dummy_cv_path_alex), "w") as f:
            f.write("Mock CV for Alex")
        with open(os.path.join(upload_dir, dummy_cv_path_emily), "w") as f:
            f.write("Mock CV for Emily")
        with open(os.path.join(upload_dir, dummy_transcript_path_emily), "w") as f:
            f.write("Mock Transcript for Emily")
        # ------------------------------------------

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
            experience="5 years of industry experience building web applications.",
            motivation="I want to help students pass and bridge the gap between theory and practice.",
            subjects="Computer Science 101, Web Development",
            linkedin_url="https://linkedin.com/in/alex-mock",
            certifications="AWS Certified Developer, CompTIA Security+",
            cv_file_path=dummy_cv_path_alex,
            bio="Experienced developer and IT lecturer.",
            year_of_study="Staff",
        )

        # Profile for Emily (Student Peer Tutor)
        profile_emily = MentorProfile(
            user_id=student4.id,
            experience="Achieved 90% in Math I, informally tutored high school math for 2 years.",
            motivation="I did really well in Math and want to help others succeed.",
            subjects="Mathematics I",
            linkedin_url="https://linkedin.com/in/emily-mock",
            certifications="None",
            cv_file_path=dummy_cv_path_emily,
            transcript_file_path="uploads/mock_emily_transcript.pdf",
            bio="Third-year ICT student who loves calculus. I explain things simply!",
            year_of_study="3rd Year",
        )

        # Profile for Dr. Smith (Pending Staff Mentor)
        profile_smith = MentorProfile(
            user_id=staff2.id,
            experience="15 years teaching Information Systems. Published 3 papers on database architecture.",
            motivation="Setting up my digital office hours for the semester.",
            subjects="Information Systems 201",
            linkedin_url="https://linkedin.com/in/dr-smith-mock",
            certifications="Ph.D. in Computer Science",
            cv_file_path="uploads/mock_smith_cv.pdf",
        )

        db.session.add_all([profile_alex, profile_emily, profile_smith])
        db.session.commit()

        print("✅ Successfully seeded 4 Students and 3 Staff members!")


if __name__ == "__main__":
    seed_database()
