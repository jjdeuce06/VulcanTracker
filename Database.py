class Database:
    def __init__(self):
        self.conn 

    def connect_database(self):
        self.conn = mysql.connector.connect(
                host = "",  #Enter your own data
                user = "",
                password = "",
                database = "vulcanTracker"
            )
        self.cursor = self.conn.cursor()