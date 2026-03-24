import sqlite3

# Connect directly to SQLite to bypass SQLAlchemy's strict rules
conn = sqlite3.connect("studysphere.db")
c = conn.cursor()

# Convert all bad lowercase strings to the uppercase Enum names SQLAlchemy expects
c.execute(
    "UPDATE mentorship_sessions SET status = 'CANCELLED' WHERE status = 'cancelled'"
)
c.execute("UPDATE mentorship_sessions SET status = 'BOOKED' WHERE status = 'booked'")
c.execute(
    "UPDATE mentorship_sessions SET status = 'COMPLETED' WHERE status = 'completed'"
)
c.execute(
    "UPDATE mentorship_sessions SET status = 'IN_PROGRESS' WHERE status = 'in-progress'"
)

conn.commit()
conn.close()
print("✅ Database repaired! All statuses conform to Enums.")
