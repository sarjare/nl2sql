from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader

db = OracleDatabase(DB_CONFIG)
db.connect()

loader = MetadataLoader(db)

metadata = loader.load_metadata()
for column, info in metadata["TRANSMAIN_POC"]["columns"].items():
    print(column, "->", info["comment"])
pprint(metadata)

db.disconnect()