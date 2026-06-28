import re
import calendar
from datetime import date, timedelta


class DateParser:

    def __init__(self):

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

    # ======================================================
    # BUILD FILTER
    # ======================================================

    def build_filter(
        self,
        start,
        end,
        filter_type="date",
        confidence=1.0,
        label=None
    ):

        return {
            "type": filter_type,
            "operator": "BETWEEN",
            "start": start,
            "end": end,
            "confidence": confidence,
            "label": label
        }

    # ======================================================
    # MAIN PARSER
    # ======================================================

    def parse(self, question):

        question = question.lower().strip()

        today = date.today()

        # ---------------- TODAY ----------------

        if "today" in question:

            d = today.strftime("%Y-%m-%d")

            return self.build_filter(d, d, label="today")

        # ---------------- YESTERDAY ----------------

        if "yesterday" in question:

            d = today - timedelta(days=1)

            d = d.strftime("%Y-%m-%d")

            return self.build_filter(d, d, label="yesterday")

        # ---------------- LAST 7 DAYS ----------------

        if "last 7 days" in question:

            start = today - timedelta(days=7)

            return self.build_filter(
                start.strftime("%Y-%m-%d"),
                today.strftime("%Y-%m-%d"),
                label="last 7 days"
            )

        # ---------------- LAST 30 DAYS ----------------

        if "last 30 days" in question:

            start = today - timedelta(days=30)

            return self.build_filter(
                start.strftime("%Y-%m-%d"),
                today.strftime("%Y-%m-%d"),
                label="last 30 days"
            )

        # ---------------- THIS WEEK ----------------

        if "this week" in question:

            start = today - timedelta(days=today.weekday())

            end = start + timedelta(days=6)

            return self.build_filter(
                start.strftime("%Y-%m-%d"),
                end.strftime("%Y-%m-%d"),
                label="this week"
            )

        # ---------------- LAST WEEK ----------------

        if "last week" in question:

            this_week = today - timedelta(days=today.weekday())

            end = this_week - timedelta(days=1)

            start = end - timedelta(days=6)

            return self.build_filter(
                start.strftime("%Y-%m-%d"),
                end.strftime("%Y-%m-%d"),
                label="last week"
            )

        # ---------------- THIS MONTH ----------------

        if "this month" in question:

            first = today.replace(day=1)

            last = today.replace(
                day=calendar.monthrange(today.year, today.month)[1]
            )

            return self.build_filter(
                first.strftime("%Y-%m-%d"),
                last.strftime("%Y-%m-%d"),
                label="this month"
            )

        # ---------------- LAST MONTH ----------------

        if "last month" in question:

            month = today.month - 1

            year = today.year

            if month == 0:
                month = 12
                year -= 1

            first = date(year, month, 1)

            last = date(
                year,
                month,
                calendar.monthrange(year, month)[1]
            )

            return self.build_filter(
                first.strftime("%Y-%m-%d"),
                last.strftime("%Y-%m-%d"),
                label="last month"
            )

        # ---------------- THIS YEAR ----------------

        if "this year" in question:

            return self.build_filter(
                f"{today.year}-01-01",
                f"{today.year}-12-31",
                label="this year"
            )

        # ---------------- LAST YEAR ----------------

        if "last year" in question:

            year = today.year - 1

            return self.build_filter(
                f"{year}-01-01",
                f"{year}-12-31",
                label="last year"
            )

        # ---------------- QUARTER ----------------

        quarter = re.search(r"q([1-4])\s*(20\d{2})", question)

        if quarter:

            q = int(quarter.group(1))

            year = int(quarter.group(2))

            first_month = (q - 1) * 3 + 1

            first = date(year, first_month, 1)

            last_month = first_month + 2

            last = date(
                year,
                last_month,
                calendar.monthrange(year, last_month)[1]
            )

            return self.build_filter(
                first.strftime("%Y-%m-%d"),
                last.strftime("%Y-%m-%d"),
                label=f"Q{q} {year}"
            )

        # ---------------- FINANCIAL YEAR ----------------

        fy = re.search(r"fy\s*(20\d{2})", question)

        if fy:

            year = fy.group(1)

            return self.build_filter(
                f"{year}-01-01",
                f"{year}-12-31",
                label=f"FY{year}"
            )

        # ---------------- MONTH YEAR ----------------

        month_match = re.search(r"([a-zA-Z]+)\s+(20\d{2})", question)

        if month_match:

            month_name = month_match.group(1)

            year = int(month_match.group(2))

            if month_name in self.months:

                month = self.months[month_name]

                first = date(year, month, 1)

                last = date(
                    year,
                    month,
                    calendar.monthrange(year, month)[1]
                )

                return self.build_filter(
                    first.strftime("%Y-%m-%d"),
                    last.strftime("%Y-%m-%d"),
                    label=f"{month_name.title()} {year}"
                )

        # ---------------- YEAR ----------------

        year_match = re.search(r"\b(20\d{2})\b", question)

        if year_match:

            year = year_match.group(1)

            return self.build_filter(
                f"{year}-01-01",
                f"{year}-12-31",
                label=year
            )

        return None