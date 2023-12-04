import sqlite3


class UserGold:
    def __init__(self, username, goldBits=-1):
        self.username = username.upper()
        self.goldBits = goldBits
        self.conn = sqlite3.connect('user.db')
        self.cursor = self.conn.cursor()

    def save(self):
        self.cursor.execute(f"INSERT INTO user VALUES ('{self.username}', '{self.goldBits}')")
        self.conn.commit()

    def get(self):
        self.cursor.execute(f"SELECT * FROM user WHERE username = '{self.username}'")
        data = self.cursor.fetchone()
        self.conn.commit()
        self.goldBits = data[1]

    def update(self, new_gold):
        self.cursor.execute(f"UPDATE user SET goldBits = '{new_gold}' WHERE username = '{self.username}'")
        self.conn.commit()


def check_for_user(username):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
    data = cursor.fetchone()
    conn.commit()
    conn.close()

    if not data:
        return False
    else:
        return True
