# framework/core/auth.py
from werkzeug.security import generate_password_hash, check_password_hash

class Auth:
    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
