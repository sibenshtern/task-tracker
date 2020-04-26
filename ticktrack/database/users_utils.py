from pymodm.errors import DoesNotExist
from flask import current_app

from ticktrack.database.models import User


def search_max_id_in_users():
    try:
        all_users = User.objects.all().values()
        return max(all_users, key=lambda user: user["_id"])["_id"]
    except DoesNotExist:
        return 1
    except ValueError:
        return 1


def create_user(email: str = None, name: str = None, password: str = None):
    users = User(id=current_app.max_id, email=email, name=name)
    users.generate_apikey()
    users.set_password(password)
    users.save()

    current_app.max_id += 1


def return_user(user_id: int = None, email: str = None, apikey: str = None):
    try:
        if user_id is not None:
            return User.objects.get({'_id': user_id})
        elif email is not None:
            return User.objects.get({'email': email})
        elif apikey is not None:
            return User.objects.get({'apikey': apikey})
        else:
            raise ValueError("You don't give any arguments")
    except DoesNotExist:
        return None
