import random
from datetime import datetime, timedelta

from faker import Faker

from app import app
from models import (
    Availability,
    CampusRole,
    MentorshipSession,
    MentorStatus,
    Message,
    Report,
    Review,
    SessionDocument,
    SessionStatus,
    User,
    db,
)

fake = Faker()


def run_simulation():
    with app.app_context():
        print("⏳ Initiating StudySphere Time Machine...")

        # 1. Fetch Existing Users created by seed.py
        mentors = User.query.filter_by(
            campus_role=CampusRole.STAFF, mentor_status=MentorStatus.APPROVED
        ).all()
        students = User.query.filter_by(campus_role=CampusRole.STUDENT).all()

        if not mentors or not students:
            print(
                "❌ Error: Not enough users found. Please run 'python seed.py' first."
            )
            return

        print(f"👥 Found {len(mentors)} Mentors and {len(students)} Students.")
        print("🧹 Wiping old interactions (keeping users/profiles intact)...")

        # Safely wipe only the interaction tables so we can re-run this script safely
        db.session.query(Message).delete()
        db.session.query(Review).delete()
        db.session.query(Report).delete()
        db.session.query(SessionDocument).delete()
        db.session.query(MentorshipSession).delete()
        db.session.query(Availability).delete()
        db.session.commit()

        # 2. Setup the Timeline (90 Days Past, 14 Days Future)
        today = datetime.now().date()
        start_date = today - timedelta(days=90)
        end_date = today + timedelta(days=14)

        time_slots = [
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
        ]

        print(f"🗓️ Fast-forwarding activity from {start_date} to {end_date}...")

        current_date = start_date
        total_sessions = 0

        while current_date <= end_date:
            is_past = current_date < today

            # Randomly select about 30-40% of mentors to be active on any given day
            daily_mentors = random.sample(
                mentors, k=random.randint(max(1, len(mentors) // 3), len(mentors) // 2)
            )

            for mentor in daily_mentors:
                # Fallback module if profile is weirdly empty
                modules = ["General Support"]
                if mentor.mentor_profile and mentor.mentor_profile.modules:
                    modules = [
                        m.strip() for m in mentor.mentor_profile.modules.split(",")
                    ]

                # Give the mentor 2 to 4 availability slots today
                slots = random.sample(time_slots, k=random.randint(2, 4))

                for slot in slots:
                    # 65% chance the slot actually gets booked by a student
                    is_booked = random.random() < 0.65

                    avail = Availability(
                        mentor_id=mentor.id,
                        date=current_date,
                        time_slot=slot,
                        is_booked=is_booked,
                    )
                    db.session.add(avail)

                    if is_booked:
                        student = random.choice(students)

                        # Determine session status based on time
                        if is_past:
                            # 90% completed successfully, 10% cancelled
                            status = (
                                SessionStatus.COMPLETED
                                if random.random() < 0.9
                                else SessionStatus.CANCELLED
                            )
                        else:
                            status = SessionStatus.BOOKED

                        session = MentorshipSession(
                            mentor_id=mentor.id,
                            student_id=student.id,
                            date=current_date,
                            time_slot=slot,
                            module=random.choice(modules),
                            status=status,
                        )
                        db.session.add(session)
                        db.session.flush()  # Generate the ID immediately for Workspace relationships
                        total_sessions += 1

                        # --- GENERATE WORKSPACE CONTEXT ---
                        if status == SessionStatus.COMPLETED:
                            # Back-and-forth chat history
                            db.session.add(
                                Message(
                                    session_id=session.id,
                                    sender_id=student.id,
                                    receiver_id=mentor.id,
                                    content=fake.sentence(nb_words=8),
                                )
                            )
                            db.session.add(
                                Message(
                                    session_id=session.id,
                                    sender_id=mentor.id,
                                    receiver_id=student.id,
                                    content=fake.sentence(nb_words=12),
                                )
                            )
                            db.session.add(
                                Message(
                                    session_id=session.id,
                                    sender_id=mentor.id,
                                    receiver_id=student.id,
                                    content="Great session today. Here are your notes.",
                                    performance_rating=random.choice(
                                        ["good", "excellent"]
                                    ),
                                )
                            )

                            # 75% chance the student left a review
                            if random.random() < 0.75:
                                rating = random.choices(
                                    [3, 4, 5], weights=[10, 30, 60], k=1
                                )[0]
                                db.session.add(
                                    Review(
                                        session_id=session.id,
                                        student_id=student.id,
                                        mentor_id=mentor.id,
                                        rating=rating,
                                        review_text=fake.paragraph(nb_sentences=2),
                                    )
                                )

                            # 15% chance they uploaded a dummy file to the workspace
                            if random.random() < 0.15:
                                db.session.add(
                                    SessionDocument(
                                        session_id=session.id,
                                        uploader_id=mentor.id,
                                        file_name=f"study_guide_{current_date}.pdf",
                                        file_path="documents/cvs/mock_cv.pdf",
                                    )
                                )

                            # 1% chance someone was reported
                            if random.random() < 0.01:
                                db.session.add(
                                    Report(
                                        session_id=session.id,
                                        reporter_id=mentor.id,
                                        reported_user_id=student.id,
                                        reason="Student did not show up.",
                                    )
                                )

                        elif status == SessionStatus.BOOKED:
                            # Just an initial booking note from the student
                            db.session.add(
                                Message(
                                    session_id=session.id,
                                    sender_id=student.id,
                                    receiver_id=mentor.id,
                                    content=f"Booking Notes: {fake.sentence(nb_words=6)}",
                                )
                            )

            # Commit day-by-day to prevent memory crashes
            db.session.commit()
            current_date += timedelta(days=1)

        print(
            f"✅ Time Machine Complete! Fast-forwarded {total_sessions} live sessions with full workspace history."
        )


if __name__ == "__main__":
    run_simulation()
