import csv

import pytest

from simplefinance.schedule_export import HEADERS, schedule_row, write_schedules_csv


def schedule(**kw):
    row = {
        "name": "Rent",
        "account_name": "Current Account",
        "category_name": "Mortgage / Rent",
        "payee": "Green Valley Rentals",
        "memo": "",
        "amount": -950.0,
        "frequency": "Monthly",
        "next_date": "2026-10-01",
        "active": 1,
    }
    row.update(kw)
    return row


def read_back(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def test_headers_start_with_the_columns_import_csv_requires():
    # Import CSV requires exactly these six (matched case-insensitively);
    # anything after them is ignored, so an export can be re-imported.
    assert HEADERS[:6] == [
        "Day of Month",
        "Account",
        "Category",
        "Payee",
        "Amount",
        "Frequency",
    ]
    assert HEADERS[6:] == ["Name", "Next Date", "Memo", "Active"]


def test_row_values():
    assert schedule_row(schedule(memo="monthly rent")) == [
        1,
        "Current Account",
        "Mortgage / Rent",
        "Green Valley Rentals",
        "-950.00",
        "Monthly",
        "Rent",
        "2026-10-01",
        "monthly rent",
        "Yes",
    ]


def test_day_of_month_comes_from_next_date_and_income_stays_positive():
    row = schedule_row(schedule(next_date="2026-11-28", amount=2500))
    assert row[0] == 28 and row[4] == "2500.00"


def test_inactive_schedule_and_bad_date():
    row = schedule_row(schedule(active=0, next_date="not-a-date"))
    assert row[0] == "" and row[9] == "No"


def test_negative_zero_amount_written_as_zero():
    assert schedule_row(schedule(amount=-0.001))[4] == "0.00"


def test_write_and_read_back_with_awkward_text(tmp_path):
    path = tmp_path / "out.csv"
    rows = [
        schedule(payee='Smith, "Bob" & Sons', memo="line one\nline two", name="Café £"),
        schedule(name="Salary", amount=2500.0, category_name="Salary", next_date="2026-10-15"),
    ]
    assert write_schedules_csv(path, rows) == 2

    assert path.read_bytes().startswith(b"\xef\xbb\xbf")  # BOM for Excel
    back = read_back(path)
    assert [r["Payee"] for r in back][0] == 'Smith, "Bob" & Sons'
    assert back[0]["Memo"] == "line one\nline two"
    assert back[0]["Name"] == "Café £"
    assert back[1]["Day of Month"] == "15" and back[1]["Amount"] == "2500.00"


def test_empty_export_still_has_header(tmp_path):
    path = tmp_path / "empty.csv"
    assert write_schedules_csv(path, []) == 0
    assert read_back(path) == []
    assert path.read_text(encoding="utf-8-sig").splitlines()[0] == ",".join(HEADERS)


def test_exports_real_database(tmp_path):
    pytest.importorskip("tkinter")
    from simplefinance.app import FinanceDB

    db = FinanceDB(tmp_path / "finance.db")
    db.add_account("Current Account", "Current", 0.0)
    account_id = db.conn.execute("SELECT id FROM accounts").fetchone()["id"]
    cats = {r["name"]: r["id"] for r in db.conn.execute("SELECT id, name FROM categories")}
    db.add_schedule("Rent", account_id, cats["Mortgage / Rent"], "Landlord", "the memo", 950.0, "Monthly", "2026-10-01")
    db.add_schedule("Salary", account_id, cats["Salary"], "Acme", "", 2500.0, "Monthly", "2026-10-25")

    path = tmp_path / "sched.csv"
    assert write_schedules_csv(path, db.get_schedules()) == 2

    back = {r["Name"]: r for r in read_back(path)}
    # Stored sign is category-driven: Expense negative, Income positive
    assert back["Rent"]["Amount"] == "-950.00" and back["Rent"]["Memo"] == "the memo"
    assert back["Salary"]["Amount"] == "2500.00"
    assert back["Rent"]["Category"] == "Mortgage / Rent"
    assert back["Salary"]["Day of Month"] == "25"
