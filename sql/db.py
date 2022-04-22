import sqlite3


class DB:
    def __init__(self):

        self.cur = None
        self.con = None

        self.connect_sqlite3()

        self.create_table()

    def connect_sqlite3(self):
        self.con = sqlite3.connect('bmwix.db')

    def create_table(self):
        self.cur = self.con.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE trade_setting
                       (up_rate, add_rate, trade_high, trade_low, buy_amt)''')

        # Insert a row of data
        self.cur.execute("INSERT INTO trade_setting VALUES (10, 10, 9, 5, 100000)")

        # Save (commit) the changes
        self.con.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()
