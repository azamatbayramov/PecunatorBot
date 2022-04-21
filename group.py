from firebase_admin import db
import datetime as dt


class Group:
    def __init__(self, group_id, group_name):
        self.group_id = str(group_id)
        self.group_name = group_name

        self.ref = db.reference(f"groups/{group_id}")
        self.users_ref = self.ref.child("users")
        self.operations_ref = self.ref.child("operations")

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
            {"group_info": {"creation_datetime": dt.datetime.now().timestamp(),
                            "group_name": self.group_name,
                            "total_balance": 0
                            }}
        )

    def get_group_info(self):
        return self.ref.child("group_info").get()

    def get_total_balance(self):
        return self.ref.child("group_info/total_balance").get()

    def edit_total_balance(self, diff):
        current_balance = self.get_total_balance()
        self.ref.child("group_info").update({"total_balance": current_balance + diff})

        return current_balance + diff

    # Users
    def add_user(self, user_id, username=None):
        self.users_ref.child(user_id).set({"username": username, "balance": 0})

    def delete_user(self, user_id):
        self.users_ref.child(user_id).set({})

    def edit_username(self, user_id, username):
        self.users_ref.child(user_id).update({"username": username})

    def edit_user_balance(self, user_id, diff):
        current_balance = self.get_user(user_id)["balance"]
        self.users_ref.child(user_id).update({"balance": current_balance + diff})

    def get_user(self, user_id):
        return self.users_ref.child(user_id).get()

    def get_users(self):
        return self.users_ref.get()

    def reset_user_balance(self, user_id):
        self.users_ref.child(user_id).update({"balance": 0})

    # Operations
    def get_operations(self):
        return self.operations_ref.get()

    def add_operation(self, d):
        self.operations_ref.push(d)

    def add_payment(self, author, amount, label):
        self.add_operation({
            "type": "payment",
            "author": author,
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
            "author": author,
            "datetime": dt.datetime.now().timestamp(),
            "is_discarded": False,
            "snapshot": snapshot,
        })
