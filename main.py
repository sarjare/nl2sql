from pprint import pprint

from config import DB_CONFIG
from database import OracleDatabase
from metadata_loader import MetadataLoader
from metadata_index import MetadataIndex
from parser import QueryParser
from sql_builder import SQLBuilder


def main():

    # -----------------------------
    # Connect Database
    # -----------------------------

    db = OracleDatabase(DB_CONFIG)

    db.connect()

    # -----------------------------
    # Load Metadata
    # -----------------------------

    loader = MetadataLoader(db)

    metadata = loader.load_metadata()

    # -----------------------------
    # Build Metadata Index
    # -----------------------------

    index = MetadataIndex(metadata)

    index.build()

    # -----------------------------
    # Parser
    # -----------------------------

    parser = QueryParser(index)

    # -----------------------------
    # SQL Builder
    # -----------------------------

    builder = SQLBuilder(metadata)

    # -----------------------------
    # Ask Question
    # -----------------------------

    while True:

        question = input("\nAsk> ")

        if question.lower() == "exit":
            break

        query = parser.parse(question)

        print("\nParsed Query")

        pprint(query)

        sql = builder.build(query)

        print("\nGenerated SQL")

        print(sql)

        print("\nExecuting...\n")

        rows = db.execute(sql)

        for row in rows:

            print(row)

    db.disconnect()


if __name__ == "__main__":

    main()