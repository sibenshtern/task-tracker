from datetime import date
from typing import List, Optional

import jwt
from flask import current_app

from . import create_session, models


class UserUtils:

    def __init__(self, database_session):
        self.session = database_session

    def create_user(self, email: str, name: str, password: str) -> models.User:
        user = models.User(email=email, name=name)
        user.set_password(password)
        user.generate_apikey()

        self.session.add(user)
        self.session.commit()

        return user

    def get_user(self, **kwargs) -> Optional[models.User]:
        if kwargs.get('user_id') is not None:
            return self.session.query(models.User).get(kwargs.get('user_id'))
        elif kwargs.get('email') is not None:
            return self.session.query(models.User).filter(
                models.User.email == kwargs.get('email')
            ).first()
        elif kwargs.get('apikey') is not None:
            return self.session.query(models.User).filter(
                models.User.apikey == kwargs.get('apikey')
            ).first()
        else:
            raise ValueError("You don't give any keywords arguments")

    @staticmethod
    def generate_jwt_token(payloads: dict) -> str:
        """

        :param payloads: Словарь с полезной информацией
        :return: Токен, в котором зашифрована полезная информация из
        payloads
        """

        jwt_token = jwt.encode(
            payloads, current_app.secret_key, algorithm="HS256"
        )
        return jwt_token

    def verify_jwt_token(self, token: str) -> Optional[models.User]:
        """

        :param token: JSON Web Token
        :return: пользователя по id, которое зашифровано в token
        """
        try:
            payloads = jwt.decode(
                token, current_app.secret_key, algoritms=["HS256"]
            )
        except Exception as error:
            print(error)
            return None

        action_from_payloads = payloads.get('action')
        if action_from_payloads is not None:
            if action_from_payloads.startswith("reset_password"):
                user_id = payloads.get("user_id")
            elif action_from_payloads.startswith("verify_account"):
                user_id = payloads.get("user_id")
            else:
                raise Exception("Wrong action")

            user = self.get_user(user_id=user_id)
        else:
            raise Exception("Action is undefined")

        return user


class TasksUtils:

    def __init__(self, database_session):
        self.session = database_session

    def create_task(
            self, user_id: int, title: str, labels: List[models.Label],
            finish_date: Optional[date] = None) -> models.Task:
        task = models.Task(user_id=user_id, title=title)

        if finish_date is not None:
            task.finish_date = finish_date

        task.labels.extend(labels)
        self.session.add(task)
        self.session.commit()

        return task

    def get_task(self, user_id: int, task_id: int) -> Optional[models.Task]:
        return self.session.query(models.Task).filter(
            models.Task.id == task_id, models.Task.user_id == user_id
        ).first()

    def delete_task(self, user_id: int, task_id: int) -> None:
        task = self.session.query(models.Task).filter(
            models.Task.id == task_id, models.Task.user_id == user_id
        ).first()

        if task is not None:
            self.session.delete(task)

        self.session.commit()

    def get_tasks_for_today(self, user_id: int) -> Optional[List[models.Task]]:
        return self.session.query(models.Task).filter(
            models.Task.user_id == user_id,
            models.Task.finish_date == date.today()
        ).all()

    def get_tasks(self, user_id: int) -> Optional[List[models.Task]]:
        return self.session.query(models.Task).filter(
            models.Task.user_id == user_id
        ).all()


class LabelsUtils:

    def __init__(self, database_session):
        self.session = database_session

    def create_label(self, user_id: int, title: str) -> None:
        label = models.Label(user_id=user_id, title=title)
        self.session.add(label)
        self.session.commit()

    def get_label(self, user_id: int, **kwargs) -> Optional[models.Label]:
        if kwargs.get('label_id') is not None:
            return self.session.query(models.Label).filter(
                models.Label.id == kwargs.get('label_id'),
                models.Label.user_id == user_id
            ).first()
        elif kwargs.get('title') is not None:
            return self.session.query(models.Label).filter(
                models.Label.title == kwargs.get('title'),
                models.Label.user_id == user_id
            ).first()
        else:
            raise Exception("You don't give any keywords arguments")
    
    def get_labels(self, user_id: int) -> Optional[List[models.Label]]:
        return self.session.query(models.Label).filter(
            models.Label.user_id == user_id
        ).all()

    def delete_label(self, user_id: int, **kwargs) -> None:
        if kwargs.get('label_id') is not None:
            label = self.get_label(user_id, label_id=kwargs.get('label_id'))
        elif kwargs.get('title') is not None:
            label = self.get_label(user_id, title=kwargs.get('title'))
        else:
            raise Exception("You don't give any arguments")

        self.session.delete(label)
        self.session.commit()


session = create_session()
users_utils = UserUtils(session)
tasks_utils = TasksUtils(session)
labels_utils = LabelsUtils(session)




