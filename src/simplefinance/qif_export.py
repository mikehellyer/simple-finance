"""Export Simple Finance data as a QIF file that Moneydance can import.

QIF is the one format Moneydance imports that carries accounts, categories,
transactions, transfers between accounts and opening balances. It cannot
represent Scheduled Transactions, Budgetary Transactions or Scenario Sheets,
so those are not exported.

Moneydance's importer notes that shaped this file:
- QIF is an ASCII format; non-ASCII text is corrupted on import, so every
  free-text field is reduced to plain ASCII here.
- An account's balance is only right if an opening-balance entry is the first
  transaction in that account (Quicken convention: payee "Opening Balance",
  category "[<the account itself>]").
- Both sides of a transfer are exported with the same date so Moneydance can
  match them into one transfer instead of duplicating it.
- "/" in a category is read as a class separator and ":" as a sub-category
  separator, and "[...]" marks a transfer, so those characters are replaced
  in category and account names.

This module has no Tkinter dependency so it can be unit tested directly.
"""

import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

NEWLINE = "\r\n"

_ACCOUNT_TYPES = {
    "Current": "Bank",
    "Savings": "Bank",
    "Cash": "Cash",
    "Credit Card": "CCard",
    "Other": "Oth A",
}
_DEFAULT_ACCOUNT_TYPE = "Bank"

_TRANSLATIONS = {
    0x00A3: "GBP",  # pound sign
    0x20AC: "EUR",
    0x2013: "-",
    0x2014: "-",
    0x2018: "'",
    0x2019: "'",
    0x201C: '"',
    0x201D: '"',
    0x2026: "...",
    0x00A0: " ",
}

_NAME_REPLACEMENTS = (("/", "-"), (":", "-"), ("[", "("), ("]", ")"))


@dataclass
class QifExport:
    text: str
    account_count: int
    category_count: int
    transaction_count: int
    transfer_count: int
    renames: list = field(default_factory=list)


def _ascii(value):
    """Plain single-line ASCII: accents dropped, other non-ASCII becomes '?'."""
    text = str(value or "").translate(_TRANSLATIONS)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.encode("ascii", "replace").decode("ascii")
    text = "".join(" " if ord(ch) < 32 or ord(ch) == 127 else ch for ch in text)
    return text.strip()


def _name_label(name):
    """An account or category name made safe for QIF's special characters."""
    text = _ascii(name)
    for bad, good in _NAME_REPLACEMENTS:
        text = text.replace(bad, good)
    return text.strip()


def _qif_date(value):
    d = value if isinstance(value, date) else date.fromisoformat(str(value))
    return f"{d.month:02d}/{d.day:02d}/{d.year:04d}"


def _qif_amount(value):
    rounded = round(float(value), 2) + 0.0  # + 0.0 turns -0.0 into 0.0
    return f"{rounded:.2f}"


def build_qif(accounts, categories, transactions, today=None):
    """Build the QIF text for the given data.

    accounts:     dicts with id, name, account_type, opening_balance
    categories:   dicts with id, name, category_type ("Income" or "Expense")
    transactions: dicts with id, txn_date (ISO), account_id, category_id,
                  payee, memo, amount, transfer_group, reconciled
    """
    today = today or date.today()

    account_labels = {a["id"]: _name_label(a["name"]) for a in accounts}
    category_labels = {c["id"]: _name_label(c["name"]) for c in categories}

    renames = []
    for a in accounts:
        if account_labels[a["id"]] != a["name"]:
            renames.append(("Account", a["name"], account_labels[a["id"]]))
    for c in categories:
        if category_labels[c["id"]] != c["name"]:
            renames.append(("Category", c["name"], category_labels[c["id"]]))

    # A transfer is exported as such only when both of its legs are present
    # in different accounts; otherwise it falls back to a plain transaction.
    legs_by_group = defaultdict(list)
    for t in transactions:
        if t.get("transfer_group"):
            legs_by_group[t["transfer_group"]].append(t)

    def transfer_partner(txn):
        legs = legs_by_group.get(txn.get("transfer_group"))
        if not legs or len(legs) != 2:
            return None
        other = legs[0] if legs[1] is txn else legs[1]
        if other["account_id"] == txn["account_id"]:
            return None
        return other

    by_account = defaultdict(list)
    for t in transactions:
        by_account[t["account_id"]].append(t)

    lines = []

    lines.append("!Type:Cat")
    seen_categories = set()
    for c in categories:
        label = category_labels[c["id"]]
        if not label or label in seen_categories:
            continue
        seen_categories.add(label)
        lines.append(f"N{label}")
        lines.append("I" if c["category_type"] == "Income" else "E")
        lines.append("^")

    def account_record(account):
        return [
            "!Account",
            f"N{account_labels[account['id']]}",
            f"T{_ACCOUNT_TYPES.get(account['account_type'], _DEFAULT_ACCOUNT_TYPE)}",
            "^",
        ]

    lines.append("!Option:AutoSwitch")
    for account in accounts:
        record = account_record(account)
        # Inside the AutoSwitch list only the first record carries "!Account".
        lines.extend(record if account is accounts[0] else record[1:])
    lines.append("!Clear:AutoSwitch")

    transaction_count = 0
    transfer_pairs = 0

    for account in accounts:
        label = account_labels[account["id"]]
        qif_type = _ACCOUNT_TYPES.get(account["account_type"], _DEFAULT_ACCOUNT_TYPE)
        rows = sorted(
            by_account.get(account["id"], []), key=lambda t: (t["txn_date"], t["id"])
        )

        lines.extend(account_record(account))
        lines.append(f"!Type:{qif_type}")

        opening = float(account["opening_balance"] or 0.0)
        if abs(opening) >= 0.005:
            if rows:
                opening_date = date.fromisoformat(rows[0]["txn_date"]) - timedelta(days=1)
            else:
                opening_date = today
            lines.append(f"D{_qif_date(opening_date)}")
            lines.append(f"T{_qif_amount(opening)}")
            lines.append("POpening Balance")
            lines.append(f"L[{label}]")
            lines.append("^")

        for txn in rows:
            transaction_count += 1
            lines.append(f"D{_qif_date(txn['txn_date'])}")
            lines.append(f"T{_qif_amount(txn['amount'])}")

            payee = _ascii(txn.get("payee"))
            if payee:
                lines.append(f"P{payee}")
            memo = _ascii(txn.get("memo"))
            if memo:
                lines.append(f"M{memo}")

            partner = transfer_partner(txn)
            if partner is not None:
                lines.append(f"L[{account_labels[partner['account_id']]}]")
                if txn["amount"] < 0:
                    transfer_pairs += 1
            elif txn.get("category_id") in category_labels:
                category = category_labels[txn["category_id"]]
                if category:
                    lines.append(f"L{category}")

            if txn.get("reconciled"):
                lines.append("CX")
            lines.append("^")

    return QifExport(
        text=NEWLINE.join(lines) + NEWLINE,
        account_count=len(accounts),
        category_count=len(seen_categories),
        transaction_count=transaction_count,
        transfer_count=transfer_pairs,
        renames=renames,
    )


def write_qif(path, export):
    """Write an export to disk. The text is pure ASCII with CRLF line endings
    already in place, so no newline translation or encoding surprises."""
    with open(path, "w", encoding="ascii", newline="") as handle:
        handle.write(export.text)
