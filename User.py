class User:
    def __init__(self, user):
        self.username = user["username"]
        self.favorites = user["favorites"]
        self.pref = user["pref"]