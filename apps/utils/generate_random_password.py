import secrets
import string

def generate_random_password(length=12):
    """Generate a secure, user-friendly random password."""
    
    friendly_symbols = "!@#$%^&*-_+="
    alphabet = string.ascii_letters + string.digits + friendly_symbols

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in friendly_symbols for c in password)):
            return password
