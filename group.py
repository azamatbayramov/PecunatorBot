import datetime as dt
from typing import NamedTuple

from firebase_admin import db

from user import User


class GroupInfo(NamedTuple):
    group_name: str
    creation_date: int
    total_balance: int


class Group:
    def __init__(self, group_id: str, group_name: str):
        self.id = group_id
        self.name = group_name

        self.ref = db.reference(f"groups/{group_id}")
        self.users_ref = self.ref.child("users")
        self.operations_ref = self.ref.child("operations")

    # Initialization
    def init_in_db(self) -> None:
        self.create_group_info_in_db()
        # We need this as a function because
        # we might have to init more stuff later

    def exists(self) -> bool:
        return self.ref.child("group_info").get() is not None

    # Group info
    def create_group_info_in_db(self) -> None:
        return self.ref.set(
            {"group_info": {"creation_datetime": dt.datetime.now().timestamp(),
                            "group_name": self.name,
                            "total_balance": 0
                            }}
        )

    def get_group_info(self) -> GroupInfo:
        # КаааК кастить типы, я не понимаююю!
        # Пол часа гуглил
        return self.ref.child("group_info").get()

    def get_total_balance(self) -> int:
        return int(self.ref.child("group_info/total_balance").get())

    def edit_total_balance(self, diff: int) -> int:
        current_balance = self.get_total_balance()
        self.ref.child("group_info").update({"total_balance": current_balance + diff})

        return current_balance + diff

    def reset_total_balance(self):
        self.ref.child("group_info").update({"total_balance": 0})

    # Users
    def add_user(self, user: User) -> None:
        self.users_ref.child(user.id).set({
            "username": user.username,
            "balance": 0
        })

    def delete_user(self, user: User) -> None:
        self.users_ref.child(user.id).set({})

    def edit_username(self, user: User) -> None:
        self.users_ref.child(user.id).update({
            "username": user.username
        })

    def edit_user_balance(self, user: User, diff: int) -> None:
        current_balance = self.get_user(user)["balance"]
        self.users_ref.child(user.id).update({"balance": current_balance + diff})

    def get_user(self, user: User):
        return self.users_ref.child(user.id).get()

    def get_users(self):
        return self.users_ref.get()

    def reset_user_balance(self, user: User) -> None:
        self.users_ref.child(user.id).update({
            "balance": 0
        })

    # Operations
    def get_operations(self):
        return self.operations_ref.get()

    def add_operation(self, d):
        self.operations_ref.push(d)

    def add_payment(self, author, amount, label):
        self.add_operation({
            "type": "payment",
            "author": author.id,
            "datetime": dt.datetime.now().timestamp(),
            "is_discarded": False,
            "amount": amount,
            "label": label
        })

    def add_reset(self, author):
        snapshot = dict()

        users = self.get_users()

        for user_id in users.keys():
            snapshot[user_id] = users[user_id]["balance"]

        self.add_operation({
            "type": "reset",
            "author": author.id,
            "datetime": dt.datetime.now().timestamp(),
            "is_discarded": False,
            "snapshot": snapshot,
        })
