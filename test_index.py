from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from metadata_index import MetadataIndex

db = OracleDatabase(DB_CONFIG)

db.connect()

metadata = MetadataLoader(db).load_metadata()

index = MetadataIndex(metadata).build()

db.disconnect()

while True:

    word = input("Search : ").lower()

    if word == "exit":
        break

    pprint(index.get(word))