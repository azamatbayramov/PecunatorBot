from firebase_admin import db
import datetime


class Group:
    def __init__(self, group_id, group_name):
        self.group_id = str(group_id)
        self.group_name = group_name

        self.ref = db.reference(f"groups/{group_id}")
        self.users_ref = self.ref.child("users")

        self.init_group_in_db()

    # Initialization
    def init_group_in_db(self):
        if not self.is_initialized_in_db():
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

    def is_initialized_in_db(self):
        return self.get_group_info() is not None

    # Group info
    def create_group_info_in_db(self):
        return self.ref.set(
            {"group_info": {"creation_datetime": datetime.datetime.now().timestamp(),
                            "group_name": self.group_name,
                            "total_balance": 0
                            }}
        )

    def get_group_info(self):
        return self.ref.child("group_info").get()

    def get_total_balance(self):
        return self.ref.child("group_info/total_balance").get()

    # Users
    def add_user(self, user_id, username=None):
        self.users_ref.child(user_id).set({"username": username, "balance": 0})

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
        return self.users_ref.get()

    # Operations
    def get_operations(self):
        return self.ref.child("operations").get()
