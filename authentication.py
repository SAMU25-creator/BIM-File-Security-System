USERS = {
    "valid_user": "correct_password"
}


def login(username, password):
    if username in USERS and USERS[username] == password:
        return True

    return False