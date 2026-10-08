
import hashlib
from db import execute_insert, execute_select


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(login, password, role="user"):
    existing = execute_select("users", {"login": login})

    if existing:
        return None

    return execute_insert("users", {
        "login": login,
        "password_hash": hash_password(password),
        "role": role
    })


def authenticate(login, password):
    users = execute_select("users", {"login": login})

    if not users:
        return None

    user = users[0]

    if user["password_hash"] == hash_password(password):
        return user

    return None


def check_permission(current_user, action, target_owner=None):
    users = execute_select("users", {"login": current_user})

    if not users:
        return False

    role = users[0]["role"]

    if role == "admin":
        return True

    if action == "kill":
        return False

    if action == "delete_file":
        if target_owner is None:
            return False
        return target_owner == current_user

    return True
