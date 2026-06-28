import re
from collections import defaultdict


class MetadataIndex:

    def __init__(self, metadata):

        self.metadata = metadata

        self.index = defaultdict(list)

        self.stop_words = {
            "the", "of", "for", "to", "a", "an",
            "is", "are", "per", "by", "in",
            "on", "at", "and", "or", "show"
        }

    # ----------------------------------------
    # Build Index
    # ----------------------------------------

    def build(self):

        for table in self.metadata:

            # -------------------------
            # Table Name
            # -------------------------

            table_words = re.findall(r"\w+", table.lower())

            for word in table_words:

                if word in self.stop_words:
                    continue

                self._add(word, table, None, "table")

            # -------------------------
            # Columns
            # -------------------------

            for column in self.metadata[table]["columns"]:

                # Column Name

                column_words = re.findall(r"\w+", column.lower())

                for word in column_words:

                    if word in self.stop_words:
                        continue

                    self._add(word, table, column, "column")

                # Column Comment

                comment = self.metadata[table]["columns"][column]["comment"]

                if comment:

                    comment_words = re.findall(
                        r"\w+",
                        comment.lower()
                    )

                    for word in comment_words:

                        if word in self.stop_words:
                            continue

                        self._add(word, table, column, "comment")

        return self.index

    # ----------------------------------------
    # Add keyword
    # ----------------------------------------

    def _add(self, keyword, table, column, source):

        self.index[keyword].append({

            "table": table,

            "column": column,

            "source": source

        })

    # ----------------------------------------
    # Search
    # ----------------------------------------

    def search(self, question):

        words = re.findall(r"\w+", question.lower())

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
                        "score": 0
                    }

                scores[key]["score"] += 1

        results = list(scores.values())

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results