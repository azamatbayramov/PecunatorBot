from database.models import Group, User, Operation
from database.database import Session


def get_balances_str(group_id):
    session = Session()

    group = session.query(Group).filter(Group.telegram_id == group_id).first()

    answer = ''

    for user in group.users:
        answer += f'{user.username} - {user.balance}\n'

    answer += f"Total balance: {group.total_balance}"

    return answer


def get_transactions_to_align_balances(group_id):
    session = Session()

    group = session.query(Group).filter(Group.telegram_id == group_id).first()

    users = group.users

    transactions = solve_balances(users)

    answer = 'Transactions:\n'

    for i in transactions:
        answer += f"{i[0]} -> {i[1]} {i[2]}\n"

    return answer


def solve_balances(users):
    lst = [[user.balance, user.username] for user in users]

    transactions = []

    average = sum([b[0] for b in lst]) / len(lst)

    lst.sort(key=lambda s: s[0], reverse=True)

    for i in range(len(lst)):
        if lst[i][0] == average:
            break

        for j in range(len(lst) - 1, -1, -1):
            if lst[j][0] == average:
                break

            c = lst[i][0] - average
            q = average - lst[j][0]

            if q >= c:
                transactions.append((lst[j][1], lst[i][1], c))
                lst[i][0] -= c
                lst[j][0] += c
            else:
                transactions.append((lst[j][1], lst[i][1], c - q))
                lst[i][0] -= q
                lst[j][0] += q
            print(lst)

    return transactions
