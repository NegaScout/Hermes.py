import string
import secrets

def generate_password(self):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(14))
    return password
