from spreadsheet import SHEET

WORKSHEET = SHEET.worksheet("Payments")


def add_payment(user_id, amount, purpose, date):
    all_values = WORKSHEET.get_all_values()
    new_line_n = len(all_values) + 1

    WORKSHEET.update(f"A{new_line_n}:Z{new_line_n}", [[user_id, amount, purpose, date, 0]])


def discard_payment(payment_id):
    WORKSHEET.update(f"E{payment_id}", 1)

