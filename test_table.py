from config import DB_CONFIG
from database import OracleDatabase

db = OracleDatabase(DB_CONFIG)
db.connect()

rows = db.execute("""
SELECT table_name
FROM all_tables
WHERE owner = :owner
""", {"owner": DB_CONFIG["working_schema"]})

print(rows)

db.disconnect()