import re


class QueryParser:

    def __init__(self, metadata_index):

        self.metadata_index = metadata_index

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
            "greater than": ">",
            "more than": ">",
            "above": ">",
            "less than": "<",
            "below": "<",
            "under": "<",
            "equal to": "=",
            "equals": "=",
            "=": "=",
            ">": ">",
            "<": "<"
        }

        self.months = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12
        }

    def parse(self, question):

        question = question.lower()

        query = {
            "tables": [],
            "columns": [],
            "aggregation": None,
            "filters": [],
            "group_by": [],
            "order_by": None,
            "limit": None
        }

        # -------------------------
        # Search metadata index
        # -------------------------

        matches = self.metadata_index.search(question)

        seen_tables = set()
        seen_columns = set()

        for item in matches:

            if item["table"] not in seen_tables:
                query["tables"].append(item["table"])
                seen_tables.add(item["table"])

            if item["column"] and item["column"] not in seen_columns:
                query["columns"].append(item["column"])
                seen_columns.add(item["column"])

        # -------------------------
        # Aggregation
        # -------------------------

        for word, sql in self.aggregations.items():

            if word in question:

                query["aggregation"] = sql
                break

        # -------------------------
        # Top N
        # -------------------------

        top = re.search(r"top\s+(\d+)", question)

        if top:

            query["limit"] = int(top.group(1))

            query["order_by"] = {
                "direction": "DESC"
            }

        # -------------------------
        # Numbers
        # -------------------------

        number = re.search(r"\d+", question)

        value = None

        if number:

            value = int(number.group())

        # -------------------------
        # Operators
        # -------------------------

        operator = None

        for text, symbol in self.operators.items():

            if text in question:

                operator = symbol
                break

        if operator and value and query["columns"]:

            query["filters"].append({

                "column": query["columns"][0],

                "operator": operator,

                "value": value

            })

        return query