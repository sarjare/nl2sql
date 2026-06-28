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

# SELECT
#     a.table_name,
#     a.column_name,
#     c_pk.table_name AS referenced_table,
#     b.column_name AS referenced_column
# FROM all_cons_columns a
# JOIN all_constraints c
#     ON a.owner = c.owner
#    AND a.constraint_name = c.constraint_name
# JOIN all_constraints c_pk
#     ON c.r_owner = c_pk.owner
#    AND c.r_constraint_name = c_pk.constraint_name
# JOIN all_cons_columns b
#     ON c_pk.owner = b.owner
#    AND c_pk.constraint_name = b.constraint_name
#    AND a.position = b.position
# WHERE c.constraint_type = 'R'
# AND a.owner = 'FA_USER';