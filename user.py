from firebase_admin import db
import datetime


class User:
    def __init__(self, user_id, username=None, name=None):
        self.id = str(user_id)
        self.username = username
        self.name = name

        self.ref = db.reference(f"users/{user_id}")
        self.groups_ref = self.ref.child("groups")

        self.init_user_in_db()

    # Initialization in database
    def init_user_in_db(self):
        if not self.is_initialized_in_db():
            self.create_user_info_in_db()
            return {
                "result": True,
                "message": "User has been initialized"
            }

        else:
            return {
                "result": False,
                "message": "User has already been already initialized"
            }

    def is_initialized_in_db(self):
        return self.get_user_info() is not None

    # User info
    def create_user_info_in_db(self):
        return self.ref.set(
            {"user_info": {"first_use_datetime": datetime.datetime.now().timestamp()}}
        )

    def get_user_info(self):
        return self.ref.child("user_info").get()

    # Groups
    def add_group(self, group):
        self.groups_ref.child(group.id).set({"group_name": group.name, "balance": 0})

    def delete_group(self, group):
        self.groups_ref.child(group.id).set({})

    def edit_group_name(self, group):
        self.groups_ref.child(group.id).update({"group_name": group.name})

    def edit_balance(self, group, diff):
        current_balance = self.get_group(group)["balance"]
        self.groups_ref.child(group.id).update({"balance": current_balance + diff})

    def get_group(self, group):
        return self.groups_ref.child(group.id).get()

    def get_groups(self):
        return self.groups_ref.get()

    def reset_group_balance(self, group):
        self.groups_ref.child(group.id).update({"balance": 0})
