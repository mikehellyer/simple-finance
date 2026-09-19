from datetime import date

import pytest

from simplefinance.qif_export import build_qif, write_qif

TODAY = date(2026, 9, 19)


def parse(text):
    """Minimal QIF reader: list of (section header, {field letter: value})."""
    records = []
    section = None
    fields = {}
    for line in text.split("\r\n"):
        if not line:
            continue
        if line.startswith("!"):
            section = line
        elif line == "^":
            records.append((section, fields))
            fields = {}
        else:
            fields[line[0]] = line[1:]
    return records


def records_in(text, section):
    return [f for s, f in parse(text) if s == section]


def account(id_, name, type_="Current", opening=0.0):
    return {"id": id_, "name": name, "account_type": type_, "opening_balance": opening}


def category(id_, name, type_="Expense"):
    return {"id": id_, "name": name, "category_type": type_}


def txn(id_, day, account_id, amount, **kw):
    row = {
        "id": id_,
        "txn_date": day,
        "account_id": account_id,
        "category_id": None,
        "payee": "",
        "memo": "",
        "amount": amount,
        "transfer_group": None,
        "reconciled": 0,
    }
    row.update(kw)
    return row


def test_categories_are_typed_and_made_safe():
    cats = [
        category(1, "Salary", "Income"),
        category(2, "Mortgage / Rent"),
        category(3, "Home: Repairs"),
        category(4, "[Odd]"),
    ]
    export = build_qif([account(1, "Current")], cats, [], today=TODAY)
    cat_records = records_in(export.text, "!Type:Cat")

    assert [r["N"] for r in cat_records] == [
        "Salary",
        "Mortgage - Rent",
        "Home- Repairs",
        "(Odd)",
    ]
    assert "I" in cat_records[0] and "E" not in cat_records[0]
    assert "E" in cat_records[1] and "I" not in cat_records[1]
    assert export.category_count == 4
    assert ("Category", "Mortgage / Rent", "Mortgage - Rent") in export.renames


def test_account_list_and_type_mapping():
    accounts = [
        account(1, "Current", "Current"),
        account(2, "Rainy Day", "Savings"),
        account(3, "Wallet", "Cash"),
        account(4, "Visa", "Credit Card"),
        account(5, "House", "Other"),
    ]
    export = build_qif(accounts, [], [], today=TODAY)
    text = export.text

    assert "!Option:AutoSwitch" in text and "!Clear:AutoSwitch" in text
    # Account list first (only the first record carries the !Account header)
    account_list = text.split("!Option:AutoSwitch\r\n")[1].split("!Clear:AutoSwitch")[0]
    assert account_list.startswith("!Account\r\nNCurrent\r\nTBank\r\n^\r\n")
    assert account_list.count("!Account") == 1

    types = {}
    for section, fields in parse(text):
        if section == "!Account" and "T" in fields:
            types[fields["N"]] = fields["T"]
    assert types == {
        "Current": "Bank",
        "Rainy Day": "Bank",
        "Wallet": "Cash",
        "Visa": "CCard",
        "House": "Oth A",
    }
    for header in ("!Type:Bank", "!Type:Cash", "!Type:CCard", "!Type:Oth A"):
        assert header in text
    assert export.account_count == 5


def test_opening_balance_is_first_and_dated_before_earliest_transaction():
    accounts = [account(1, "Current", opening=250.5)]
    txns = [txn(2, "2026-03-05", 1, -10.0), txn(1, "2026-03-01", 1, 20.0)]
    records = records_in(build_qif(accounts, [], txns, today=TODAY).text, "!Type:Bank")

    assert records[0] == {
        "D": "02/28/2026",
        "T": "250.50",
        "P": "Opening Balance",
        "L": "[Current]",
    }
    assert [r["D"] for r in records[1:]] == ["03/01/2026", "03/05/2026"]


def test_zero_opening_balance_omitted_and_empty_account_uses_today():
    zero = build_qif([account(1, "Current", opening=0.0)], [], [], today=TODAY)
    assert records_in(zero.text, "!Type:Bank") == []

    empty = build_qif([account(1, "Current", opening=99.0)], [], [], today=TODAY)
    assert records_in(empty.text, "!Type:Bank")[0]["D"] == "09/19/2026"


def test_transaction_fields():
    accounts = [account(1, "Current")]
    cats = [category(1, "Groceries")]
    txns = [
        txn(
            1,
            "2026-09-01",
            1,
            -45.2,
            category_id=1,
            payee="Tesco Stores",
            memo="weekly shop",
            reconciled=1,
        ),
        txn(2, "2026-09-02", 1, 12.0),
    ]
    export = build_qif(accounts, cats, txns, today=TODAY)
    first, second = records_in(export.text, "!Type:Bank")

    assert first == {
        "D": "09/01/2026",
        "T": "-45.20",
        "P": "Tesco Stores",
        "M": "weekly shop",
        "L": "Groceries",
        "C": "X",
    }
    assert second == {"D": "09/02/2026", "T": "12.00"}
    assert export.transaction_count == 2


def test_transfer_legs_reference_each_other_with_matching_dates():
    accounts = [account(1, "Current"), account(2, "Savings", "Savings")]
    txns = [
        txn(1, "2026-09-10", 1, -100.0, payee="Transfer to Savings", transfer_group="g1"),
        txn(2, "2026-09-10", 2, 100.0, payee="Transfer from Current", transfer_group="g1"),
    ]
    export = build_qif(accounts, [], txns, today=TODAY)
    out_leg = records_in(export.text, "!Type:Bank")
    assert len(out_leg) == 2  # Current and Savings are both Bank type

    current, savings = out_leg
    assert current["L"] == "[Savings]" and current["T"] == "-100.00"
    assert savings["L"] == "[Current]" and savings["T"] == "100.00"
    assert current["D"] == savings["D"] == "09/10/2026"
    assert export.transfer_count == 1
    assert export.transaction_count == 2


def test_orphaned_transfer_leg_falls_back_to_plain_transaction():
    accounts = [account(1, "Current"), account(2, "Savings")]
    txns = [txn(1, "2026-09-10", 1, -100.0, payee="Transfer to Savings", transfer_group="g1")]
    export = build_qif(accounts, [], txns, today=TODAY)
    record = records_in(export.text, "!Type:Bank")[0]

    assert "L" not in record
    assert export.transfer_count == 0


def test_output_is_ascii_crlf_and_single_line_fields():
    accounts = [account(1, "Café Account")]
    txns = [
        txn(
            1,
            "2026-09-01",
            1,
            -5.0,
            payee="Café £5 deal \U0001F600",
            memo="line one\nline two\ttabbed",
        )
    ]
    export = build_qif(accounts, [], txns, today=TODAY)

    export.text.encode("ascii")  # raises if any non-ASCII slipped through
    assert "\n" not in export.text.replace("\r\n", "")
    record = records_in(export.text, "!Type:Bank")[0]
    assert record["P"] == "Cafe GBP5 deal ?"
    assert record["M"] == "line one line two tabbed"
    assert ("Account", "Café Account", "Cafe Account") in export.renames
    assert export.text.endswith("\r\n")


def test_negative_zero_amount_is_written_as_zero():
    export = build_qif([account(1, "Current")], [], [txn(1, "2026-09-01", 1, -0.001)], today=TODAY)
    assert records_in(export.text, "!Type:Bank")[0]["T"] == "0.00"


def test_write_qif_round_trips_bytes(tmp_path):
    export = build_qif([account(1, "Current")], [], [txn(1, "2026-09-01", 1, 1.0)], today=TODAY)
    path = tmp_path / "out.qif"
    write_qif(path, export)

    raw = path.read_bytes()
    assert raw.decode("ascii") == export.text
    assert b"\r\r" not in raw  # no doubled carriage returns


def test_exports_real_database(tmp_path):
    pytest.importorskip("tkinter")
    from simplefinance.app import FinanceDB

    db = FinanceDB(tmp_path / "finance.db")
    db.add_account("Current Account", "Current", 1000.0)
    db.add_account("Savings", "Savings", 0.0)
    ids = {r["name"]: r["id"] for r in db.conn.execute("SELECT id, name FROM accounts")}
    cats = {r["name"]: r["id"] for r in db.conn.execute("SELECT id, name FROM categories")}

    db.add_transaction("2026-09-01", ids["Current Account"], cats["Groceries"], "Tesco", "", -30.0)
    db.add_transaction("2026-09-02", ids["Current Account"], cats["Salary"], "Acme", "", 500.0)
    db.add_transfer("2026-09-03", ids["Current Account"], ids["Savings"], 200.0, "to savings")

    accounts, categories, transactions = db.get_export_data()
    export = build_qif(accounts, categories, transactions, today=TODAY)

    assert export.account_count == 2
    assert export.transaction_count == 4
    assert export.transfer_count == 1

    current = records_in(export.text, "!Type:Bank")[: 1 + 3]
    assert current[0]["P"] == "Opening Balance" and current[0]["T"] == "1000.00"
    assert [r["D"] for r in current[1:]] == ["09/01/2026", "09/02/2026", "09/03/2026"]
    assert current[1]["L"] == "Groceries"
    assert current[3]["L"] == "[Savings]"
    export.text.encode("ascii")
