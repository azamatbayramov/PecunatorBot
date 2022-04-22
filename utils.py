import group
import user


def get_group_and_user(message):
    g = group.Group(
        str(message.chat.id),
        message.chat.title
    )

    u = user.User(
        str(message.from_user.id),
        message.from_user.username,
        f"{message.from_user.first_name}{' ' + message.from_user.last_name if message.from_user.last_name else ''})"
    )

    return g, u
