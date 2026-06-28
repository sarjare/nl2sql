from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from parser import QueryParser

db = OracleDatabase(DB_CONFIG)

db.connect()

loader = MetadataLoader(db)

metadata = loader.load_metadata()

parser = QueryParser(metadata)

question = input("Ask: ")

query = parser.parse(question)

print(query)

db.disconnect()