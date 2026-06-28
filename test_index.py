from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from metadata_index import MetadataIndex

db = OracleDatabase(DB_CONFIG)

db.connect()

metadata = MetadataLoader(db).load_metadata()

index = MetadataIndex(metadata)

index.build()

while True:

    question = input("Ask : ")

    pprint(index.search(question))