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

    def parse(self, question):

        question = question.lower()

        words = re.findall(r"\w+", question)

        query = {
            "tables": [],
            "columns": [],
            "aggregation": None,
            "filters": []
        }

        # ------------------------
        # Find Aggregation
        # ------------------------

        for word in words:
            if word in self.aggregations:
                query["aggregation"] = self.aggregations[word]
                break

        # ------------------------
        # Find Tables & Columns
        # ------------------------

        best_score = 0

        best_table = None

        best_column = None

        for table in self.metadata:

            table_score = 0

            for column in self.metadata[table]["columns"]:

                comment = self.metadata[table]["columns"][column]["comment"]

                if comment is None:
                    continue

                keywords = comment.lower().split()

                score = 0

                for word in words:

                    if word in keywords:
                        score += 1

                if score > best_score:

                    best_score = score

                    best_table = table

                    best_column = column

        if best_table:

            query["tables"].append(best_table)

            query["columns"].append(best_column)

        return query