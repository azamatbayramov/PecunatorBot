from spreadsheet import SHEET

WORKSHEET = SHEET.worksheet("Users")


def get_info_about_user(user_id=None, username=None):
    if user_id:
        find_index = 0
        find_thing = str(user_id)
    elif username:
        find_index = 1
        find_thing = str(username)
    else:
        return Exception("You have to pass user_id or username")

    all_values = WORKSHEET.get_all_values()

    for i in range(len(all_values)):
        if all_values[i][find_index] == find_thing:
            info = [int(all_values[i][0]), all_values[i][1], int(all_values[i][2]), int(all_values[i][3])]
            return i + 1, info

    return None


def add_user(user_id, username, joined):
    all_values = WORKSHEET.get_all_values()
    new_line_n = len(all_values) + 1

    WORKSHEET.update(f"A{new_line_n}:Z{new_line_n}", [[user_id, username, 0, joined]])


def edit_joined(user_id, username, joined):
    info_about_user = get_info_about_user(user_id)

    if info_about_user:
        row, info = info_about_user

        if info[3] == joined and joined:
            return "User @{} already joined"
        elif info[3] == joined and not joined:
            return "User @{} already left"

        WORKSHEET.update(f"D{row}", joined)
    else:
        add_user(user_id, username, joined)

    # Add joinings

    if joined:
        return "User @{} joined"
    else:
        return "User @{} left"




def update_balances_after_payment(user_id, amount):
    pass
