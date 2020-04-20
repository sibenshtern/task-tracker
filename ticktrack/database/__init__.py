from pymodm import connect
from pymodm.errors import DoesNotExist

from ticktrack.database.models import User


mongo_uri = "mongodb+srv://application:dbapplication@ticktrackcluster-p1bgs." \
            "mongodb.net/ticktrack?retryWrites=true&w=majority"
connect(mongo_uri, alias="mongodb_app")


def return_user(user_id: int = None, email: str = None):
    try:
        if user_id is not None:
            return User.objects.get({"_id": user_id})
        elif email is not None:
            return User.objects.get({"email": email})
        else:
            raise ValueError("You don't give arguments")
    except DoesNotExist:
        return None


def create_user(email, password, name):

    def search_max_id():
        all_users = User.objects.all().values()
        return max(all_users, key=lambda user: user["_id"])["_id"]

    try:
        last_id = search_max_id()
        last_id += 1
    except DoesNotExist:
        last_id = 1
    except ValueError:
        last_id = 1

    users = User(id=last_id, email=email, name=name)
    users.set_password(password)
    users.save()
