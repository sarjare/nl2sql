from config import DB_CONFIG


class MetadataLoader:

    def __init__(self, db):
        self.db = db

        # Mapping between working schema and metadata schema
        self.table_mapping = {
            "TRANSMAIN_POC": "TRANSMAIN",
            "PORTFOLIOS_POC": "PORTFOLIOS",
            "SECURITIES_POC": "SECURITIES"
        }

    def load_metadata(self):

        metadata = {}

        # -----------------------------
        # STEP 1 : Read all columns
        # -----------------------------
        column_query = """
        SELECT
            table_name,
            column_name,
            data_type,
            nullable
        FROM all_tab_columns
        WHERE owner = :owner
        AND table_name IN (
            'TRANSMAIN_POC',
            'PORTFOLIOS_POC',
            'SECURITIES_POC'
        )
        ORDER BY table_name, column_id
        """

        columns = self.db.execute(
            column_query,
            {"owner": DB_CONFIG["working_schema"]}
        )

        # -----------------------------
        # STEP 2 : Read comments
        # -----------------------------
        comment_query = """
        SELECT
            table_name,
            column_name,
            comments
        FROM all_col_comments
        WHERE owner = :owner
        """

        comments = self.db.execute(
            comment_query,
            {"owner": DB_CONFIG["metadata_schema"]}
        )

        # -----------------------------
        # STEP 3 : Create lookup dictionary
        # -----------------------------

        comment_lookup = {}

        for table_name, column_name, comment in comments:

            comment_lookup[(table_name, column_name)] = comment

        # -----------------------------
        # STEP 4 : Merge everything
        # -----------------------------

        for table_name, column_name, datatype, nullable in columns:

            if table_name not in metadata:

                metadata[table_name] = {
                    "columns": {}
                }

            original_table = self.table_mapping[table_name]

            comment = comment_lookup.get(
                (original_table, column_name),
                ""
            )

            metadata[table_name]["columns"][column_name] = {
                "datatype": datatype,
                "nullable": nullable,
                "comment": comment
            }

        return metadata