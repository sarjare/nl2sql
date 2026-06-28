class SQLBuilder:

    def __init__(self, metadata):

        self.metadata = metadata

        self.main_table = "TRANSMAIN_POC"

        # Table aliases
        self.alias = {
            "TRANSMAIN_POC": "t",
            "PORTFOLIOS_POC": "p",
            "SECURITIES_POC": "s"
        }

        # Join conditions
        self.joins = {
            "PORTFOLIOS_POC": "t.PORIK = p.PORIK",
            "SECURITIES_POC": "t.SECIK = s.SECIK"
        }

    # =====================================================
    # FIND DATE COLUMN
    # =====================================================
    def find_date_column(self, tables):
        for table in tables:
            if table not in self.metadata:
                continue

        for column, info in self.metadata[table]["columns"].items():

            if info.get("is_date"):

                return {

                    "table": table,

                    "column": column

                }
        return None

    # =====================================================
    # QUALIFY COLUMN
    # =====================================================

    def qualify_column(self, column, tables):

        for table in tables:

            if table not in self.metadata:
                continue

            if column in self.metadata[table]["columns"]:

                alias = self.alias.get(table, "")

                if alias:
                    return f"{alias}.{column}"

                return column

        return column

    # =====================================================
    # BUILD
    # =====================================================

    def build(self, query):

        sql = []

        sql.append(self.build_select(query))

        sql.append(self.build_from(query))

        where_clause = self.build_where(query)

        if where_clause:
            sql.append(where_clause)

        group_clause = self.build_group(query)

        if group_clause:
            sql.append(group_clause)

        order_clause = self.build_order(query)

        if order_clause:
            sql.append(order_clause)

        limit_clause = self.build_limit(query)

        if limit_clause:
            sql.append(limit_clause)

        return "\n".join(sql)

    # =====================================================
    # SELECT
    # =====================================================

    def build_select(self, query):

        columns = query["columns"]

        agg = query["aggregation"]

        if not columns:

            return "SELECT *"
        qualified = []

        for c in columns:

            alias = self.alias[c["table"]]

            qualified.append(

                f"{alias}.{c['column']}"

    )


        if agg:

            return f"SELECT {agg}({qualified[0]})"

        return "SELECT " + ", ".join(qualified)

    # =====================================================
    # FROM
    # =====================================================

    def build_from(self, query):

        tables = query["tables"]

        if not tables:

            return ""

        if len(tables) == 1:

            alias = self.alias.get(tables[0], "")

            return f"FROM {tables[0]} {alias}"

        sql = []

        sql.append(f"FROM {self.main_table} t")

        for table in tables:

            if table == self.main_table:
                continue

            alias = self.alias.get(table, "")

            join = self.joins.get(table)

            if join:

                sql.append(

                    f"JOIN {table} {alias} ON {join}"

                )

        return "\n".join(sql)

    # =====================================================
    # WHERE
    # =====================================================

    def build_where(self, query):

        filters = query["filters"]

        if not filters:
            return ""

        conditions = []

        for f in filters:

            # -------------------------
            # Numeric Filter
            # -------------------------

            if "value" in f and f.get("type") != "string":
                column = self.qualify_column(f["column"],query["tables"] )

                conditions.append(

                    f"{column} {f['operator']} {f['value']}"

                )
            elif f.get("type") == "string":
                column = self.qualify_column(f["table"],f["column"]

    )

                conditions.append(

                f"{column} = '{f['value']}'"

    )

            # -------------------------
            # Date Filter
            # -------------------------

            elif f.get("type") == "date":

                date_column = self.find_date_column(
                    query["tables"]
                )

                if date_column:

                    date_column = self.qualify_column(
                        date_column,
                        query["tables"]
                    )

                    conditions.append(

                        f"""{date_column}
BETWEEN
TO_DATE('{f['start']}','YYYY-MM-DD')
AND
TO_DATE('{f['end']}','YYYY-MM-DD')"""

                    )

        if not conditions:
            return ""

        return "WHERE\n" + "\nAND ".join(conditions)
        # =====================================================
    # GROUP BY
    # =====================================================

    def build_group(self, query):

        if not query["group_by"]:
            return ""

        qualified = []

        for column in query["group_by"]:

            qualified.append(
                self.qualify_column(
                    column,
                    query["tables"]
                )
            )

        return "GROUP BY " + ", ".join(qualified)

    # =====================================================
    # ORDER BY
    # =====================================================

    def build_order(self, query):

        order = query["order_by"]

        if not order:
            return ""

        if not query["columns"]:
            return ""

        column = self.qualify_column(
            query["columns"][0],
            query["tables"]
        )

        direction = order.get("direction", "ASC")

        return f"ORDER BY {column} {direction}"

    # =====================================================
    # LIMIT
    # =====================================================

    def build_limit(self, query):

        limit = query.get("limit")

        if limit is None:
            return ""

        return f"FETCH FIRST {limit} ROWS ONLY"

    # =====================================================
    # VALIDATE QUERY
    # =====================================================

    def validate(self, query):

        if not query["tables"]:
            raise Exception("No table detected.")

        if not query["columns"] and query["aggregation"] is None:
            raise Exception("No column detected.")

        return True

    # =====================================================
    # PRETTY SQL
    # =====================================================

    def pretty_print(self, sql):

        print("\nGenerated SQL")
        print("=" * 60)
        print(sql)
        print("=" * 60)