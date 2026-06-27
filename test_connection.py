from config import DB_CONFIG
from database import OracleDatabase

db = OracleDatabase(DB_CONFIG)

db.connect()

rows = db.execute("SELECT 'CONNECTED' FROM DUAL")

print(rows)

db.disconnect()