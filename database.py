import oracledb

class OracleDatabase:

    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):

        dsn = f"{self.config['host']}:{self.config['port']}/{self.config['service']}"

        self.connection = oracledb.connect(
            user=self.config["user"],
            password=self.config["password"],
            dsn=dsn
        )

        print("Connected to Oracle")

    def disconnect(self):

        if self.connection:
            self.connection.close()

    def execute(self, query, params=None):

        cursor = self.connection.cursor()

        cursor.execute(query, params or {})

        return cursor.fetchall()