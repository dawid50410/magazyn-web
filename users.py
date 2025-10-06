
from werkzeug.security import generate_password_hash, check_password_hash

users = {
    'admin': {
        'password_hash': generate_password_hash('haslo123'),
        'role': 'admin'
    },
    'viewer': {
        'password_hash': generate_password_hash('podglad'),
        'role': 'viewer'
    }
}

def verify_user(username, password):
    u = users.get(username)
    if not u:
        return False
    return check_password_hash(u['password_hash'], password)

def get_role(username):
    u = users.get(username)
    if not u:
        return None
    return u['role']
