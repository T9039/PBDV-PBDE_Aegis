import random
import smtplib
import socket

from email_validator import EmailNotValidError, validate_email


# FUNCTIONS
def generate_otp():
    return str(random.randint(100000, 999999))


def send_email(to_email, subject, body):
    try:
        socket.create_connection(("smtp.mailtrap.io", 587), timeout=5)
        print("Can reach Mailtrap SMTP!")
    except Exception as e:
        print("Cannot connect to Mailtrap:", e)

    """
    Simplest option: use Gmail SMTP or Mailtrap.io (free).
    For a school project you can hardcode Mailtrap credentials.
    """
    from_email = "aa66b1448e7173"
    from_password = "370f53b9a831dc"

    try:
        with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(from_email, to_email, message)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False


def is_valid_dut_email(email: str) -> bool:
    """
    Checks if the email has valid format and DUT domain.
    """
    try:
        v = validate_email(email)
        email_normalized = v.email.lower()
        if not (
            email_normalized.endswith("@dut.ac.za")
            or email_normalized.endswith("@dut4life.ac.za")
        ):
            return False
        return True
    except EmailNotValidError:
        return False
