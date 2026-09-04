import re


def validate_name(name):
    if not name.strip():
        return False, "Name cannot be empty."

    if len(name.strip()) < 2:
        return False, "Name must contain at least 2 characters."

    return True, ""


def validate_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        return False, "Please enter a valid email address."

    return True, ""


def validate_phone(phone):
    if not phone.isdigit() or len(phone) != 10:
        return False, "Phone number must contain exactly 10 digits."

    return True, ""


def validate_capacity(capacity):
    if capacity <= 0:
        return False, "Capacity must be greater than zero."

    return True, ""


def validate_credits(credits):
    if credits < 1 or credits > 6:
        return False, "Credits must be between 1 and 6."

    return True, ""