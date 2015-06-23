import functools
AUTHENTICATION_LEVELS = [
    "NO AUTH",
    "APPLICATION",
    "MEMBER"
]


def no_auth(func):
    func._auth_level = 0
    return func

def app_auth(func):
    func._auth_level = 1
    return func

def member_auth(func):
    func._auth_level = 2
    return func
