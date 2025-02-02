class Database:
    def ___init__(self):
        self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "Ninjago2!",
                database = "vulcanTracker"
            )

        self.cursor = self.conn.cursor()