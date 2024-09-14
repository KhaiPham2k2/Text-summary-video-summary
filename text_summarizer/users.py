# users.py
from models import User

class UserManager:
    users = []

    @classmethod
    def add_user(cls, username, password):
        user = User(username, password)
        cls.users.append(user)

    @classmethod
    def validate_user(cls, username, password):
        for user in cls.users:
            if user.username == username and user.password == password:
                return True
        return False
