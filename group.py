from firebase_admin import db
import datetime


class Group:
    def __init__(self, group_id):
        self.groupId = group_id

        self.ref = db.reference(f"groups/{group_id}")
        self.users_ref = self.ref.child("users")

    def init_group(self):
        if not self.is_initialized():
            self.create_group_info_in_db()
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

    def create_group_info_in_db(self):
        return self.ref.set({"group_info": {"creation_datetime": str(datetime.datetime.now())}})

    def add_user(self, user_id, username=None):
        self.users_ref.child(user_id).set({"user_id": user_id, "username": username, "balance": 0})

    def delete_user(self, user_id):
        self.users_ref.child(user_id).set({})

    def edit_username(self, user_id, username):
        self.users_ref.child(user_id).update({"username": username})

    def edit_balance(self, user_id, diff):
        current_balance = self.get_user(user_id)["balance"]
        self.users_ref.child(user_id).update({"balance": current_balance + diff})

    def get_user(self, user_id):
        return self.users_ref.child(user_id).get()

    def get_users(self):
        return self.ref.child("users").get()

    def get_group_info(self):
        return self.ref.child("group_info").get()

    def get_operations(self):
        return self.ref.child("operations").get()
