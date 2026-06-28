import re
from collections import defaultdict


class MetadataIndex:

    def __init__(self, metadata):

        self.metadata = metadata

        self.index = defaultdict(list)

        self.stop_words = {
            "the", "of", "for", "to", "a", "an",
            "is", "are", "per", "by", "in",
            "on", "at", "and", "or",
            "show", "get", "give", "display",
            "find", "list", "all"
        }

        # Simple synonym dictionary
        self.synonyms = {

            "shares": "share",
            "security": "securities",
            "portfolio": "portfolios",
            "fund": "portfolio",
            "value": "amount",
            "qty": "quantity",
            "transaction": "transactions"

        }

    # ====================================================
    # BUILD INDEX
    # ====================================================
    def build(self):
        for table in self.metadata:

        # ======================================
        # TABLE NAME
        # ======================================

            table_words = self.tokenize(table)

            table_keywords = self.create_phrases(table_words)

        for keyword in table_keywords:

            self._add(
                keyword=keyword,
                table=table,
                column=None,
                source="table"
            )

        # ======================================
        # COLUMNS
        # ======================================

        for column, info in self.metadata[table]["columns"].items():

            datatype = info["datatype"]

            nullable = info["nullable"]

            comment = info["comment"] or ""

            # ----------------------------------
            # COLUMN NAME
            # ----------------------------------

            column_words = self.tokenize(column)

            column_keywords = self.create_phrases(column_words)

            for keyword in column_keywords:

                self._add(
                    keyword=keyword,
                    table=table,
                    column=column,
                    source="column",
                    datatype=datatype,
                    nullable=nullable,
                    comment=comment
                )

            # ----------------------------------
            # COLUMN COMMENT
            # ----------------------------------

            comment_words = self.tokenize(comment)

            comment_keywords = self.create_phrases(comment_words)

            for keyword in comment_keywords:

                self._add(
                    keyword=keyword,
                    table=table,
                    column=column,
                    source="comment",
                    datatype=datatype,
                    nullable=nullable,
                    comment=comment
                )

        return self.index

    # ====================================================
    # NORMALIZE
    # ====================================================

    def normalize(self, word):

        word = word.lower()

        if word in self.synonyms:
            return self.synonyms[word]

        return word
    # ====================================================
# TOKENIZE
# ====================================================

def tokenize(self, text):

    words = re.findall(r"\w+", text.lower())

    tokens = []

    for word in words:

        word = self.normalize(word)

        if word in self.stop_words:
            continue

        tokens.append(word)

    return tokens


# ====================================================
# CREATE PHRASES
# ====================================================

def create_phrases(self, words):

    phrases = []

    # Single words

    phrases.extend(words)

    # Two-word phrases

    for i in range(len(words) - 1):

        phrases.append(

            words[i] + " " + words[i + 1]

        )

    # Three-word phrases

    for i in range(len(words) - 2):

        phrases.append(

            words[i] + " " +
            words[i + 1] + " " +
            words[i + 2]

        )

    return phrases
    # ====================================================
    # ADD
    # ====================================================

    def _add(
        self,
        keyword,
        table,
        column,
        source,
        datatype=None,
        nullable=None,
        comment=""
    ):

        self.index[keyword].append({

            "table": table,

            "column": column,

            "source": source,

            "datatype": datatype,

            "nullable": nullable,

            "comment": comment

        })

    # ====================================================
    # SEARCH
    # ====================================================
def search(self, question):

    words = self.tokenize(question)

    keywords = self.create_phrases(words)

    scores = {}

    table_scores = {}

    for word in keywords:

        if word not in self.index:
            continue

        for item in self.index[word]:

            key = (
                item["table"],
                item["column"]
            )

            if key not in scores:

                scores[key] = {

                    "table": item["table"],

                    "column": item["column"],

                    "datatype": item["datatype"],

                    "nullable": item["nullable"],

                    "comment": item["comment"],

                    "score": 0

                }

            points = 0

            # Phrase matching
            if " " in word:

                points += 5

            else:

                points += 2

            # Comment is stronger than column name
            if item["source"] == "comment":

                points += 3

            elif item["source"] == "column":

                points += 2

            else:

                points += 1

            scores[key]["score"] += points

            table = item["table"]

            table_scores[table] = table_scores.get(table, 0) + points

    if not table_scores:

        return []

    best_table = max(

        table_scores,

        key=table_scores.get

    )

    results = [

        row

        for row in scores.values()

        if row["table"] == best_table

    ]

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return results