import re
from collections import defaultdict
from date_parser import DateParser
class QueryParser:

    def __init__(self, metadata_index):

        self.metadata_index = metadata_index
        self.date_parser = DateParser()
        # --------------------------
        # SQL Functions
        # --------------------------

        self.aggregations = {

            "sum": "SUM",
            "total": "SUM",

            "count": "COUNT",

            "average": "AVG",
            "avg": "AVG",

            "minimum": "MIN",
            "min": "MIN",

            "maximum": "MAX",
            "max": "MAX"
        }

        # --------------------------
        # Comparison Operators
        # --------------------------

        self.operator_patterns = {

            "greater than": ">",
            "more than": ">",
            "above": ">",

            "less than": "<",
            "below": "<",
            "under": "<",

            "equal to": "=",
            "equals": "=",
            "equal": "="
        }

        # --------------------------
        # Sorting
        # --------------------------

        self.sort_keywords = {

            "highest": "DESC",
            "largest": "DESC",
            "biggest": "DESC",
            "top": "DESC",

            "lowest": "ASC",
            "smallest": "ASC",
            "bottom": "ASC"
        }

        self.group_keywords = {

            "group",
            "each",
            "per"
        }

    # ===========================================================
    # TOKENIZER
    # ===========================================================

    def tokenize(self, question):

        return re.findall(r"\w+", question.lower())

    # ===========================================================
    # AGGREGATION
    # ===========================================================

    def find_aggregation(self, question):

        question = question.lower()

        for key in self.aggregations:

            if key in question:

                return self.aggregations[key]

        return None

    # ===========================================================
    # LIMIT
    # ===========================================================

    def find_limit(self, question):

        question = question.lower()

        m = re.search(r"top\s+(\d+)", question)

        if m:

            return int(m.group(1))

        m = re.search(r"first\s+(\d+)", question)

        if m:

            return int(m.group(1))

        return None

    # ===========================================================
    # ORDER BY
    # ===========================================================

    def find_order(self, question):

        question = question.lower()

        for key in self.sort_keywords:

            if key in question:

                return {

                    "direction": self.sort_keywords[key]

                }

        return None

    # ===========================================================
    # OPERATOR
    # ===========================================================

    def find_operator(self, question):

        question = question.lower()

        for text in sorted(
                self.operator_patterns.keys(),
                key=len,
                reverse=True):

            if text in question:

                return self.operator_patterns[text]

        return None

    # ===========================================================
    # NUMBER
    # ===========================================================

    def find_number(self, question):

        m = re.search(r"\d+", question)

        if m:

            return int(m.group())

        return None

    # ===========================================================
    # SEARCH METADATA
    # ===========================================================
    # ===========================================================
# SEARCH METADATA
# ===========================================================

def search_metadata(self, question):

    matches = self.metadata_index.search(question)

    tables = []
    columns = []

    seen_tables = set()
    seen_columns = set()

    for item in matches:

        # -----------------------------
        # Tables
        # -----------------------------

        if item["table"] not in seen_tables:

            tables.append(item["table"])
            seen_tables.add(item["table"])

        # -----------------------------
        # Columns
        # -----------------------------

        if item["column"]:

            key = (item["table"], item["column"])

            if key not in seen_columns:

                columns.append({
                    "table": item["table"],
                    "column": item["column"]
                })

                seen_columns.add(key)

    return tables, columns
    # ===========================================================
    # BUILD FILTER
    # ===========================================================
def build_filter(self, columns, question):
    if not columns:
        return []
    question = question.lower()

    filters = []

    patterns = [

        (r"(greater than|more than|above)\s+(\d+)", ">"),

        (r"(less than|below|under)\s+(\d+)", "<"),

        (r"(equal to|equals|equal)\s+(\d+)", "=")

    ]

    for pattern, operator in patterns:

        matches = re.findall(pattern, question)

        for match in matches:

            value = int(match[1])

            filters.append({

                "table": columns[0]["table"],

                "column": columns[0]["column"],

                "operator": operator,

                "value": value

            })

    return filters
def build_filter(self, columns, question):

    if not columns:
        return []

    question = question.lower()

    filters = []

    patterns = [

        (r"(greater than|more than|above)\s+(\d+)", ">"),

        (r"(less than|below|under)\s+(\d+)", "<"),

        (r"(equal to|equals|equal)\s+(\d+)", "=")

    ]

    for pattern, operator in patterns:

        matches = re.findall(pattern, question)

        for match in matches:

            value = int(match[1])

            filters.append({

                "table": columns[0]["table"],

                "column": columns[0]["column"],

                "operator": operator,

                "value": value

            })

    return filters
    #=========================================================
    # GROUP BY
    # ===========================================================

def find_group_by(self, question):
    question = question.lower()
    for word in self.group_keywords:
        if word in question:
            return True

        return False

    # ===========================================================
    # DATE PLACEHOLDER
    # ===========================================================
def find_dates(self, question):

    date_filter = self.date_parser.parse(question)

    if date_filter:

        return [date_filter]

    return []
    # ===========================================================
    # MAIN PARSER
    # ===========================================================

def parse(self, question):
    query = {
        "tables": [],

            "columns": [],

            "aggregation": None,

            "filters": [],

            "group_by": [],

            "order_by": None,

            "limit": None

        }

        # ----------------------------------
        # Metadata Search
        # ----------------------------------

    tables, columns = self.search_metadata(question)
    query["tables"] = tables
    query["columns"] = columns

        # ----------------------------------
        # Aggregation
        # ----------------------------------

    query["aggregation"] = self.find_aggregation(question)

        # ----------------------------------
        # Limit
        # ----------------------------------

    query["limit"] = self.find_limit(question)

        # ----------------------------------
        # Order
        # ----------------------------------

    query["order_by"] = self.find_order(question)

        # ----------------------------------
        # Operator
        # ----------------------------------

    operator = self.find_operator(question)

        # ----------------------------------
        # Number
        # ----------------------------------

    value = self.find_number(question)

        # ----------------------------------
        # Filter
        # ----------------------------------

    query["filters"].extend(self.build_filter(

            columns,
            question

        )
    )
        # ----------------------------------
        # Dates
        # ----------------------------------

    date_filters = self.find_dates(question)
    if date_filters:
        query["filters"].extend(date_filters)

        # ----------------------------------
        # Group By
        # ----------------------------------

    if self.find_group_by(question):
        if len(columns) > 1:
                query["group_by"] = [c["column"]for c in columns[1:]]
        return query