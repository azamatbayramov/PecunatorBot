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


def align_balances(group_id):
    session = Session()

    users = session.query(User).filter(User.group_id == group_id).all()

    total = 0