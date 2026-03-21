import os
import random
import shutil
from datetime import datetime, timedelta

from faker import Faker
from werkzeug.security import generate_password_hash

from app import app
from models import (
    Availability,
    CampusRole,
    MentorProfile,
    MentorshipSession,
    MentorStatus,
    Message,
    Report,
    Review,
    SessionStatus,
    StudentProfile,
    User,
    db,
)

fake = Faker()


def seed_database():
    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()

        print("🏗️  Creating all tables with NEW schema...")
        db.create_all()

        # ==========================================
        # FOLDER RESET & DUMMY FILES
        # ==========================================
        upload_dir = "uploads"
        print(f"📁 Resetting '{upload_dir}' directory...")

        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)

        cv_dir = os.path.join(upload_dir, "documents", "cvs")
        os.makedirs(cv_dir, exist_ok=True)

        dummy_cv_path = "documents/cvs/mock_cv.pdf"
        with open(os.path.join(upload_dir, dummy_cv_path), "w") as f:
            f.write("Generic Mock CV")

        print("🌱 Seeding core 'Demo' accounts...")

        # ==========================================
        # 1. CORE DEMO ACCOUNTS (Matches login.html)
        # ==========================================
        pw_student = generate_password_hash("Student1!")
        pw_mentor = generate_password_hash("Mentor1!")
        pw_admin = generate_password_hash("Admin123!")

        # Demo Student 1
        student1 = User(
            email="Student1@dut.ac.za",
            password_hash=pw_student,
            full_name="Sipho Dlamini",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )
        student1.is_profile_complete = True

        # Demo Student 2
        student2 = User(
            email="Student2@dut.ac.za",
            password_hash=pw_student,
            full_name="Nomsa Khumalo",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )
        student2.is_profile_complete = True

        # Demo Mentor
        mentor = User(
            email="Mentor@dut.ac.za",
            password_hash=pw_mentor,
            full_name="Prof. Thabo Nkosi",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.APPROVED,
        )
        mentor.is_profile_complete = True

        # Demo Admin (For future use)
        admin = User(
            email="Admin@dut.ac.za",
            password_hash=pw_admin,
            full_name="System Administrator",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.NONE,
        )

        db.session.add_all([student1, student2, mentor, admin])
        db.session.commit()

        # --- Profiles for Demo Accounts ---
        db.session.add(
            StudentProfile(
                user_id=student1.id,
                faculty="Applied Sciences",
                degree_program="BSc Computer Science",
                study_level="Undergraduate",
                year_of_study="BSc - 3rd Year",
                subjects_needing_help="Python, Calculus",
                preferred_learning_style="Visual Learner",
                bio="Passionate about technology.",
            )
        )

        db.session.add(
            StudentProfile(
                user_id=student2.id,
                faculty="Engineering & Technology",
                degree_program="BEng Electrical",
                study_level="Undergraduate",
                year_of_study="BEng - 2nd Year",
                subjects_needing_help="Physics, Circuits",
                preferred_learning_style="Auditory Learner",
            )
        )

        db.session.add(
            MentorProfile(
                user_id=mentor.id,
                modules="Mathematics, Physics, Statistics",
                faculty="Applied Sciences",
                study_level="Postgraduate",
                year_of_study="PhD / Doctorate",
                awards="Best Tutor Award 2023",
                cv_file_path=dummy_cv_path,
            )
        )
        db.session.commit()

        print("📅 Generating Dashboard Data (Sessions, Messages, Availability)...")

        # ==========================================
        # 2. DASHBOARD DATA GENERATION
        # ==========================================
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=5)
        yesterday = today - timedelta(days=1)

        # --- Availability ---
        db.session.add_all(
            [
                Availability(mentor_id=mentor.id, date=tomorrow, time_slot="09:00"),
                Availability(
                    mentor_id=mentor.id,
                    date=tomorrow,
                    time_slot="10:00",
                    is_booked=True,
                ),
                Availability(mentor_id=mentor.id, date=tomorrow, time_slot="14:00"),
                Availability(
                    mentor_id=mentor.id,
                    date=next_week,
                    time_slot="11:00",
                    is_booked=True,
                ),
            ]
        )

        # --- Sessions ---
        db.session.add_all(
            [
                # Upcoming Bookings
                MentorshipSession(
                    mentor_id=mentor.id,
                    student_id=student1.id,
                    date=tomorrow,
                    time_slot="10:00",
                    module="Mathematics",
                    status=SessionStatus.BOOKED,
                ),
                MentorshipSession(
                    mentor_id=mentor.id,
                    student_id=student2.id,
                    date=next_week,
                    time_slot="11:00",
                    module="Physics",
                    status=SessionStatus.BOOKED,
                ),
                # Past Session
                MentorshipSession(
                    mentor_id=mentor.id,
                    student_id=student1.id,
                    date=yesterday,
                    time_slot="15:00",
                    module="Statistics",
                    status=SessionStatus.COMPLETED,
                ),
                # Cancelled Session
                MentorshipSession(
                    mentor_id=mentor.id,
                    student_id=student2.id,
                    date=today,
                    time_slot="08:00",
                    module="Mathematics",
                    status=SessionStatus.CANCELLED,
                ),
            ]
        )

        # --- Messages ---
        db.session.add_all(
            [
                Message(
                    sender_id=mentor.id,
                    receiver_id=student1.id,
                    content="Focus on Chapter 5 of Calculus. Complete exercises 5.1 to 5.3.",
                    performance_rating="good",
                ),
                Message(
                    sender_id=student2.id,
                    receiver_id=mentor.id,
                    content="Thank you for the notes! Could we go over circuits next week?",
                ),
            ]
        )

        # --- Reviews & Reports ---
        db.session.add(
            Review(
                student_id=student1.id,
                mentor_id=mentor.id,
                rating=5,
                review_text="Prof. Nkosi explains things so clearly!",
            )
        )
        db.session.add(
            Report(
                reporter_id=mentor.id,
                reported_user_id=student1.id,
                reason="Student was 30 minutes late to session without notice.",
            )
        )

        db.session.commit()

        # ==========================================
        # 3. BULK GENERATION (The Crowd)
        # ==========================================
        print("🚀 Generating 40 random bulk users...")
        default_pw = generate_password_hash("password123")
        tech_subjects = [
            "Python",
            "Java",
            "Mathematics I",
            "Networking",
            "Data Structures",
        ]
        faculties = [
            "Applied Sciences",
            "Engineering & Technology",
            "Accounting & Informatics",
        ]
        prefixes = ["BSc", "BEng", "BICT"]

        for i in range(40):
            is_student = random.random() < 0.7
            new_user = User(
                email=fake.unique.email(),
                password_hash=default_pw,
                full_name=fake.name(),
                campus_role=CampusRole.STUDENT if is_student else CampusRole.STAFF,
                mentor_status=MentorStatus.NONE
                if is_student
                else MentorStatus.APPROVED,
            )
            new_user.is_profile_complete = True
            db.session.add(new_user)
            db.session.commit()

            fac_idx = random.randint(0, 2)
            if is_student:
                db.session.add(
                    StudentProfile(
                        user_id=new_user.id,
                        faculty=faculties[fac_idx],
                        degree_program=f"{prefixes[fac_idx]} in {fake.job()}",
                        study_level="Undergraduate",
                        year_of_study=f"{prefixes[fac_idx]} - 2nd Year",
                        subjects_needing_help="Networking",
                        bio=fake.sentence(),
                    )
                )
            else:
                db.session.add(
                    MentorProfile(
                        user_id=new_user.id,
                        modules="Python, Data Structures",
                        faculty=faculties[fac_idx],
                        study_level="Postgraduate",
                        year_of_study="Masters Degree",
                        cv_file_path=dummy_cv_path,
                    )
                )

        db.session.commit()
        print(
            "✅ Successfully seeded complete database with interactive Dashboard content!"
        )


if __name__ == "__main__":
    seed_database()
