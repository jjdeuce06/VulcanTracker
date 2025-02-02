class Database:
    def ___init__(self):
        self.conn = mysql.connector.connect(
                host = "", #Enter your own data!
                user = "",
                password = "",
                database = "vulcanTracker"
            )

        self.cursor = self.conn.cursor()