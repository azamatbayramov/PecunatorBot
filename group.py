from firebase_admin import db
import datetime


class Group:
    def __init__(self, groupId):
        self.groupId = groupId

        self.ref = db.reference(f"groups/{groupId}")
        self.users_ref = self.ref.child("users")

    def init_group(self):
        if not self.is_initialized():
            self.create_groupInfo_in_db()
            return {
                "result": True,
                "message": "Group has been initialized"
            }

        else:
            return {
                "result": False,
                "message": "Group has already been already initialized"
            }

    def is_initialized(self):
        return self.get_group_info() is not None

    def create_groupInfo_in_db(self):
        return self.ref.set({"group_info": {"creation_date": str(datetime.datetime.now())}})

    def add_user(self, userId, username=None):
        self.users_ref.child(userId).set({"user_id": userId, "username": username, "balance": 0})

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

    def get_group_info(self):
        return self.ref.child("group_info").get()

    def get_operations(self):
        return self.ref.child("operations").get()
