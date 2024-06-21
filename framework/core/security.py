# framework/core/security.py
from itsdangerous import URLSafeTimedSerializer

class Security:
    def __init__(self, secret_key):
        self.serializer = URLSafeTimedSerializer(secret_key)

    def generate_csrf_token(self):
        return self.serializer.dumps({})

    def validate_csrf_token(self, token):
        try:
            self.serializer.loads(token, max_age=3600)
            return True
        except:
            return False
