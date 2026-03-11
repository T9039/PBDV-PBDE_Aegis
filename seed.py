import os
import random
import shutil

from faker import Faker
from werkzeug.security import generate_password_hash

from app import app
from models import CampusRole, MentorProfile, MentorStatus, StudentProfile, User, db

fake = Faker()


def seed_database():
    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()

        print("🏗️  Creating all tables...")
        db.create_all()

        # ==========================================
        # FOLDER RESET & DUMMY FILES
        # ==========================================
        upload_dir = "uploads"
        print(f"📁 Resetting '{upload_dir}' directory...")

        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)

        cv_dir = os.path.join(upload_dir, "documents", "cvs")
        transcript_dir = os.path.join(upload_dir, "documents", "transcripts")
        os.makedirs(cv_dir, exist_ok=True)
        os.makedirs(transcript_dir, exist_ok=True)

        dummy_cv_path = "documents/cvs/mock_cv.pdf"
        dummy_transcript_path = "documents/transcripts/mock_transcript.pdf"

        with open(os.path.join(upload_dir, dummy_cv_path), "w") as f:
            f.write("Generic Mock CV")
        with open(os.path.join(upload_dir, dummy_transcript_path), "w") as f:
            f.write("Generic Mock Transcript")

        print("🌱 Seeding core 'Hero' testing accounts...")

        # ==========================================
        # 1. CORE TESTING ACCOUNTS (Hardcoded for easy login)
        # ==========================================
        default_pw = generate_password_hash("password123")

        # Student 1: Needs Help (Has StudentProfile)
        student1 = User(
            email="22012345@dut4life.ac.za",
            password_hash=default_pw,
            full_name="Original Student",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.NONE,
        )

        # Student 2: Peer Tutor (Has MentorProfile)
        student_tutor = User(
            email="emily@dut4life.ac.za",
            password_hash=default_pw,
            full_name="Emily PeerTutor",
            campus_role=CampusRole.STUDENT,
            mentor_status=MentorStatus.APPROVED,
        )

        # Staff 1: Approved Mentor
        staff_mentor = User(
            email="alex@dut.ac.za",
            password_hash=default_pw,
            full_name="Alex Admin",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.APPROVED,
        )

        # Staff 2: Pending Mentor
        staff_pending = User(
            email="dr.smith@dut.ac.za",
            password_hash=default_pw,
            full_name="Dr. Alan Smith",
            campus_role=CampusRole.STAFF,
            mentor_status=MentorStatus.PENDING,
        )

        db.session.add_all([student1, student_tutor, staff_mentor, staff_pending])
        db.session.commit()  # Commit to get IDs

        # Profiles for Core Accounts
        db.session.add(
            StudentProfile(
                user_id=student1.id,
                degree_program="Diploma in ICT",
                year_of_study="1st Year",
                subjects_needing_help="Python, Mathematics I",
                primary_goals="Pass my midterms",
                bio="I am a visual learner.",
            )
        )
        db.session.add(
            MentorProfile(
                user_id=staff_mentor.id,
                experience="5 years industry experience.",
                motivation="Helping students succeed.",
                subjects="Web Development, Python",
                linkedin_url="https://linkedin.com",
                certifications=None,
                cv_file_path=dummy_cv_path,
                bio="Tech lead.",
            )
        )
        db.session.add(
            MentorProfile(
                user_id=student_tutor.id,
                experience="Got 90% in Math.",
                motivation="I love teaching.",
                subjects="Mathematics I",
                certifications=None,
                linkedin_url="https://linkedin.com",
                cv_file_path=dummy_cv_path,
                transcript_file_path=dummy_transcript_path,
                bio="Math nerd!",
            )
        )
        db.session.add(
            MentorProfile(
                user_id=staff_pending.id,
                experience="10 years teaching.",
                motivation="Digital office hours.",
                certifications=None,
                linkedin_url="https://linkedin.com",
                subjects="Database Architecture",
                cv_file_path=dummy_cv_path,
            )
        )
        db.session.commit()

        # ==========================================
        # 2. BULK GENERATION (The Crowd)
        # ==========================================
        print("🚀 Generating 50 random users for the crowd...")

        tech_subjects = [
            "Python",
            "Java",
            "C++",
            "Mathematics I",
            "Web Development",
            "Database Architecture",
            "Networking",
            "Data Structures",
            "UI/UX Design",
            "Cloud Computing",
        ]
        years = ["1st Year", "2nd Year", "3rd Year", "BTech", "Honours"]
        degrees = [
            "Diploma in ICT",
            "BSc Computer Science",
            "Diploma in Engineering",
            "BCom Information Systems",
        ]

        for i in range(60):
            # 60% chance to be a student, 40% to be staff
            is_student = random.random() < 0.6
            role = CampusRole.STUDENT if is_student else CampusRole.STAFF

            # Determine mentor status based on role
            status_roll = random.random()

            if is_student:
                # Students are mostly just students (70% NONE, 15% PENDING, 15% APPROVED)
                if status_roll < 0.70:
                    m_status = MentorStatus.NONE
                elif status_roll < 0.85:
                    m_status = MentorStatus.PENDING
                else:
                    m_status = MentorStatus.APPROVED
            else:
                # Staff in this dummy data are highly likely to be mentors (20% NONE, 30% PENDING, 50% APPROVED)
                if status_roll < 0.20:
                    m_status = MentorStatus.NONE
                elif status_roll < 0.50:
                    m_status = MentorStatus.PENDING
                else:
                    m_status = MentorStatus.APPROVED

            # Create the User
            new_user = User(
                email=fake.unique.email(),
                password_hash=default_pw,
                full_name=fake.name(),
                campus_role=role,
                mentor_status=m_status,
            )
            db.session.add(new_user)
            db.session.commit()  # Commit immediately to get the ID for relationships

            # Give students their profiles
            if is_student and random.random() < 0.8:
                db.session.add(
                    StudentProfile(
                        user_id=new_user.id,
                        degree_program=random.choice(degrees),
                        year_of_study=random.choice(years),
                        subjects_needing_help=", ".join(
                            random.sample(tech_subjects, random.randint(1, 3))
                        ),
                        primary_goals=fake.sentence(),
                        bio=fake.paragraph(nb_sentences=2),
                    )
                )

            # Give mentors (both pending and approved) their profiles
            if m_status in [MentorStatus.PENDING, MentorStatus.APPROVED]:
                db.session.add(
                    MentorProfile(
                        user_id=new_user.id,
                        experience=fake.paragraph(nb_sentences=2),
                        motivation=fake.paragraph(nb_sentences=1),
                        subjects=", ".join(
                            random.sample(tech_subjects, random.randint(1, 4))
                        ),
                        linkedin_url="https://linkedin.com",
                        certifications=None,
                        cv_file_path=dummy_cv_path,
                        bio=fake.paragraph(nb_sentences=2)
                        if random.random() < 0.5
                        else None,
                        year_of_study=random.choice(years) if is_student else "Staff",
                    )
                )

        db.session.commit()
        print("✅ Successfully seeded 100+ highly diverse database entries!")


if __name__ == "__main__":
    seed_database()
