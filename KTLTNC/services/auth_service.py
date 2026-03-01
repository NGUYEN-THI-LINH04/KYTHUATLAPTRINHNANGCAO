USER_FILE = "data/users.txt"

def check_login(username, password):
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                u, p, role = line.strip().split(";")
                if u == username and p == password:
                    return {
                        "username": u,
                        "role": role
                    }
    except FileNotFoundError:
        return None

    return None
