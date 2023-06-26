import sqlite3
class Member_DB:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        # IF NOT EXISTS

        sql = """
        CREATE TABLE IF NOT EXISTS member(
            username text,
            mail Text Primary Key,
            phone Integer,
            password text,
            position text
            )
            """
        # Login System DB

        self.cur.execute(sql)
        self.con.commit()

    # insert function
    def insert(self, username, mail, phone, password, position):
        self.cur.execute("INSERT INTO member VALUES(?,?,?,?,?)", (username, mail, phone, password, position))
        self.con.commit()
    # Fetch all data from db
    def fetch(self):
        self.cur.execute("SELECT * FROM member")
        rows = self.cur.fetchall()
        return rows

    def fetch_login(self):
        self.cur.execute("SELECT mail, password FROM member")
        rows = self.cur.fetchall()
        return rows
    def fetch_mail(self):
        self.cur.execute("SELECT mail FROM member")
        rows = self.cur.fetchall()
        return rows
    def fetch_phone(self):
        self.cur.execute("SELECT phone FROM member")
        rows = self.cur.fetchall()
        return rows
    def fetch_password(self):
        self.cur.execute("SELECT password FROM member")
        rows = self.cur.fetchall()
        return rows

    #Delete Function
    def delete(self, id):
        self.cur.execute("DELETE FROM member WHERE id=?", (id,))
        self.con.commit()
db = Member_DB("member.db")