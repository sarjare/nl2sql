import re


class MetadataIndex:

    def __init__(self, metadata):

        self.metadata = metadata

        self.index = {}

        self.stop_words = {"the", "of","for","to","a","an","is", "are","per","by", "in","on","at","and","or"}
    def build(self):

        for table in self.metadata:

            # --------------------------
            # Index Table Name
            # --------------------------

            table_words = re.findall(r"\w+", table.lower())

            for word in table_words:

                if word in self.stop_words:
                    continue

                self._add(
                    word,
                    table,
                    None,
                    "table"
                )

            # --------------------------
            # Index Columns
            # --------------------------

            for column in self.metadata[table]["columns"]:

                # Column Name

                column_words = re.findall(
                    r"\w+",
                    column.lower()
                )

                for word in column_words:

                    if word in self.stop_words:
                        continue

                    self._add(
                        word,
                        table,
                        column,
                        "column"
                    )

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

                        self._add(
                            word,
                            table,
                            column,
                            "comment"
                        )

        return self.index

    def _add(self, keyword, table, column, source):

        if keyword not in self.index:

            self.index[keyword] = []

        self.index[keyword].append({

            "table": table,

            "column": column,

            "source": source

        })