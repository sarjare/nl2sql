from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from sql_builder import SQLBuilder

db = OracleDatabase(DB_CONFIG)

db.connect()

metadata = MetadataLoader(db).load_metadata()

builder = SQLBuilder(metadata)

query = {

    "tables": [
        "SECURITIES_POC"
    ],

    "columns": [
        "SECSIZE"
    ],

    "aggregation": "SUM",

    "filters": [

        {
            "column": "SECSIZE",
            "operator": ">",
            "value": 100
        }

    ],

    "group_by": [],

    "order_by": {

        "direction": "DESC"

    },

    "limit": 10

}

builder.validate(query)

sql = builder.build(query)

builder.pretty_print(sql)