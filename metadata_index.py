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
        # ===========================================
# Ranking Weights
# ===========================================

    self.weights = {

        "column_exact": 10,

        "comment_exact": 8,

        "column": 6,

        "comment": 4,

        "table": 2,

        "synonym": 1

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
        word = word.lower().strip()
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

    words = re.findall(r"\w+", question.lower())

    words = [self.normalize(word) for word in words]

    scores = {}

    for word in words:

        if word in self.stop_words:
            continue

        if word not in self.index:
            continue

        for item in self.index[word]:

            key = (item["table"], item["column"])

            if key not in scores:

                scores[key] = {

                    "table": item["table"],

                    "column": item["column"],

                    "datatype": item["datatype"],

                    "nullable": item["nullable"],

                    "comment": item["comment"],

                    "score": 0

                }

            score = 0

            if item["source"] == "column":

                if item["column"] and item["column"].lower() == word:

                    score = self.weights["column_exact"]

                else:

                    score = self.weights["column"]

            elif item["source"] == "comment":

                comment = (item["comment"] or "").lower()

                if comment == word:

                    score = self.weights["comment_exact"]

                elif word in comment:

                    score = self.weights["comment"]

            elif item["source"] == "table":

                score = self.weights["table"]

            scores[key]["score"] += score

    results = list(scores.values())

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )
    for item in results:
        if item["score"] >= 20:

            item["confidence"] = "HIGH"

        elif item["score"] >= 10:

            item["confidence"] = "MEDIUM"

        else:

            item["confidence"] = "LOW"
    return results