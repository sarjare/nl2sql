from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from metadata_index import MetadataIndex
from parser import QueryParser

db = OracleDatabase(DB_CONFIG)

db.connect()

metadata = MetadataLoader(db).load_metadata()

index = MetadataIndex(metadata)

index.build()

parser = QueryParser(index)

while True:

    question = input("Ask : ")

    pprint(parser.parse(question))