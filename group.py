from firebase_admin import db
import json
import datetime


class Group:
    def __init__(self, groupId):
        self.groupId = groupId

        self.ref = db.reference(f"groups/{groupId}")
        self.users_ref = self.ref.child("users")

    def is_initialized(self):
        if self.get_groupInfo():
            return True
        else:
            return False

    def init_in_db(self):
        return self.ref.set({"groupInfo": {"creationDate": str(datetime.datetime.now())}})

    def add_user(self, userId, username=None):
        self.users_ref.child(userId).set({"userId": userId, "username": username, "balance": 0})

    def delete_user(self, userId):
        self.users_ref.child(userId).set({})

    def edit_username(self, userId, username):
        self.users_ref.child(userId).update({"username": username})

    def edit_balance(self, userId, diff):
        current_balance = self.get_user(userId)["balance"]
        self.users_ref.child(userId).update({"balance": current_balance + diff})

    def get_user(self, userId):
        return self.users_ref.child(userId).get()

    def get_users(self):
        return self.ref.child("users").get()

    def get_groupInfo(self):
        return self.ref.child("groupInfo").get()

    def get_operations(self):
        return self.ref.child("operations").get()
