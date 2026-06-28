import re


class QueryParser:

    def __init__(self, metadata):

        self.metadata = metadata

        self.aggregations = {
            "sum": "SUM",
            "total": "SUM",
            "count": "COUNT",
            "average": "AVG",
            "avg": "AVG",
            "maximum": "MAX",
            "minimum": "MIN",
            "max": "MAX",
            "min": "MIN"
        }

        self.operators = {
            "greater": ">",
            "more": ">",
            "above": ">",
            "less": "<",
            "below": "<",
            "under": "<",
            "equal": "=",
            "equals": "="
        }

    def parse(self, question):

        question = question.lower()

        words = re.findall(r"\w+", question)

        query = {
            "tables": [],
            "columns": [],
            "aggregation": None,
            "filters": [],
            "group_by": [],
            "order_by": None,
            "limit": None
        }

        # -----------------------------
        # Aggregation
        # -----------------------------

        for word in words:
            if word in self.aggregations:
                query["aggregation"] = self.aggregations[word]
                break

        # -----------------------------
        # Detect operator
        # -----------------------------

        operator = None

        for word in words:
            if word in self.operators:
                operator = self.operators[word]
                break

        # -----------------------------
        # Detect numeric value
        # -----------------------------

        value = None

        for word in words:
            if word.isdigit():
                value = int(word)
                break

        # -----------------------------
        # Match columns using comments
        # -----------------------------

        matched_tables = set()
        matched_columns = []

        for table in self.metadata:

            for column in self.metadata[table]["columns"]:

                comment = self.metadata[table]["columns"][column]["comment"]

                if not comment:
                    continue

                keywords = re.findall(r"\w+", comment.lower())

                score = 0

                for word in words:
                    if word in keywords:
                        score += 1

                if score > 0:

                    matched_tables.add(table)

                    matched_columns.append({
                        "table": table,
                        "column": column,
                        "score": score
                    })

        matched_columns.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        seen = set()

        for item in matched_columns:

            if item["column"] not in seen:

                query["columns"].append(item["column"])
                seen.add(item["column"])

        query["tables"] = list(matched_tables)

        # -----------------------------
        # Create filter
        # -----------------------------

        if operator and value is not None and query["columns"]:

            query["filters"].append({

                "column": query["columns"][0],

                "operator": operator,

                "value": value

            })

        return query