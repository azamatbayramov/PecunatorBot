import datetime as dt

from firebase_admin import db
from pydantic import BaseModel
from typing import Dict, Union, Optional

from user import User


class GroupInfo(BaseModel):
    group_name: str
    creation_date: int
    total_balance: int


class UserInfo(BaseModel):
    username: str
    name: Optional[str]
    balance: int


class Operation(BaseModel):
    type: str
    author: str
    datetime: int
    is_discarded: bool


class PaymentOperation(Operation):
    type = "payment"
    label: str
    amount: int


class ResetOperation(Operation):
    type = "reset"
    snapshot: Dict[str, int]


class Group:
    def __init__(self, group_id: str, group_name: str = None):
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
        return GroupInfo(**self.ref.child("group_info").get())  # TODO: Fix typing

    def get_total_balance(self) -> int:
        return int(self.ref.child("group_info/total_balance").get())  # TODO: Fix typing

    def edit_total_balance(self, diff: int) -> int:
        current_balance = self.get_total_balance()
        self.ref.child("group_info").update({
            "total_balance": current_balance + diff
        })

        return current_balance + diff

    def reset_total_balance(self) -> None:
        self.ref.child("group_info").update({
            "total_balance": 0
        })

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
        current_balance = self.get_user(user).balance
        self.users_ref.child(user.id).update({
            "balance": current_balance + diff
        })

    def get_user(self, user: User) -> UserInfo:
        data = self.users_ref.child(user.id).get()
        return None if data is None else UserInfo(**data)  # TODO: Fix typing

    def get_users(self) -> Dict[str, UserInfo]:
        data = self.users_ref.get()
        return {k: UserInfo(**v) for k, v in data.items()}  # TODO: Fix typing

    def reset_user_balance(self, user: User) -> None:
        self.users_ref.child(user.id).update({
            "balance": 0
        })

    # Operations
    def add_operation(self, d: Operation) -> None:
        self.operations_ref.push(d.dict())

    def add_payment(self, author: User, amount: int, label: str) -> None:
        self.add_operation(PaymentOperation(
            author=author.id,
            datetime=dt.datetime.now().timestamp(),
            is_discarded=False,
            amount=amount,
            label=label
        ))

    def add_reset(self, author: User) -> None:
        snapshot, users = dict(), self.get_users()
        for user_id in users.keys():
            snapshot[user_id] = users[user_id].balance

        self.add_operation(ResetOperation(
            author=author.id,
            datetime=dt.datetime.now().timestamp(),
            is_discarded=False,
            snapshot=snapshot
        ))
