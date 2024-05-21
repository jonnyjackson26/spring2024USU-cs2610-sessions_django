from .models import User

def isValidEmail(email):
    if "@" in email:
        if not User.objects.filter(email=email).exists():
            return True
    return False

def isValidPassword(pw):
    if len(pw)>8:
        return any(char.isdigit() for char in pw)
