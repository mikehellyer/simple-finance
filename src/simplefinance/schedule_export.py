"""Export Scheduled Transactions to CSV.

The first six columns are exactly what the Scheduled tab's "Import CSV..."
reads (Day of Month, Account, Category, Payee, Amount, Frequency), so an
export can be re-imported. The importer ignores columns it doesn't know, so
the extra fields it would otherwise lose (Name, Next Date, Memo, Active) are
appended after them - the file is a complete record, not just importable.

Amount keeps the stored sign (Expense negative, Income positive), matching
the import template. Next Date is ISO (YYYY-MM-DD) so a spreadsheet can't
misread it as day/month. No Tkinter dependency, so it can be unit tested.
"""

import csv
from datetime import date

HEADERS = [
    "Day of Month",
    "Account",
    "Category",
    "Payee",
    "Amount",
    "Frequency",
    "Name",
    "Next Date",
    "Memo",
    "Active",
]


def _day_of_month(next_date):
    try:
        return date.fromisoformat(str(next_date)).day
    except ValueError:
        return ""


def schedule_row(schedule):
    """One CSV row for a schedule dict (keys as returned by get_schedules)."""
    next_date = schedule["next_date"]
    return [
        _day_of_month(next_date),
        schedule["account_name"],
        schedule["category_name"],
        schedule["payee"],
        f"{round(float(schedule['amount']), 2) + 0.0:.2f}",
        schedule["frequency"],
        schedule["name"],
        next_date,
        schedule["memo"],
        "Yes" if schedule["active"] else "No",
    ]


def write_schedules_csv(path, schedules):
    """Write schedules to path (UTF-8 with BOM so Excel reads it correctly,
    like the import template). Returns the number of schedules written."""
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        count = 0
        for schedule in schedules:
            writer.writerow(schedule_row(schedule))
            count += 1
    return count
