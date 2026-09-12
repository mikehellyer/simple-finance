#!/usr/bin/env python3
"""
Simple Finance
Version 0.10.12

A lightweight Moneydance-style personal finance program for Linux using
only Python's standard library: Tkinter + SQLite.

Version 0.10.12:
- No functional change - test release to confirm the 0.10.11 red banner
  styling and auto-quit-after-update behaviour work on a real install

Version 0.10.11 improves the update banner:
- Banner text and the Update button are now red so the notification is
  harder to miss
- Clicking Update now quits Simple Finance after opening the downloaded
  installer, instead of leaving the running app blocking its own
  replacement in Applications/Program Files

Version 0.10.10:
- No functional change - test release to confirm the 0.10.9 update-checker
  fix actually surfaces a real update banner on a real installed build

Version 0.10.9 fixes:
- The update checker never actually worked on the built macOS installer -
  the frozen app had no usable CA certificate bundle, so every HTTPS check
  failed with a certificate error, which was silently treated the same as
  "GitHub unreachable" (by design, so it never disrupts normal app use)
- Bundles certifi's CA bundle with the app and points the update checker's
  HTTPS requests at it explicitly, instead of relying on whatever the build
  environment happened to provide

Version 0.10.8 fixes:
- The GitHub repo backing the update checker was renamed from
  mikehellyer/finance to mikehellyer/simple-finance; the app now polls the
  new name directly instead of relying on GitHub's rename redirect

Version 0.10.7 fixes:
- Scheduled and Budgetary transactions created before the amount sign was
  derived from category type could still show the raw sign originally typed
- Existing rows are now normalised (Expense -> negative, Income -> positive)
  automatically on startup, matching rows added or edited since
- Cosmetic only - forecasts and schedule processing already computed the
  correct sign from category type independently

Version 0.10.6 improves OFX importing:
- Selected Likely/Possible manual matches can replace their existing manual Account Transaction
- Replacement updates the existing transaction in place rather than creating a duplicate
- Preserves transaction ID, category, scheduled link and reconciliation state
- Applies the OFX date, payee, memo, amount, FITID/external ID and import source
- Adds Select Likely Manual for quick multi-selection
- Import button reports how many rows are new imports vs replacements
- Exact OFX duplicates remain protected
- Linked transfer rows are excluded from replacement matching

Version 0.10.5 fixes:
- Applies the safe double-click edit pattern across the other editable lists
- Scheduled Transactions now edit the exact row double-clicked
- Budgetary Transactions now edit the exact row double-clicked
- Budgetary Transactions shown on the 6 Month Budget tab use the same safe edit path
- Categories now edit the exact row double-clicked
- These edit dialogs build completely before becoming modal, preventing blank square windows
- Missing/deleted rows are checked before edit dialogs open

Version 0.10.4 fixes:
- Double-click editing in Account Transactions now targets the exact row under the mouse
- Prevents stale Treeview selection from opening the wrong/non-existent transaction
- Edit Transaction dialog now builds completely before becoming modal
- Transaction lookup is validated before the edit window is opened
- Any unexpected dialog-construction error is cleaned up instead of leaving a blank Edit transaction window

Version 0.10.3 improves reconciliation usability:
- Adds a prominent overall reconciliation status box
- Shows PDF VERIFIED / PDF CHECK REQUIRED
- Shows matched statement rows, remaining rows and readiness at a glance
- Final reconciliation button is disabled until all required checks pass
- Main Account Transactions Reconciled column now displays a clear tick (✓)
- Completion message confirms how many Account Transactions were marked reconciled

Version 0.10.2 fixes:
- RBS transaction dates are now parsed from the real left edge rather than the indented header position
- Correctly preserves 10/11/12/25/26/27/28 AUG dates instead of losing their first digit
- Foreign-currency amounts and exchange rates inside descriptions are no longer mistaken for Paid In/Withdrawn values
- Stops transaction parsing when the RBS interest/overdraft information section begins
- BROUGHT FORWARD is reliably excluded from transaction rows
- Added independent PDF summary validation for total Paid In and total Withdrawn
- Uses the PDF's stated Period Covered dates for reconciliation and ledger checks
- Tested against the complete six-page RBS Reward Platinum statement supplied for development

Version 0.10.1 improves:
- Added a fixed-column PDF parser for RBS/NatWest-style statements
- Correctly reads Date / Description / Paid In / Withdrawn / Balance columns
- Transactions with a blank date inherit the previous printed transaction date
- Multi-line descriptions are joined before the transaction is created
- BROUGHT FORWARD is treated as the opening running balance, not a transaction
- The statement running balance is used to validate and, where necessary, correct each parsed amount
- Reconciliation screen now includes a PDF Check column for row-by-row balance validation

Version 0.10.0 adds:
- PDF bank statement reconciliation workflow
- Extracts text from normal text-based PDF statements using pdftotext/Poppler
- Reviews and edits parsed statement transactions before reconciliation
- Matches PDF transactions to existing Account Transactions with fuzzy dates/descriptions
- Matched, possible, missing and already-reconciled rows are colour highlighted
- Checks statement opening + activity = statement closing balance
- Shows reconciliation difference and unmatched account entries
- Lets missing statement transactions be added to Account Transactions
- Lets ambiguous matches be manually confirmed or changed
- Saves reconciliation history and marks matched transactions as reconciled
- Account Transactions now has a visible Reconciled column

Version 0.9.5 improves:
- Manual OFX matching now searches up to 4 days either side of the bank posting date
- Exact amount is treated as the strongest manual-match clue
- Description/payee matching is now supporting evidence rather than a strict requirement
- Unique nearby amount matches can be marked Likely manual even when wording differs substantially
- Matching is one-to-one so one manual transaction cannot hide several OFX transactions
- Ambiguous repeated amounts remain marked Possible manual
- OFX preview shows the matched manual transaction date

Version 0.9.4 adds:
- OFX preview now detects transactions that may already exist as manual Account Transactions
- Likely manual matches are highlighted in yellow
- Possible date/amount manual matches are highlighted in orange
- Exact OFX duplicates remain marked Already imported
- Only genuinely New transactions are selected automatically
- Manual matches can still be selected deliberately if they are separate transactions

Version 0.9.3 changes:
- The Simple Finance icon now appears inside the program header
- The header icon is shown at the top-left beside the program name
- Uses the same custom icon as the desktop shortcut and running-window icon

Version 0.9.2 fixes:
- Last-used Scenario Sheet now reopens automatically when Simple Finance starts
- If that scenario was deleted, the first remaining saved scenario loads automatically
- Scenario selection is remembered by database ID, so renaming a scenario is safe
- Replaced the pop-up scenario drop-down with an embedded Saved Scenarios list inside the program window

Version 0.9.1 changes:
- Scenario Sheet rows with a negative running balance are highlighted in red
- Negative carried balances on month heading rows are highlighted too

Version 0.9.0 adds:
- Built-in editable Scenario Sheet for the six-month budget
- Copy the current projection into a named scenario without changing real finance data
- Six months arranged vertically like a financial transaction sheet
- Eight spare editable rows are added to every month
- Edit Date, Description, Income and Spending directly by double-clicking cells
- Balance is recalculated and displayed on every row
- Save multiple independent scenarios
- Insert, clear and delete scenario rows
- Export a scenario to CSV for LibreOffice Calc

Version 0.8.4 changes:
- Running Simple Finance window now uses the custom application icon
- Linux window class is now SimpleFinance instead of generic Tk
- Desktop launcher can correctly associate the running window with Simple Finance
- Installer places the icon beside the application as well as in the icon theme

Version 0.8.3 changes:
- Renamed Account Register tab to Account Transactions
- Reordered Scheduled and Categories tabs
- Categories now sits immediately to the left of Backup & Restore

Version 0.8.2 adds:
- Edit existing categories
- Double-click a category to edit it
- Rename categories safely
- Change a category between Expense and Income
- Future Scheduled and Budgetary transactions automatically follow the new category type
- Category deletion now also protects categories used by Budgetary Transactions

Version 0.8.1 adds:
- Edit existing scheduled transactions
- Double-click a schedule to edit it
- Change name, account, category, payee, amount, frequency, next date and memo
- Edited schedules update the Six Month Budget immediately

Version 0.8.0 adds:
- Settings tab
- UK DD/MM/YYYY date format is now the default
- Optional ISO YYYY-MM-DD and US MM/DD/YYYY display/input formats
- Date-format setting is stored in the finance database and included in backups
- All visible transaction, schedule, budget and OFX dates follow the setting
- Dates remain stored internally in ISO format for reliability

Version 0.7.0 adds:
- Backup & Restore tab
- Manual full-database backups
- Automatic startup backups
- Automatic safety backup before restore
- Backup validation before recovery
- Retains the 10 most recent automatic backups

Version 0.6.0 adds:
- Dedicated Budgetary Transactions tab
- Forecast-only income and spending entries
- Account, Category, Payee, Amount, Frequency, Next Date and optional End Date
- Add, edit and delete budgetary transactions
- Budgetary transactions never post into the real Account Register
- Six Month Budget combines Scheduled + Budgetary transactions automatically

Version 0.5.1 fixes:
- Scheduled Expense categories now project as money out
- Scheduled Income categories now project as money in
- Existing positive-valued expense schedules no longer inflate the forecast
- Future scheduled transaction processing respects category type

Version 0.5.0 adds:
- Six Month Budget projection tab
- Uses the selected account's current balance as the projection starting point
- Includes scheduled transactions automatically
- Separate editable projection-only Budget Items
- One-off, weekly, monthly and yearly Budget Items
- Optional end dates for temporary budget items
- Six-month income, spending and closing-balance summary
- Month detail view with projected running balance

Version 0.4.4 changes:
- Account Register now displays newest transactions first
- Running balances remain calculated correctly

Version 0.4.3 adds:
- Edit existing account details
- Change account name
- Change account type
- Change opening / starting balance
- Running and current balances recalculate automatically

Version 0.4.2 adds:
- Select exactly which OFX/QFX transactions to import
- All new bank transactions are selected by default
- Select All New and Clear Selection controls
- Import totals update to match the current selection
- Already-imported OFX transactions remain protected from re-import

Version 0.4.1 fixes:
- Multi-selection deletion in the Account Register
- Select All button and Ctrl+A support
- Safe bulk deletion of ordinary transactions and linked transfers

Version 0.4.0 adds:
- OFX/QFX bank statement import for ordinary transactions
- Bank statement preview before import
- Choose the destination Simple Finance account
- OFX FITID duplicate protection
- Re-importing an overlapping statement skips transactions already imported
- Supports both OFX 1.x (SGML) and OFX 2.x (XML-style) bank files

Version 0.3.4 added:
- CSV import for ordinary transactions
- Transaction CSV template creation

Version 0.3.3 adds:
- Calendar date picker for transfers
- Calendar date picker for scheduled transaction Next Date
- Consistent date selection throughout the program

Version 0.3.2 adds:
- Calendar date picker when adding/editing transactions
- Previous/next month navigation and Today shortcut

Version 0.3.1 adds:
- More forgiving CSV account/category matching (dash and whitespace variants)

Version 0.3 adds:
- CSV import for scheduled transactions
- CSV template creation
- Validation of account/category/day/amount/frequency before import
- Automatic calculation of the first next due date from Day of Month

Version 0.2 features retained:
- Moneydance-style account register
- Payment / Deposit columns
- Running balance
- Account register filtering
- Edit existing transactions
- Account-to-account transfers
- Double-click an account to open its register
- Existing databases remain compatible

Existing features:
- Accounts
- Categories
- Transactions
- Scheduled recurring transactions
- Automatic processing of due scheduled transactions on startup
- Persistent SQLite database
"""

import calendar
import csv
import hashlib
import html
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import uuid
import unicodedata
import webbrowser
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

from simplefinance import paths
from simplefinance.version import __version__, GITHUB_REPO
from simplefinance.updater import (
    UpdateChecker,
    download_asset,
    open_installer,
    pick_asset_for_platform,
)

APP_NAME = "Simple Finance"
APP_VERSION = __version__

DATE_FORMATS = {
    "UK": {
        "label": "UK (DD/MM/YYYY)",
        "strftime": "%d/%m/%Y",
        "example": "06/09/2026",
    },
    "ISO": {
        "label": "ISO (YYYY-MM-DD)",
        "strftime": "%Y-%m-%d",
        "example": "2026-09-06",
    },
    "US": {
        "label": "US (MM/DD/YYYY)",
        "strftime": "%m/%d/%Y",
        "example": "09/06/2026",
    },
}


def money(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}£{abs(value):,.2f}"


def parse_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%Y-%m-%d").date()


def add_months(d: date, months: int = 1) -> date:
    month_index = (d.month - 1) + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def advance_date(d: date, frequency: str) -> date:
    if frequency == "Daily":
        return d + timedelta(days=1)
    if frequency == "Weekly":
        return d + timedelta(days=7)
    if frequency == "Monthly":
        return add_months(d, 1)
    if frequency == "Yearly":
        try:
            return d.replace(year=d.year + 1)
        except ValueError:
            return d.replace(year=d.year + 1, day=28)
    raise ValueError(f"Unknown frequency: {frequency}")


def date_for_day_in_month(year: int, month: int, day_of_month: int) -> date:
    """Return a valid date, using the month's last day when needed."""
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day_of_month, last_day))


def first_due_date_from_day(day_of_month: int, today=None) -> date:
    """
    Find the next occurrence of a day-of-month, including today.

    For example, if today is 6 Sep and the imported day is 5, the first
    due date will be 5 Oct. If the imported day is 20 it will be 20 Sep.
    Day 29-31 is clamped to the final day of shorter months.
    """
    today = today or date.today()
    candidate = date_for_day_in_month(today.year, today.month, day_of_month)
    if candidate >= today:
        return candidate

    next_month = add_months(date(today.year, today.month, 1), 1)
    return date_for_day_in_month(next_month.year, next_month.month, day_of_month)


def decode_ofx_bytes(data: bytes) -> str:
    """
    Decode an OFX/QFX file.

    OFX 1.x often uses an ASCII-style header with CHARSET:1252, while
    OFX 2.x is normally XML/UTF-8. Try the declared charset first and
    then safe fallbacks commonly used by UK banks.
    """
    header_probe = data[:4096].decode("latin-1", errors="ignore")
    match = re.search(r"(?im)^\s*CHARSET\s*:\s*([^\r\n]+)", header_probe)
    declared = match.group(1).strip().upper() if match else ""

    candidates = []
    if declared:
        if declared in {"1252", "WINDOWS-1252", "CP1252"}:
            candidates.append("cp1252")
        elif declared in {"UTF-8", "UTF8"}:
            candidates.append("utf-8-sig")
        elif declared in {"ISO-8859-1", "8859-1", "LATIN1", "LATIN-1"}:
            candidates.append("latin-1")

    candidates.extend(["utf-8-sig", "cp1252", "latin-1"])

    seen = set()
    for encoding in candidates:
        if encoding in seen:
            continue
        seen.add(encoding)
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass

    return data.decode("latin-1", errors="replace")


def ofx_tag_value(block: str, tag: str) -> str:
    """
    Read a leaf value from either XML-style OFX or OFX 1.x SGML.

    In OFX 1.x, leaf tags often do not have explicit closing tags:
        <NAME>SHOP NAME
    so the value is read up to the next '<' or line break.
    """
    match = re.search(
        rf"<{re.escape(tag)}\b[^>]*>\s*([^<\r\n]*)",
        block,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    return html.unescape(match.group(1).strip())


def parse_ofx_date(value: str) -> date:
    """Extract YYYYMMDD from common OFX timestamp forms."""
    match = re.search(r"(\d{4})(\d{2})(\d{2})", value or "")
    if not match:
        raise ValueError(f'Invalid OFX date "{value}"')
    return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))


def mask_bank_account(account_id: str) -> str:
    value = (account_id or "").strip()
    if not value:
        return "Unknown account"
    if len(value) <= 4:
        return value
    return "••••" + value[-4:]


def parse_ofx_file(path):
    """
    Parse bank and credit-card statements from OFX/QFX using only the
    Python standard library.

    Returns a list of statement dictionaries. Each statement contains
    its source account details and a list of transactions.
    """
    data = Path(path).read_bytes()
    text = decode_ofx_bytes(data)

    # Bank statements and credit-card statements use different aggregate tags.
    blocks = []
    for kind, tag in (("Bank", "STMTRS"), ("Credit Card", "CCSTMTRS")):
        for match in re.finditer(
            rf"<{tag}\b[^>]*>(.*?)</{tag}>",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            blocks.append((kind, match.group(1)))

    # Some files are imperfect but still contain STMTTRN aggregates.
    # Treat the whole OFX document as one statement as a fallback.
    if not blocks and re.search(r"<STMTTRN\b", text, flags=re.IGNORECASE):
        blocks.append(("Bank", text))

    if not blocks:
        raise ValueError(
            "No bank transactions were found in this OFX/QFX file."
        )

    statements = []

    for statement_index, (kind, block) in enumerate(blocks, start=1):
        account_id = ofx_tag_value(block, "ACCTID")
        bank_id = ofx_tag_value(block, "BANKID")
        account_type = ofx_tag_value(block, "ACCTTYPE")
        currency = ofx_tag_value(block, "CURDEF") or "GBP"
        dt_start_raw = ofx_tag_value(block, "DTSTART")
        dt_end_raw = ofx_tag_value(block, "DTEND")
        balance_raw = ofx_tag_value(block, "BALAMT")

        start_date = None
        end_date = None
        try:
            if dt_start_raw:
                start_date = parse_ofx_date(dt_start_raw)
        except ValueError:
            pass
        try:
            if dt_end_raw:
                end_date = parse_ofx_date(dt_end_raw)
        except ValueError:
            pass

        balance = None
        if balance_raw:
            try:
                balance = float(balance_raw.replace(",", ""))
            except ValueError:
                balance = None

        transactions = []

        for txn_index, txn_match in enumerate(
            re.finditer(
                r"<STMTTRN\b[^>]*>(.*?)</STMTTRN>",
                block,
                flags=re.IGNORECASE | re.DOTALL,
            ),
            start=1,
        ):
            txn_block = txn_match.group(1)

            posted_raw = ofx_tag_value(txn_block, "DTPOSTED")
            amount_raw = ofx_tag_value(txn_block, "TRNAMT")
            fitid = ofx_tag_value(txn_block, "FITID")
            txn_type = ofx_tag_value(txn_block, "TRNTYPE")
            name = ofx_tag_value(txn_block, "NAME")
            memo = ofx_tag_value(txn_block, "MEMO")
            checknum = ofx_tag_value(txn_block, "CHECKNUM")

            if not posted_raw or not amount_raw:
                # A malformed transaction cannot be imported reliably.
                continue

            try:
                posted = parse_ofx_date(posted_raw)
                amount = float(amount_raw.replace(",", ""))
            except (ValueError, TypeError):
                continue

            payee = name.strip() or memo.strip() or txn_type.title() or "Bank transaction"

            # Avoid repeating exactly the same text in Payee and Memo.
            display_memo = memo.strip()
            if display_memo.casefold() == payee.casefold():
                display_memo = ""

            if checknum:
                check_text = f"Ref: {checknum}"
                display_memo = (
                    f"{display_memo} | {check_text}"
                    if display_memo
                    else check_text
                )

            if fitid:
                external_id = "OFX:" + fitid.strip()
            else:
                # FITID is standard OFX, but provide deterministic duplicate
                # protection for banks that omit it.
                fingerprint_source = "|".join(
                    [
                        account_id,
                        posted.isoformat(),
                        f"{amount:.8f}",
                        txn_type,
                        name,
                        memo,
                        checknum,
                    ]
                )
                digest = hashlib.sha256(
                    fingerprint_source.encode("utf-8", errors="replace")
                ).hexdigest()
                external_id = "OFXFP:" + digest

            transactions.append(
                {
                    "txn_date": posted.isoformat(),
                    "amount": amount,
                    "payee": payee,
                    "memo": display_memo,
                    "txn_type": txn_type or "",
                    "fitid": fitid or "",
                    "external_id": external_id,
                    "source_order": txn_index,
                }
            )

        if not transactions:
            continue

        transactions.sort(
            key=lambda row: (row["txn_date"], row["source_order"])
        )

        source_label = f"{kind} {mask_bank_account(account_id)}"
        if account_type:
            source_label += f" ({account_type})"

        statements.append(
            {
                "kind": kind,
                "account_id": account_id,
                "bank_id": bank_id,
                "account_type": account_type,
                "currency": currency.upper(),
                "start_date": start_date.isoformat() if start_date else "",
                "end_date": end_date.isoformat() if end_date else "",
                "ledger_balance": balance,
                "source_label": source_label,
                "transactions": transactions,
                "statement_index": statement_index,
            }
        )

    if not statements:
        raise ValueError(
            "The OFX/QFX file was recognised, but no usable transactions were found."
        )

    return statements


def month_start(d: date) -> date:
    return date(d.year, d.month, 1)


def month_end(d: date) -> date:
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])


def projection_dates(first_date: date, frequency: str, from_date: date, to_date: date, end_date=None):
    """
    Generate occurrence dates for a scheduled/budget item inside a projection window.
    """
    if first_date > to_date:
        return []

    if end_date is not None and first_date > end_date:
        return []

    if frequency == "One-off":
        if from_date <= first_date <= to_date and (end_date is None or first_date <= end_date):
            return [first_date]
        return []

    current = first_date

    # Bring old projection-only items forward until they reach the visible horizon.
    while current < from_date:
        current = advance_date(current, frequency)
        if end_date is not None and current > end_date:
            return []

    dates = []
    while current <= to_date:
        if end_date is not None and current > end_date:
            break
        dates.append(current)
        current = advance_date(current, frequency)

    return dates


PDF_MONEY_RE = re.compile(
    r"(?:£\s*)?\(?-?\d[\d,]*\.\d{2}\)?\s*(?:CR|DR)?",
    re.IGNORECASE,
)


def parse_statement_money(value):
    raw = (value or "").strip()
    negative = raw.startswith("(") or raw.endswith(")") or bool(
        re.search(r"\bDR\s*$", raw, re.IGNORECASE)
    )
    positive = bool(re.search(r"\bCR\s*$", raw, re.IGNORECASE))
    cleaned = re.sub(r"(?i)\b(?:CR|DR)\b", "", raw)
    cleaned = cleaned.replace("£", "").replace(",", "")
    cleaned = cleaned.replace("(", "").replace(")", "").strip()
    if cleaned.startswith("-"):
        negative = True
    number = abs(float(cleaned))
    if negative:
        return -number, True
    if positive:
        return number, True
    return number, False


def extract_pdf_statement_text(path):
    """Extract text from a text-based PDF statement using Poppler pdftotext."""
    executable = shutil.which("pdftotext")
    if not executable:
        raise ValueError(
            "PDF statement support needs the Poppler 'pdftotext' utility.\n\n"
            "On Ubuntu/Pop!_OS install it with:\n"
            "sudo apt install poppler-utils"
        )

    try:
        result = subprocess.run(
            [executable, "-layout", "-nopgbrk", str(path), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            timeout=45,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError(f"Could not read the PDF statement: {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or "pdftotext returned an error."
        raise ValueError(f"Could not extract text from the PDF.\n\n{detail}")

    extracted = result.stdout.replace("\x0c", "\n")
    if len(re.sub(r"\s+", "", extracted)) < 80:
        raise ValueError(
            "Very little text could be extracted from this PDF. It may be a scanned "
            "image-only statement. This version supports normal searchable/text PDFs; "
            "a scanned statement needs OCR first."
        )
    return extracted


def _statement_default_year(text):
    years = re.findall(r"\b20\d{2}\b", text)
    if not years:
        return date.today().year
    counts = {}
    for value in years:
        year = int(value)
        counts[year] = counts.get(year, 0) + 1
    return max(counts, key=counts.get)


def _parse_statement_date_prefix(line, default_year):
    month_names = {
        name.casefold(): index
        for index, name in enumerate(calendar.month_abbr)
        if name
    }
    month_names.update(
        {
            name.casefold(): index
            for index, name in enumerate(calendar.month_name)
            if name
        }
    )

    patterns = [
        re.compile(r"^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b"),
        re.compile(
            r"^\s*(\d{1,2})\s+([A-Za-z]{3,9})(?:\s+(\d{2,4}))?\b",
            re.IGNORECASE,
        ),
        re.compile(
            r"^\s*(\d{1,2})[-/]([A-Za-z]{3,9})(?:[-/](\d{2,4}))?\b",
            re.IGNORECASE,
        ),
    ]

    match = patterns[0].search(line)
    if match:
        day, month, year = map(int, match.groups())
        if year < 100:
            year += 2000
        try:
            return date(year, month, day), match.end()
        except ValueError:
            return None, None

    for pattern in patterns[1:]:
        match = pattern.search(line)
        if not match:
            continue
        day = int(match.group(1))
        month_text = match.group(2).casefold()
        month = month_names.get(month_text)
        if month is None:
            month = month_names.get(month_text[:3])
        if month is None:
            return None, None
        raw_year = match.group(3)
        year = int(raw_year) if raw_year else default_year
        if year < 100:
            year += 2000
        try:
            return date(year, month, day), match.end()
        except ValueError:
            return None, None

    return None, None


def _find_labeled_statement_balance(text, opening=True):
    if opening:
        phrases = (
            "opening balance",
            "balance brought forward",
            "balance b/f",
            "brought forward",
            "previous balance",
            "starting balance",
        )
    else:
        phrases = (
            "closing balance",
            "balance carried forward",
            "balance c/f",
            "carried forward",
            "new balance",
            "statement balance",
        )

    for line in text.splitlines():
        folded = " ".join(line.casefold().split())
        if not any(phrase in folded for phrase in phrases):
            continue
        tokens = list(PDF_MONEY_RE.finditer(line))
        if not tokens:
            continue
        try:
            amount, _ = parse_statement_money(tokens[-1].group(0))
            return amount
        except ValueError:
            continue
    return None


def _infer_statement_amount(description, raw_amount, explicit_sign):
    if explicit_sign:
        return raw_amount

    folded = (description or "").casefold()
    positive_words = (
        "salary", "wages", "refund", "credit", "deposit", "paid in",
        "payment received", "transfer from", "interest received", "cashback",
    )
    negative_words = (
        "direct debit", "standing order", "card", "purchase", "withdrawal",
        "cash", "fee", "charge", "payment", "transfer to", "debit",
    )
    if any(word in folded for word in positive_words):
        return abs(raw_amount)
    if any(word in folded for word in negative_words):
        return -abs(raw_amount)
    # Most unlabeled everyday statement entries are debits; the review screen
    # lets the user correct any unusual credit that cannot be inferred.
    return -abs(raw_amount)



def _statement_table_header_positions(line):
    """
    Detect a fixed-column statement header such as:

        Date   Description   Paid In(£)   Withdrawn(£)   Balance(£)
    """
    folded = line.casefold()

    date_pos = folded.find("date")
    desc_pos = folded.find("description")
    paid_pos = folded.find("paid in")
    withdrawn_pos = folded.find("withdrawn")
    balance_pos = folded.find("balance")

    positions = (date_pos, desc_pos, paid_pos, withdrawn_pos, balance_pos)
    if any(pos < 0 for pos in positions):
        return None

    if not (date_pos < desc_pos < paid_pos < withdrawn_pos < balance_pos):
        return None

    return {
        "date": date_pos,
        "description": desc_pos,
        "paid_in": paid_pos,
        "withdrawn": withdrawn_pos,
        "balance": balance_pos,
    }


def _find_statement_summary_total(text, label):
    """
    Read a monetary total from the statement summary, e.g.:
        Paid In £10,653.39
        Withdrawn £10,395.49
    """
    wanted = label.casefold()
    for line in text.splitlines():
        folded = " ".join(line.casefold().split())
        if wanted not in folded:
            continue
        tokens = list(PDF_MONEY_RE.finditer(line))
        if not tokens:
            continue
        try:
            amount, _ = parse_statement_money(tokens[-1].group(0))
            return abs(float(amount))
        except (TypeError, ValueError):
            continue
    return None


def _find_statement_period(text):
    """
    Read an RBS-style summary period:
        Period Covered 06 AUG 2026 to 04 SEP 2026
    """
    pattern = re.compile(
        r"period\s+covered\s+"
        r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})\s+to\s+"
        r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None, None

    start, _ = _parse_statement_date_prefix(match.group(1), date.today().year)
    end, _ = _parse_statement_date_prefix(match.group(2), date.today().year)
    return start, end


def _parse_fixed_column_statement_table(text, opening_balance=None, closing_balance=None):
    """
    Parse an RBS/NatWest-style fixed-column transaction table extracted with
    pdftotext -layout.

    The important detail is that monetary values are classified by the START
    POSITION of the number relative to the PDF column headings. Values before
    the Paid In column belong to the description (for example foreign-currency
    amounts and VRATE figures) and must not become transactions.
    """
    cleaned = text.replace("\u00a0", " ")
    lines = cleaned.splitlines()
    default_year = _statement_default_year(cleaned)

    if not any(_statement_table_header_positions(line) for line in lines):
        return None

    rows = []
    warnings = []

    positions = None
    in_table = False
    last_date = None
    previous_running = opening_balance

    pending_date = None
    pending_description = []

    # These mark the end of a transaction table/page. A repeated Date /
    # Description / Paid In header will switch parsing back on on the next page.
    stop_phrases = (
        "interest (variable)",
        "statement abbreviations",
        "account name",
        "the royal bank of scotland plc.",
        "retstmt",
    )

    def flush_pending():
        nonlocal pending_date, pending_description
        pending_date = None
        pending_description = []

    def classify_money_tokens(line, pos):
        """
        Classify only numbers physically located in the three money columns.

        Using token.start() is intentional. Header labels are left aligned while
        monetary values are right aligned, so midpoint boundaries are unreliable.
        """
        values = {
            "paid_in": None,
            "withdrawn": None,
            "balance": None,
        }
        first_column_money_start = None

        for match in PDF_MONEY_RE.finditer(line):
            start_pos = match.start()

            # Anything before Paid In is description content. This excludes
            # values such as "CAD 3.30 VRATE 1.8750".
            if start_pos < pos["paid_in"]:
                continue

            try:
                amount, _ = parse_statement_money(match.group(0))
            except (TypeError, ValueError):
                continue

            amount = abs(float(amount))

            if start_pos >= pos["balance"]:
                column = "balance"
            elif start_pos >= pos["withdrawn"]:
                column = "withdrawn"
            else:
                column = "paid_in"

            values[column] = amount

            if (
                first_column_money_start is None
                or start_pos < first_column_money_start
            ):
                first_column_money_start = start_pos

        return (
            values["paid_in"],
            values["withdrawn"],
            values["balance"],
            first_column_money_start,
        )

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        header_positions = _statement_table_header_positions(line)
        if header_positions:
            positions = header_positions
            in_table = True
            flush_pending()
            continue

        if not in_table or positions is None:
            continue

        folded_line = " ".join(line.casefold().split())

        # Stop before footer/page-header/non-transaction sections. The next
        # proper table header will re-enable parsing.
        if any(phrase in folded_line for phrase in stop_phrases):
            flush_pending()
            in_table = False
            continue

        # Parse the date from the FULL line, not from the header's Date column
        # start. On RBS page 1 the heading is indented one character but actual
        # dates start at column 0; slicing from the header position turned
        # "11 AUG" into "1 AUG".
        parsed_date, date_end = _parse_statement_date_prefix(
            line, default_year
        )

        if parsed_date is not None:
            last_date = parsed_date
            if pending_description:
                # A new printed date starts a new statement group.
                flush_pending()
            description_start = date_end
        else:
            description_start = positions["description"]

        paid_in, withdrawn, running_balance, first_money_start = (
            classify_money_tokens(line, positions)
        )

        # A description extends to the first genuine statement-money column,
        # not the first money-looking value anywhere on the line.
        description_end = (
            first_money_start
            if first_money_start is not None
            else len(line)
        )

        description_piece = line[
            description_start : max(description_start, description_end)
        ].strip()

        if description_piece:
            if not pending_description:
                pending_date = parsed_date or last_date
            pending_description.append(description_piece)

        has_statement_money = (
            paid_in is not None
            or withdrawn is not None
            or running_balance is not None
        )
        if not has_statement_money:
            continue

        txn_date = parsed_date or pending_date or last_date
        description = " ".join(pending_description).strip()
        folded_description = description.casefold()

        # Page-to-page balance markers are not transactions.
        if "brought forward" in folded_description:
            if running_balance is not None:
                previous_running = running_balance
                if opening_balance is None:
                    opening_balance = running_balance
            flush_pending()
            continue

        if any(
            phrase in folded_description
            for phrase in (
                "carried forward",
                "closing balance",
                "opening balance",
                "previous balance",
                "new balance",
            )
        ):
            if running_balance is not None:
                previous_running = running_balance
            flush_pending()
            continue

        if txn_date is None:
            warnings.append(
                f'Could not determine a date for statement row '
                f'"{description or line.strip()}".'
            )
            flush_pending()
            continue

        amount = None
        source = ""

        if paid_in is not None and withdrawn is None:
            amount = abs(paid_in)
            source = "Paid In"
        elif withdrawn is not None and paid_in is None:
            amount = -abs(withdrawn)
            source = "Withdrawn"
        elif paid_in is not None and withdrawn is not None:
            # Extremely unusual, but retain deterministic behaviour.
            amount = abs(paid_in) - abs(withdrawn)
            source = "Paid In/Withdrawn"

        balance_corrected = False

        # Running balance is an arithmetic audit trail. It is a fallback, not
        # the normal parser: correctly extracted RBS rows should not need it.
        if running_balance is not None and previous_running is not None:
            delta = round(
                float(running_balance) - float(previous_running), 2
            )

            if amount is None:
                amount = delta
                source = "Running balance"
                balance_corrected = True
            else:
                expected = round(
                    float(previous_running) + float(amount), 2
                )
                discrepancy = round(
                    expected - float(running_balance), 2
                )
                if abs(discrepancy) > 0.01:
                    amount = delta
                    source = "Running balance"
                    balance_corrected = True

        if amount is None:
            warnings.append(
                f'No amount could be read for '
                f'"{description or "statement transaction"}" '
                f'on {txn_date.isoformat()}.'
            )
            flush_pending()
            continue

        pdf_check_difference = None
        if running_balance is not None and previous_running is not None:
            pdf_check_difference = round(
                float(previous_running)
                + float(amount)
                - float(running_balance),
                2,
            )

        rows.append(
            {
                "txn_date": txn_date.isoformat(),
                "description": description or "Statement transaction",
                "amount": round(float(amount), 2),
                "statement_balance": running_balance,
                "raw_amount": round(abs(float(amount)), 2),
                "explicit_sign": True,
                "pdf_check_difference": pdf_check_difference,
                "pdf_amount_source": source,
                "pdf_amount_corrected": balance_corrected,
            }
        )

        if running_balance is not None:
            previous_running = running_balance
        elif previous_running is not None:
            previous_running = round(
                float(previous_running) + float(amount), 2
            )

        flush_pending()

    if not rows:
        return None

    if closing_balance is None:
        balances = [
            row["statement_balance"]
            for row in rows
            if row.get("statement_balance") is not None
        ]
        if balances:
            closing_balance = balances[-1]

    if opening_balance is None and rows:
        first = rows[0]
        if first.get("statement_balance") is not None:
            opening_balance = round(
                float(first["statement_balance"]) - float(first["amount"]), 2
            )
            warnings.append(
                "Opening balance was inferred from the first transaction; "
                "please verify it."
            )

    corrected_count = sum(
        1 for row in rows if row.get("pdf_amount_corrected")
    )
    if corrected_count:
        warnings.append(
            f"{corrected_count} transaction amount(s) needed running-balance "
            "correction. Review those rows."
        )

    bad_checks = [
        row
        for row in rows
        if row.get("pdf_check_difference") is not None
        and abs(float(row["pdf_check_difference"])) > 0.01
    ]
    if bad_checks:
        warnings.append(
            f"{len(bad_checks)} transaction row(s) fail the running-balance "
            "check and should be reviewed."
        )

    return {
        "opening_balance": opening_balance,
        "closing_balance": closing_balance,
        "transactions": rows,
        "warnings": warnings,
        "parser_name": "RBS/NatWest fixed-column parser",
    }


def parse_pdf_statement_text(text):
    """
    Heuristically parse common UK text-based bank statements.

    The reconciliation screen is intentionally editable because banks differ
    in layout. Running-balance changes are preferred over wording when present.
    """
    cleaned_text = text.replace("\u00a0", " ")
    default_year = _statement_default_year(cleaned_text)
    opening_balance = _find_labeled_statement_balance(cleaned_text, opening=True)
    closing_balance = _find_labeled_statement_balance(cleaned_text, opening=False)
    period_start, period_end = _find_statement_period(cleaned_text)
    statement_paid_in = _find_statement_summary_total(cleaned_text, "paid in")
    statement_withdrawn = _find_statement_summary_total(cleaned_text, "withdrawn")

    fixed_column = _parse_fixed_column_statement_table(
        cleaned_text,
        opening_balance=opening_balance,
        closing_balance=closing_balance,
    )
    if fixed_column is not None:
        fixed_column["period_start"] = (
            period_start.isoformat() if period_start else None
        )
        fixed_column["period_end"] = (
            period_end.isoformat() if period_end else None
        )
        fixed_column["statement_paid_in"] = statement_paid_in
        fixed_column["statement_withdrawn"] = statement_withdrawn
        return fixed_column

    blocks = []
    current = None
    for raw_line in cleaned_text.splitlines():
        line = raw_line.rstrip()
        parsed_date, end = _parse_statement_date_prefix(line, default_year)
        if parsed_date is not None:
            if current is not None:
                blocks.append(current)
            current = {
                "date": parsed_date,
                "parts": [line[end:].strip()],
                "source": [line],
            }
        elif current is not None and line.strip():
            folded_line = " ".join(line.casefold().split())
            boundary_phrases = (
                "opening balance", "closing balance", "balance brought forward",
                "balance carried forward", "brought forward", "carried forward",
                "previous balance", "statement balance",
            )
            if any(phrase in folded_line for phrase in boundary_phrases):
                # A balance/summary line belongs to the statement, not to the
                # preceding transaction description.
                blocks.append(current)
                current = None
            else:
                # Continuation descriptions are common in PDF statements.
                current["parts"].append(line.strip())
                current["source"].append(line)
    if current is not None:
        blocks.append(current)

    rows = []
    balance_words = (
        "opening balance", "closing balance", "balance brought forward",
        "balance carried forward", "brought forward", "carried forward",
        "previous balance",
    )

    for block in blocks:
        body = " ".join(block["parts"])
        matches = list(PDF_MONEY_RE.finditer(body))
        if not matches:
            continue

        description = PDF_MONEY_RE.sub(" ", body)
        description = " ".join(description.split())
        folded = description.casefold()
        if any(word in folded for word in balance_words):
            continue

        parsed_tokens = []
        for match in matches:
            try:
                parsed_tokens.append(parse_statement_money(match.group(0)))
            except ValueError:
                pass
        if not parsed_tokens:
            continue

        raw_amount, explicit_sign = parsed_tokens[0]
        statement_balance = None
        if len(parsed_tokens) >= 2:
            statement_balance = parsed_tokens[-1][0]

        rows.append(
            {
                "txn_date": block["date"].isoformat(),
                "description": description or "Statement transaction",
                "amount": _infer_statement_amount(
                    description, raw_amount, explicit_sign
                ),
                "statement_balance": statement_balance,
                "raw_amount": raw_amount,
                "explicit_sign": explicit_sign,
            }
        )

    # Where a running balance is present, its change is substantially more
    # reliable than guessing debit/credit from PDF text columns.
    previous_balance = opening_balance
    for row in rows:
        running = row.get("statement_balance")
        if running is None:
            continue
        if previous_balance is not None:
            delta = round(float(running) - float(previous_balance), 2)
            if abs(delta) >= 0.005:
                row["amount"] = delta
        previous_balance = running

    # If a closing label was not found but transaction rows clearly contain a
    # running balance, the final running balance is a useful fallback.
    if closing_balance is None:
        running_values = [
            row["statement_balance"]
            for row in rows
            if row.get("statement_balance") is not None
        ]
        if running_values:
            closing_balance = running_values[-1]

    # If opening balance is missing but the first row has a running balance,
    # infer it from the first parsed transaction. The UI makes this field
    # editable and labels parser warnings so the user remains in control.
    opening_inferred = False
    if opening_balance is None and rows and rows[0].get("statement_balance") is not None:
        opening_balance = round(
            rows[0]["statement_balance"] - rows[0]["amount"], 2
        )
        opening_inferred = True

    warnings = []
    if not rows:
        warnings.append(
            "No transaction rows were detected automatically. You can add rows manually, "
            "but this PDF layout may need a bank-specific parser."
        )
    if opening_balance is None:
        warnings.append("Opening balance was not found - enter it from the statement.")
    elif opening_inferred:
        warnings.append(
            "Opening balance was inferred from the first transaction - please verify it."
        )
    if closing_balance is None:
        warnings.append("Closing balance was not found - enter it from the statement.")

    return {
        "opening_balance": opening_balance,
        "closing_balance": closing_balance,
        "transactions": rows,
        "warnings": warnings,
        "period_start": period_start.isoformat() if period_start else None,
        "period_end": period_end.isoformat() if period_end else None,
        "statement_paid_in": statement_paid_in,
        "statement_withdrawn": statement_withdrawn,
    }


class FinanceDB:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = paths.data_dir() / "finance.db"
        else:
            self.db_path = Path(db_path)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_schema()
        self.migrate_schema()
        self.seed_defaults()

    def create_schema(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                account_type TEXT NOT NULL,
                opening_balance REAL NOT NULL DEFAULT 0.0,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category_type TEXT NOT NULL
            );


            CREATE TABLE IF NOT EXISTS app_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                txn_date TEXT NOT NULL,
                account_id INTEGER NOT NULL,
                category_id INTEGER,
                payee TEXT,
                memo TEXT,
                amount REAL NOT NULL,
                scheduled_id INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(account_id) REFERENCES accounts(id),
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );

            CREATE TABLE IF NOT EXISTS scheduled_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_id INTEGER NOT NULL,
                category_id INTEGER,
                payee TEXT,
                memo TEXT,
                amount REAL NOT NULL,
                frequency TEXT NOT NULL,
                next_date TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY(account_id) REFERENCES accounts(id),
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );


            CREATE TABLE IF NOT EXISTS budget_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_id INTEGER NOT NULL,
                category_id INTEGER,
                payee TEXT,
                memo TEXT,
                amount REAL NOT NULL,
                frequency TEXT NOT NULL,
                next_date TEXT NOT NULL,
                end_date TEXT,
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY(account_id) REFERENCES accounts(id),
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );


            CREATE TABLE IF NOT EXISTS budget_scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                account_id INTEGER NOT NULL,
                starting_balance REAL NOT NULL,
                rows_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );


            CREATE TABLE IF NOT EXISTS reconciliations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                statement_start TEXT NOT NULL,
                statement_end TEXT NOT NULL,
                opening_balance REAL NOT NULL,
                closing_balance REAL NOT NULL,
                source_file TEXT,
                source_hash TEXT,
                transaction_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );
            """
        )
        self.conn.commit()

    def migrate_schema(self):
        """Add v0.2 columns to an existing v0.1 database without losing data."""
        columns = {
            row["name"]
            for row in self.conn.execute("PRAGMA table_info(transactions)").fetchall()
        }

        migrations = []
        if "transfer_group" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN transfer_group TEXT"
            )
        if "reconciled" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN reconciled INTEGER NOT NULL DEFAULT 0"
            )
        if "external_id" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN external_id TEXT"
            )
        if "import_source" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN import_source TEXT"
            )
        if "reconciliation_id" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN reconciliation_id INTEGER"
            )
        if "reconciled_at" not in columns:
            migrations.append(
                "ALTER TABLE transactions ADD COLUMN reconciled_at TEXT"
            )

        for sql in migrations:
            self.conn.execute(sql)

        budget_columns = {
            row["name"]
            for row in self.conn.execute("PRAGMA table_info(budget_items)").fetchall()
        }
        if "category_id" not in budget_columns:
            self.conn.execute("ALTER TABLE budget_items ADD COLUMN category_id INTEGER")
        if "payee" not in budget_columns:
            self.conn.execute("ALTER TABLE budget_items ADD COLUMN payee TEXT")
        if "memo" not in budget_columns:
            self.conn.execute("ALTER TABLE budget_items ADD COLUMN memo TEXT")

        # external_id is unique within an account. NULL values remain allowed,
        # so manually entered transactions are unaffected.
        self.conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_transactions_account_external_id
            ON transactions(account_id, external_id)
            WHERE external_id IS NOT NULL
            """
        )
        self.conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_reconciliations_account_source_hash
            ON reconciliations(account_id, source_hash)
            WHERE source_hash IS NOT NULL
            """
        )

        # Older scheduled transactions were entered before the amount sign was
        # derived from the category type, so some still carry whatever sign the
        # user originally typed. Bring every row in line with the current
        # convention (Expense -> negative, Income -> positive); safe to repeat.
        self.conn.execute(
            """
            UPDATE scheduled_transactions
            SET amount = -ABS(amount)
            WHERE amount > 0
              AND category_id IN (
                  SELECT id FROM categories WHERE category_type = 'Expense'
              )
            """
        )
        self.conn.execute(
            """
            UPDATE scheduled_transactions
            SET amount = ABS(amount)
            WHERE amount < 0
              AND category_id IN (
                  SELECT id FROM categories WHERE category_type = 'Income'
              )
            """
        )

        # Same stale-sign issue, same fix, for budgetary (forecast-only) transactions.
        self.conn.execute(
            """
            UPDATE budget_items
            SET amount = -ABS(amount)
            WHERE amount > 0
              AND category_id IN (
                  SELECT id FROM categories WHERE category_type = 'Expense'
              )
            """
        )
        self.conn.execute(
            """
            UPDATE budget_items
            SET amount = ABS(amount)
            WHERE amount < 0
              AND category_id IN (
                  SELECT id FROM categories WHERE category_type = 'Income'
              )
            """
        )

        self.conn.commit()

    def get_setting(self, key, default=None):
        row = self.conn.execute(
            "SELECT setting_value FROM app_settings WHERE setting_key = ?",
            (key,),
        ).fetchone()
        return row["setting_value"] if row else default

    def set_setting(self, key, value):
        self.conn.execute(
            """
            INSERT INTO app_settings(setting_key, setting_value)
            VALUES (?, ?)
            ON CONFLICT(setting_key)
            DO UPDATE SET setting_value = excluded.setting_value
            """,
            (key, str(value)),
        )
        self.conn.commit()

    def seed_defaults(self):
        defaults = [
            ("Salary", "Income"),
            ("Interest", "Income"),
            ("Groceries", "Expense"),
            ("Utilities", "Expense"),
            ("Mortgage / Rent", "Expense"),
            ("Transport", "Expense"),
            ("Insurance", "Expense"),
            ("Entertainment", "Expense"),
            ("Eating Out", "Expense"),
            ("Other", "Expense"),
        ]
        for name, ctype in defaults:
            self.conn.execute(
                "INSERT OR IGNORE INTO categories(name, category_type) VALUES (?, ?)",
                (name, ctype),
            )
        self.conn.commit()

    # ---------- Accounts ----------

    def add_account(self, name, account_type, opening_balance):
        self.conn.execute(
            "INSERT INTO accounts(name, account_type, opening_balance) VALUES (?, ?, ?)",
            (name, account_type, opening_balance),
        )
        self.conn.commit()

    def update_account(self, account_id, name, account_type, opening_balance):
        self.conn.execute(
            """
            UPDATE accounts
            SET name = ?, account_type = ?, opening_balance = ?
            WHERE id = ?
            """,
            (name, account_type, opening_balance, account_id),
        )
        self.conn.commit()

    def delete_account(self, account_id):
        txns = self.conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE account_id = ?", (account_id,)
        ).fetchone()[0]
        schedules = self.conn.execute(
            "SELECT COUNT(*) FROM scheduled_transactions WHERE account_id = ?",
            (account_id,),
        ).fetchone()[0]
        budget_items = self.conn.execute(
            "SELECT COUNT(*) FROM budget_items WHERE account_id = ?",
            (account_id,),
        ).fetchone()[0]
        scenarios = self.conn.execute(
            "SELECT COUNT(*) FROM budget_scenarios WHERE account_id = ?",
            (account_id,),
        ).fetchone()[0]
        reconciliations = self.conn.execute(
            "SELECT COUNT(*) FROM reconciliations WHERE account_id = ?",
            (account_id,),
        ).fetchone()[0]
        if txns or schedules or budget_items or scenarios or reconciliations:
            raise ValueError(
                "This account is already in use. Delete or move its transactions, "
                "schedules, budgetary transactions, saved scenarios and reconciliation "
                "history first."
            )

        self.conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.conn.commit()

    def get_accounts(self):
        return self.conn.execute(
            """
            SELECT
                a.id,
                a.name,
                a.account_type,
                a.opening_balance,
                a.opening_balance + COALESCE(SUM(t.amount), 0) AS balance
            FROM accounts a
            LEFT JOIN transactions t ON t.account_id = a.id
            WHERE a.active = 1
            GROUP BY a.id
            ORDER BY a.name
            """
        ).fetchall()

    def get_account(self, account_id):
        return self.conn.execute(
            """
            SELECT
                a.id,
                a.name,
                a.account_type,
                a.opening_balance,
                a.opening_balance + COALESCE(SUM(t.amount), 0) AS balance
            FROM accounts a
            LEFT JOIN transactions t ON t.account_id = a.id
            WHERE a.id = ?
            GROUP BY a.id
            """,
            (account_id,),
        ).fetchone()

    def get_account_choices(self):
        return self.conn.execute(
            "SELECT id, name FROM accounts WHERE active = 1 ORDER BY name"
        ).fetchall()

    # ---------- Categories ----------

    def add_category(self, name, category_type):
        self.conn.execute(
            "INSERT INTO categories(name, category_type) VALUES (?, ?)",
            (name, category_type),
        )
        self.conn.commit()

    def get_category(self, category_id):
        return self.conn.execute(
            """
            SELECT id, name, category_type
            FROM categories
            WHERE id = ?
            """,
            (category_id,),
        ).fetchone()

    def update_category(self, category_id, name, category_type):
        """
        Rename a category and/or change its Income/Expense type.

        Actual historic transactions keep their original signed amounts.
        Future Scheduled and Budgetary items are normalised to the new type.
        """
        if category_type not in ("Expense", "Income"):
            raise ValueError("Category type must be Expense or Income.")

        with self.conn:
            self.conn.execute(
                """
                UPDATE categories
                SET name = ?, category_type = ?
                WHERE id = ?
                """,
                (name, category_type, category_id),
            )

            if category_type == "Expense":
                self.conn.execute(
                    """
                    UPDATE scheduled_transactions
                    SET amount = -ABS(amount)
                    WHERE category_id = ?
                    """,
                    (category_id,),
                )
                self.conn.execute(
                    """
                    UPDATE budget_items
                    SET amount = -ABS(amount)
                    WHERE category_id = ?
                    """,
                    (category_id,),
                )
            else:
                self.conn.execute(
                    """
                    UPDATE scheduled_transactions
                    SET amount = ABS(amount)
                    WHERE category_id = ?
                    """,
                    (category_id,),
                )
                self.conn.execute(
                    """
                    UPDATE budget_items
                    SET amount = ABS(amount)
                    WHERE category_id = ?
                    """,
                    (category_id,),
                )

    def delete_category(self, category_id):
        used = self.conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM transactions WHERE category_id = ?) +
                (SELECT COUNT(*) FROM scheduled_transactions WHERE category_id = ?) +
                (SELECT COUNT(*) FROM budget_items WHERE category_id = ?)
            """,
            (category_id, category_id, category_id),
        ).fetchone()[0]

        if used:
            raise ValueError(
                "This category is already in use. Change or remove the related "
                "transactions, scheduled transactions or budgetary transactions first."
            )

        self.conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()

    def get_categories(self):
        return self.conn.execute(
            "SELECT id, name, category_type FROM categories ORDER BY category_type, name"
        ).fetchall()

    def get_category_choices(self):
        return self.conn.execute(
            "SELECT id, name, category_type FROM categories ORDER BY name"
        ).fetchall()

    # ---------- Transactions ----------

    def add_transaction(
        self,
        txn_date,
        account_id,
        category_id,
        payee,
        memo,
        amount,
        scheduled_id=None,
        transfer_group=None,
    ):
        cur = self.conn.execute(
            """
            INSERT INTO transactions
            (txn_date, account_id, category_id, payee, memo, amount, scheduled_id, transfer_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                txn_date,
                account_id,
                category_id,
                payee,
                memo,
                amount,
                scheduled_id,
                transfer_group,
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def add_transactions_bulk(self, transactions):
        """Insert a fully validated batch of ordinary transactions atomically."""
        with self.conn:
            self.conn.executemany(
                """
                INSERT INTO transactions
                (txn_date, account_id, category_id, payee, memo, amount)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        t["txn_date"],
                        t["account_id"],
                        t.get("category_id"),
                        t.get("payee", ""),
                        t.get("memo", ""),
                        t["amount"],
                    )
                    for t in transactions
                ],
            )

    def get_existing_external_ids(self, account_id, external_ids):
        """Return external IDs already stored for this account."""
        values = [value for value in external_ids if value]
        if not values:
            return set()

        found = set()
        # Stay below SQLite's usual variable limit.
        for start in range(0, len(values), 800):
            batch = values[start : start + 800]
            placeholders = ",".join("?" for _ in batch)
            rows = self.conn.execute(
                f"""
                SELECT external_id
                FROM transactions
                WHERE account_id = ?
                  AND external_id IN ({placeholders})
                """,
                [account_id, *batch],
            ).fetchall()
            found.update(row["external_id"] for row in rows)

        return found

    def find_manual_transaction_matches(
        self, account_id, transactions, date_window_days=4
    ):
        """
        Find likely pre-existing non-OFX Account Transactions.

        Manual entries do not necessarily use the bank's posted date or exact
        statement wording, so matching is deliberately fuzzy:

        - same account
        - same amount to the penny
        - manual date within +/- date_window_days of the OFX posted date
        - payee/memo similarity is supporting evidence, not mandatory

        Matching is one-to-one: once a manual transaction is paired with an
        OFX transaction it cannot be reused for another incoming row.
        """
        if not account_id or not transactions:
            return {}

        parsed_incoming = []
        for txn in transactions:
            try:
                txn_date = parse_date(txn.get("txn_date"))
            except (TypeError, ValueError):
                continue

            parsed_incoming.append((txn, txn_date))

        if not parsed_incoming:
            return {}

        earliest = min(d for _, d in parsed_incoming) - timedelta(
            days=date_window_days
        )
        latest = max(d for _, d in parsed_incoming) + timedelta(
            days=date_window_days
        )

        candidates = self.conn.execute(
            """
            SELECT
                id,
                txn_date,
                amount,
                COALESCE(payee, '') AS payee,
                COALESCE(memo, '') AS memo
            FROM transactions
            WHERE account_id = ?
              AND external_id IS NULL
              AND transfer_group IS NULL
              AND txn_date BETWEEN ? AND ?
            ORDER BY txn_date, id
            """,
            (account_id, earliest.isoformat(), latest.isoformat()),
        ).fetchall()

        if not candidates:
            return {}

        def normalise_text(value):
            value = unicodedata.normalize("NFKD", value or "")
            value = value.casefold()
            value = re.sub(r"[^a-z0-9]+", " ", value)
            return " ".join(value.split())

        def useful_tokens(value):
            ignore = {
                "card", "payment", "purchase", "debit", "credit", "visa",
                "mastercard", "contactless", "online", "pos", "bank",
                "transaction", "ref", "reference", "mobile", "transfer",
                "payment", "pymt", "bill",
            }
            return {
                token
                for token in normalise_text(value).split()
                if len(token) >= 3 and token not in ignore
            }

        def compare_text(left_value, right_value):
            left = normalise_text(left_value)
            right = normalise_text(right_value)

            if not left or not right:
                return 0.0

            if min(len(left), len(right)) >= 3 and (
                left in right or right in left
            ):
                return 1.0

            ratio = SequenceMatcher(None, left, right).ratio()

            lt = useful_tokens(left)
            rt = useful_tokens(right)
            token_score = 0.0
            if lt and rt:
                overlap = lt & rt
                if overlap:
                    token_score = len(overlap) / max(
                        1, min(len(lt), len(rt))
                    )

            return max(ratio, token_score)

        def transaction_text_score(incoming, existing):
            incoming_payee = incoming.get("payee", "")
            incoming_memo = incoming.get("memo", "")
            existing_payee = existing["payee"]
            existing_memo = existing["memo"]

            incoming_combined = " ".join(
                part for part in (incoming_payee, incoming_memo) if part
            )
            existing_combined = " ".join(
                part for part in (existing_payee, existing_memo) if part
            )

            return max(
                compare_text(incoming_payee, existing_payee),
                compare_text(incoming_memo, existing_memo),
                compare_text(incoming_combined, existing_combined),
                compare_text(incoming_payee, existing_combined),
                compare_text(incoming_combined, existing_payee),
            )

        # Build every plausible exact-amount/date-window pairing first.
        pairings = []
        incoming_candidate_counts = {}
        manual_candidate_counts = {}

        for incoming_index, (txn, txn_date) in enumerate(parsed_incoming):
            external_id = txn.get("external_id")
            if not external_id:
                continue

            amount = round(float(txn.get("amount") or 0.0), 2)

            for row in candidates:
                if round(float(row["amount"]), 2) != amount:
                    continue

                try:
                    manual_date = parse_date(row["txn_date"])
                except ValueError:
                    continue

                date_diff = abs((manual_date - txn_date).days)
                if date_diff > date_window_days:
                    continue

                text_score = transaction_text_score(txn, row)

                # Ranking strongly prefers the closest date, with text used to
                # break ties/disambiguate repeated amounts.
                date_score = max(
                    0.0,
                    1.0 - (date_diff / (date_window_days + 1)),
                )
                overall_score = (date_score * 0.70) + (text_score * 0.30)

                pairings.append(
                    {
                        "incoming_index": incoming_index,
                        "external_id": external_id,
                        "txn": txn,
                        "txn_date": txn_date,
                        "manual": row,
                        "manual_date": manual_date,
                        "date_diff": date_diff,
                        "text_score": text_score,
                        "overall_score": overall_score,
                    }
                )

                incoming_candidate_counts[incoming_index] = (
                    incoming_candidate_counts.get(incoming_index, 0) + 1
                )
                manual_candidate_counts[row["id"]] = (
                    manual_candidate_counts.get(row["id"], 0) + 1
                )

        if not pairings:
            return {}

        # Best pairs first. This makes matching one-to-one and stops one
        # manually-entered £10 payment from matching several £10 OFX rows.
        pairings.sort(
            key=lambda pair: (
                pair["overall_score"],
                pair["text_score"],
                -pair["date_diff"],
            ),
            reverse=True,
        )

        used_incoming = set()
        used_manual = set()
        matches = {}

        for pair in pairings:
            incoming_index = pair["incoming_index"]
            manual_id = pair["manual"]["id"]

            if incoming_index in used_incoming or manual_id in used_manual:
                continue

            candidate_count = incoming_candidate_counts.get(
                incoming_index, 1
            )
            date_diff = pair["date_diff"]
            text_score = pair["text_score"]

            # Confidence rules:
            #
            # * Unique exact-amount matches within 2 days are strong enough to
            #   call likely even if bank/manual descriptions differ a lot.
            # * At 3 days, a unique amount is still likely; ambiguous repeated
            #   amounts need at least a little descriptive support.
            # * At 4 days, description similarity is needed for "likely".
            # * Anything else inside the window remains visible as "possible".
            if date_diff <= 2 and candidate_count == 1:
                confidence = "likely"
            elif date_diff <= 2 and text_score >= 0.20:
                confidence = "likely"
            elif date_diff == 3 and (
                candidate_count == 1 or text_score >= 0.25
            ):
                confidence = "likely"
            elif date_diff == 4 and text_score >= 0.45:
                confidence = "likely"
            else:
                confidence = "possible"

            manual = pair["manual"]
            matches[pair["external_id"]] = {
                "confidence": confidence,
                "transaction_id": manual["id"],
                "payee": manual["payee"],
                "memo": manual["memo"],
                "txn_date": manual["txn_date"],
                "amount": float(manual["amount"]),
                "date_diff_days": date_diff,
                "text_score": text_score,
                "overall_score": pair["overall_score"],
            }

            used_incoming.add(incoming_index)
            used_manual.add(manual_id)

        return matches

    def import_and_replace_bank_transactions(
        self,
        account_id,
        new_transactions,
        manual_replacements,
        import_source,
    ):
        """
        Atomically import new OFX rows and replace selected manual matches
        in place.

        Updating the existing manual row preserves category_id, scheduled_id,
        reconciled/reconciliation_id, created_at and the transaction ID.
        """
        new_transactions = list(new_transactions or [])
        manual_replacements = list(manual_replacements or [])

        external_ids = [
            txn.get("external_id")
            for txn in new_transactions
            if txn.get("external_id")
        ]
        external_ids.extend(
            replacement["ofx_transaction"].get("external_id")
            for replacement in manual_replacements
            if replacement.get("ofx_transaction", {}).get("external_id")
        )

        existing_external_ids = self.get_existing_external_ids(
            account_id, external_ids
        )
        if existing_external_ids:
            raise ValueError(
                "One or more selected OFX transactions have already been "
                "imported. Refresh the preview and try again."
            )

        seen_manual_ids = set()
        validated_replacements = []

        for replacement in manual_replacements:
            manual_id = int(replacement["manual_transaction_id"])
            txn = replacement["ofx_transaction"]

            if manual_id in seen_manual_ids:
                raise ValueError(
                    "The same manual transaction was selected for more than "
                    "one OFX replacement."
                )
            seen_manual_ids.add(manual_id)

            row = self.conn.execute(
                """
                SELECT id, account_id, amount, external_id, transfer_group
                FROM transactions
                WHERE id = ?
                """,
                (manual_id,),
            ).fetchone()

            if not row:
                raise ValueError(
                    f"Manual transaction ID {manual_id} no longer exists."
                )
            if row["account_id"] != account_id:
                raise ValueError(
                    "A matched manual transaction belongs to a different account."
                )
            if row["external_id"]:
                raise ValueError(
                    "A matched manual transaction has already been linked to "
                    "an imported bank transaction."
                )
            if row["transfer_group"]:
                raise ValueError(
                    "Linked transfer entries cannot be replaced by an OFX row."
                )
            if round(float(row["amount"]), 2) != round(
                float(txn["amount"]), 2
            ):
                raise ValueError(
                    "The matched manual transaction amount no longer agrees "
                    "with the OFX transaction. Refresh the preview and review it."
                )

            validated_replacements.append((manual_id, txn))

        imported_count = 0
        replaced_count = 0

        with self.conn:
            for manual_id, txn in validated_replacements:
                cur = self.conn.execute(
                    """
                    UPDATE transactions
                    SET
                        txn_date = ?,
                        payee = ?,
                        memo = ?,
                        amount = ?,
                        external_id = ?,
                        import_source = ?
                    WHERE id = ?
                      AND account_id = ?
                      AND external_id IS NULL
                      AND transfer_group IS NULL
                    """,
                    (
                        txn["txn_date"],
                        txn.get("payee", ""),
                        txn.get("memo", ""),
                        txn["amount"],
                        txn["external_id"],
                        import_source,
                        manual_id,
                        account_id,
                    ),
                )
                if cur.rowcount != 1:
                    raise ValueError(
                        "A manual transaction changed while the OFX preview "
                        "was open. No replacement was completed."
                    )
                replaced_count += 1

            for txn in new_transactions:
                cur = self.conn.execute(
                    """
                    INSERT INTO transactions
                    (
                        txn_date, account_id, category_id, payee, memo, amount,
                        external_id, import_source
                    )
                    VALUES (?, ?, NULL, ?, ?, ?, ?, ?)
                    """,
                    (
                        txn["txn_date"],
                        account_id,
                        txn.get("payee", ""),
                        txn.get("memo", ""),
                        txn["amount"],
                        txn["external_id"],
                        import_source,
                    ),
                )
                if cur.rowcount == 1:
                    imported_count += 1

        return imported_count, replaced_count

    def add_bank_transactions_bulk(self, account_id, transactions, import_source):
        """
        Import OFX transactions atomically.

        INSERT OR IGNORE provides a final safety net against duplicate FITIDs,
        even if the same statement is imported twice.
        """
        before = self.conn.total_changes

        with self.conn:
            self.conn.executemany(
                """
                INSERT OR IGNORE INTO transactions
                (
                    txn_date, account_id, category_id, payee, memo, amount,
                    external_id, import_source
                )
                VALUES (?, ?, NULL, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        t["txn_date"],
                        account_id,
                        t.get("payee", ""),
                        t.get("memo", ""),
                        t["amount"],
                        t["external_id"],
                        import_source,
                    )
                    for t in transactions
                ],
            )

        return self.conn.total_changes - before

    def update_transaction(
        self, txn_id, txn_date, account_id, category_id, payee, memo, amount
    ):
        row = self.conn.execute(
            "SELECT transfer_group FROM transactions WHERE id = ?", (txn_id,)
        ).fetchone()

        if not row:
            raise ValueError("Transaction no longer exists.")

        if row["transfer_group"]:
            raise ValueError(
                "Transfers should be deleted and recreated rather than edited in version 0.2."
            )

        self.conn.execute(
            """
            UPDATE transactions
            SET txn_date = ?, account_id = ?, category_id = ?,
                payee = ?, memo = ?, amount = ?
            WHERE id = ?
            """,
            (txn_date, account_id, category_id, payee, memo, amount, txn_id),
        )
        self.conn.commit()

    def add_transfer(self, txn_date, from_account_id, to_account_id, amount, memo):
        if from_account_id == to_account_id:
            raise ValueError("The source and destination accounts must be different.")
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        group = uuid.uuid4().hex
        from_name = self.conn.execute(
            "SELECT name FROM accounts WHERE id = ?", (from_account_id,)
        ).fetchone()["name"]
        to_name = self.conn.execute(
            "SELECT name FROM accounts WHERE id = ?", (to_account_id,)
        ).fetchone()["name"]

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO transactions
                (txn_date, account_id, category_id, payee, memo, amount, transfer_group)
                VALUES (?, ?, NULL, ?, ?, ?, ?)
                """,
                (
                    txn_date,
                    from_account_id,
                    f"Transfer to {to_name}",
                    memo,
                    -amount,
                    group,
                ),
            )
            self.conn.execute(
                """
                INSERT INTO transactions
                (txn_date, account_id, category_id, payee, memo, amount, transfer_group)
                VALUES (?, ?, NULL, ?, ?, ?, ?)
                """,
                (
                    txn_date,
                    to_account_id,
                    f"Transfer from {from_name}",
                    memo,
                    amount,
                    group,
                ),
            )

    def delete_transaction(self, txn_id):
        self.delete_transactions([txn_id])

    def delete_transactions(self, txn_ids):
        """
        Delete one or more selected transactions atomically.

        If a selected row is one side of a transfer, both linked transfer
        entries are deleted.
        """
        txn_ids = [int(txn_id) for txn_id in txn_ids]
        if not txn_ids:
            return 0

        placeholders = ",".join("?" for _ in txn_ids)
        rows = self.conn.execute(
            f"""
            SELECT id, transfer_group
            FROM transactions
            WHERE id IN ({placeholders})
            """,
            txn_ids,
        ).fetchall()

        if not rows:
            return 0

        ordinary_ids = []
        transfer_groups = set()

        for row in rows:
            if row["transfer_group"]:
                transfer_groups.add(row["transfer_group"])
            else:
                ordinary_ids.append(row["id"])

        before = self.conn.total_changes

        with self.conn:
            if ordinary_ids:
                placeholders = ",".join("?" for _ in ordinary_ids)
                self.conn.execute(
                    f"DELETE FROM transactions WHERE id IN ({placeholders})",
                    ordinary_ids,
                )

            if transfer_groups:
                groups = list(transfer_groups)
                placeholders = ",".join("?" for _ in groups)
                self.conn.execute(
                    f"""
                    DELETE FROM transactions
                    WHERE transfer_group IN ({placeholders})
                    """,
                    groups,
                )

        return self.conn.total_changes - before

    def get_transaction(self, txn_id):
        return self.conn.execute(
            """
            SELECT t.*, a.name AS account_name, COALESCE(c.name, '') AS category_name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.id = ?
            """,
            (txn_id,),
        ).fetchone()

    def get_transactions(self):
        return self.conn.execute(
            """
            SELECT
                t.id,
                t.txn_date,
                a.name AS account_name,
                COALESCE(c.name, '') AS category_name,
                COALESCE(t.payee, '') AS payee,
                COALESCE(t.memo, '') AS memo,
                t.amount,
                t.transfer_group
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            LEFT JOIN categories c ON c.id = t.category_id
            ORDER BY t.txn_date DESC, t.id DESC
            """
        ).fetchall()

    def get_register_transactions(self, account_id):
        account = self.get_account(account_id)
        if not account:
            return []

        rows = self.conn.execute(
            """
            SELECT
                t.id,
                t.txn_date,
                COALESCE(t.payee, '') AS payee,
                COALESCE(c.name, '') AS category_name,
                COALESCE(t.memo, '') AS memo,
                t.amount,
                t.transfer_group,
                t.reconciled
            FROM transactions t
            LEFT JOIN categories c ON c.id = t.category_id
            WHERE t.account_id = ?
            ORDER BY t.txn_date ASC, t.id ASC
            """,
            (account_id,),
        ).fetchall()

        running = account["opening_balance"]
        result = []
        for row in rows:
            running += row["amount"]
            result.append(
                {
                    "id": row["id"],
                    "txn_date": row["txn_date"],
                    "payee": row["payee"],
                    "category_name": row["category_name"],
                    "memo": row["memo"],
                    "amount": row["amount"],
                    "balance": running,
                    "transfer_group": row["transfer_group"],
                    "reconciled": row["reconciled"],
                }
            )
        return result

    # ---------- Reconciliation ----------

    def get_reconciliation_candidates(
        self, account_id, statement_date, amount, date_window_days=14
    ):
        target_date = parse_date(statement_date)
        start_date = target_date - timedelta(days=date_window_days)
        end_date = target_date + timedelta(days=date_window_days)
        rows = self.conn.execute(
            """
            SELECT
                t.id,
                t.txn_date,
                COALESCE(t.payee, '') AS payee,
                COALESCE(t.memo, '') AS memo,
                t.amount,
                t.reconciled,
                t.reconciliation_id
            FROM transactions t
            WHERE t.account_id = ?
              AND t.txn_date BETWEEN ? AND ?
              AND ABS(t.amount - ?) < 0.005
            ORDER BY ABS(julianday(t.txn_date) - julianday(?)), t.txn_date, t.id
            """,
            (
                account_id,
                start_date.isoformat(),
                end_date.isoformat(),
                float(amount),
                target_date.isoformat(),
            ),
        ).fetchall()
        return [dict(row) for row in rows]

    def auto_match_statement_transactions(
        self, account_id, statement_transactions, date_window_days=4
    ):
        if not statement_transactions:
            return {}

        def normalise_text(value):
            value = unicodedata.normalize("NFKD", value or "")
            value = value.casefold()
            value = re.sub(r"[^a-z0-9]+", " ", value)
            return " ".join(value.split())

        def text_score(left_value, right_value):
            left = normalise_text(left_value)
            right = normalise_text(right_value)
            if not left or not right:
                return 0.0
            if min(len(left), len(right)) >= 3 and (
                left in right or right in left
            ):
                return 1.0
            ratio = SequenceMatcher(None, left, right).ratio()
            lt = {x for x in left.split() if len(x) >= 3}
            rt = {x for x in right.split() if len(x) >= 3}
            token = 0.0
            if lt and rt and lt & rt:
                token = len(lt & rt) / max(1, min(len(lt), len(rt)))
            return max(ratio, token)

        all_candidates = {}
        pairings = []

        for index, statement in enumerate(statement_transactions):
            candidates = self.get_reconciliation_candidates(
                account_id,
                statement["txn_date"],
                statement["amount"],
                date_window_days=date_window_days,
            )
            all_candidates[index] = candidates
            stmt_date = parse_date(statement["txn_date"])
            stmt_text = statement.get("description", "")

            for candidate in candidates:
                candidate_date = parse_date(candidate["txn_date"])
                date_diff = abs((candidate_date - stmt_date).days)
                candidate_text = " ".join(
                    x for x in (candidate["payee"], candidate["memo"]) if x
                )
                similarity = text_score(stmt_text, candidate_text)
                date_score = max(
                    0.0, 1.0 - date_diff / (date_window_days + 1)
                )
                # Prefer an unreconciled row when otherwise equivalent.
                unreconciled_bonus = 0.03 if not candidate["reconciled"] else 0.0
                score = date_score * 0.72 + similarity * 0.28 + unreconciled_bonus
                pairings.append(
                    {
                        "statement_index": index,
                        "candidate": candidate,
                        "date_diff": date_diff,
                        "text_score": similarity,
                        "score": score,
                    }
                )

        pairings.sort(
            key=lambda item: (
                item["score"],
                item["text_score"],
                -item["date_diff"],
            ),
            reverse=True,
        )

        used_statement = set()
        used_transactions = set()
        result = {}

        for pair in pairings:
            index = pair["statement_index"]
            candidate = pair["candidate"]
            if index in used_statement or candidate["id"] in used_transactions:
                continue

            candidate_count = len(all_candidates.get(index, []))
            date_diff = pair["date_diff"]
            similarity = pair["text_score"]

            if candidate["reconciled"]:
                confidence = "already_reconciled"
            elif date_diff <= 1 and candidate_count == 1:
                confidence = "likely"
            elif date_diff <= 2 and (candidate_count == 1 or similarity >= 0.18):
                confidence = "likely"
            elif date_diff <= 4 and similarity >= 0.48:
                confidence = "likely"
            else:
                confidence = "possible"

            result[index] = {
                **candidate,
                "confidence": confidence,
                "date_diff_days": date_diff,
                "text_score": similarity,
            }
            used_statement.add(index)
            used_transactions.add(candidate["id"])

        return result

    def get_unmatched_account_transactions(
        self, account_id, start_date, end_date, matched_transaction_ids
    ):
        matched = set(matched_transaction_ids or [])
        rows = self.conn.execute(
            """
            SELECT
                t.id,
                t.txn_date,
                COALESCE(t.payee, '') AS payee,
                COALESCE(t.memo, '') AS memo,
                t.amount,
                t.reconciled
            FROM transactions t
            WHERE t.account_id = ?
              AND t.txn_date BETWEEN ? AND ?
              AND t.reconciled = 0
            ORDER BY t.txn_date, t.id
            """,
            (account_id, start_date, end_date),
        ).fetchall()
        return [dict(row) for row in rows if row["id"] not in matched]

    def get_account_balance_through_date(self, account_id, through_date):
        account = self.get_account(account_id)
        if not account:
            return None
        total = self.conn.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE account_id = ? AND txn_date <= ?
            """,
            (account_id, through_date),
        ).fetchone()[0]
        return float(account["opening_balance"]) + float(total or 0.0)

    def get_reconciliation_by_hash(self, account_id, source_hash):
        if not source_hash:
            return None
        return self.conn.execute(
            """
            SELECT * FROM reconciliations
            WHERE account_id = ? AND source_hash = ?
            """,
            (account_id, source_hash),
        ).fetchone()

    def get_last_reconciliation(self, account_id):
        return self.conn.execute(
            """
            SELECT * FROM reconciliations
            WHERE account_id = ?
            ORDER BY statement_end DESC, id DESC
            LIMIT 1
            """,
            (account_id,),
        ).fetchone()

    def complete_reconciliation(
        self,
        account_id,
        statement_start,
        statement_end,
        opening_balance,
        closing_balance,
        transaction_ids,
        source_file,
        source_hash,
    ):
        transaction_ids = sorted(set(int(x) for x in transaction_ids))
        with self.conn:
            if source_hash:
                existing = self.conn.execute(
                    """
                    SELECT id FROM reconciliations
                    WHERE account_id = ? AND source_hash = ?
                    """,
                    (account_id, source_hash),
                ).fetchone()
                if existing:
                    raise ValueError(
                        "This PDF statement has already been reconciled for this account."
                    )

            cur = self.conn.execute(
                """
                INSERT INTO reconciliations
                (
                    account_id, statement_start, statement_end,
                    opening_balance, closing_balance,
                    source_file, source_hash, transaction_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    account_id,
                    statement_start,
                    statement_end,
                    float(opening_balance),
                    float(closing_balance),
                    source_file,
                    source_hash,
                    len(transaction_ids),
                ),
            )
            reconciliation_id = cur.lastrowid

            if transaction_ids:
                placeholders = ",".join("?" for _ in transaction_ids)
                self.conn.execute(
                    f"""
                    UPDATE transactions
                    SET reconciled = 1,
                        reconciliation_id = ?,
                        reconciled_at = CURRENT_TIMESTAMP
                    WHERE id IN ({placeholders})
                    """,
                    [reconciliation_id, *transaction_ids],
                )

        return reconciliation_id

    # ---------- Scheduled transactions ----------

    def normalise_scheduled_amount(self, category_id, amount):
        """
        Scheduled transaction amounts are interpreted using the category type.

        Expense category -> always negative
        Income category  -> always positive
        No category       -> preserve the sign entered by the user
        """
        amount = float(amount)

        if category_id is None:
            return amount

        row = self.conn.execute(
            "SELECT category_type FROM categories WHERE id = ?",
            (category_id,),
        ).fetchone()

        if not row:
            return amount

        category_type = (row["category_type"] or "").strip().casefold()

        if category_type == "expense":
            return -abs(amount)
        if category_type == "income":
            return abs(amount)

        return amount

    def add_schedule(
        self,
        name,
        account_id,
        category_id,
        payee,
        memo,
        amount,
        frequency,
        next_date,
    ):
        amount = self.normalise_scheduled_amount(category_id, amount)

        self.conn.execute(
            """
            INSERT INTO scheduled_transactions
            (name, account_id, category_id, payee, memo, amount, frequency, next_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                account_id,
                category_id,
                payee,
                memo,
                amount,
                frequency,
                next_date,
            ),
        )
        self.conn.commit()

    def add_schedules_bulk(self, schedules):
        """Insert a fully validated batch of scheduled transactions atomically."""
        with self.conn:
            self.conn.executemany(
                """
                INSERT INTO scheduled_transactions
                (name, account_id, category_id, payee, memo, amount, frequency, next_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        s["name"],
                        s["account_id"],
                        s["category_id"],
                        s["payee"],
                        s.get("memo", ""),
                        s["amount"],
                        s["frequency"],
                        s["next_date"],
                    )
                    for s in schedules
                ],
            )

    def get_schedule(self, schedule_id):
        return self.conn.execute(
            """
            SELECT
                s.*,
                a.name AS account_name,
                COALESCE(c.name, '') AS category_name,
                COALESCE(c.category_type, '') AS category_type
            FROM scheduled_transactions s
            JOIN accounts a ON a.id = s.account_id
            LEFT JOIN categories c ON c.id = s.category_id
            WHERE s.id = ?
            """,
            (schedule_id,),
        ).fetchone()

    def update_schedule(
        self,
        schedule_id,
        name,
        account_id,
        category_id,
        payee,
        memo,
        amount,
        frequency,
        next_date,
    ):
        amount = self.normalise_scheduled_amount(category_id, amount)

        self.conn.execute(
            """
            UPDATE scheduled_transactions
            SET name = ?, account_id = ?, category_id = ?, payee = ?,
                memo = ?, amount = ?, frequency = ?, next_date = ?
            WHERE id = ?
            """,
            (
                name,
                account_id,
                category_id,
                payee,
                memo,
                amount,
                frequency,
                next_date,
                schedule_id,
            ),
        )
        self.conn.commit()

    def delete_schedule(self, schedule_id):
        self.conn.execute(
            "DELETE FROM scheduled_transactions WHERE id = ?", (schedule_id,)
        )
        self.conn.commit()

    def get_schedules(self):
        return self.conn.execute(
            """
            SELECT
                s.id,
                s.name,
                a.name AS account_name,
                COALESCE(c.name, '') AS category_name,
                COALESCE(s.payee, '') AS payee,
                s.amount,
                s.frequency,
                s.next_date,
                s.active
            FROM scheduled_transactions s
            JOIN accounts a ON a.id = s.account_id
            LEFT JOIN categories c ON c.id = s.category_id
            ORDER BY s.next_date, s.name
            """
        ).fetchall()

    def process_due_schedules(self):
        today = date.today()
        schedules = self.conn.execute(
            """
            SELECT *
            FROM scheduled_transactions
            WHERE active = 1
            ORDER BY next_date
            """
        ).fetchall()

        created = 0

        for sched in schedules:
            due = parse_date(sched["next_date"])

            while due <= today:
                self.conn.execute(
                    """
                    INSERT INTO transactions
                    (txn_date, account_id, category_id, payee, memo, amount, scheduled_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        due.isoformat(),
                        sched["account_id"],
                        sched["category_id"],
                        sched["payee"],
                        sched["memo"],
                        self.normalise_scheduled_amount(
                            sched["category_id"], sched["amount"]
                        ),
                        sched["id"],
                    ),
                )
                created += 1
                due = advance_date(due, sched["frequency"])

            self.conn.execute(
                "UPDATE scheduled_transactions SET next_date = ? WHERE id = ?",
                (due.isoformat(), sched["id"]),
            )

        self.conn.commit()
        return created

    # ---------- Budget projection ----------

    def get_active_schedules_for_account(self, account_id):
        return self.conn.execute(
            """
            SELECT
                s.id,
                s.name,
                s.account_id,
                s.amount,
                s.frequency,
                s.next_date,
                COALESCE(s.payee, '') AS payee,
                COALESCE(c.name, '') AS category_name,
                COALESCE(c.category_type, '') AS category_type
            FROM scheduled_transactions s
            LEFT JOIN categories c ON c.id = s.category_id
            WHERE s.account_id = ?
              AND s.active = 1
            ORDER BY s.next_date, s.name
            """,
            (account_id,),
        ).fetchall()

    def normalise_budget_amount(self, category_id, amount):
        """
        Budgetary transactions use category type just like scheduled items.

        Expense category -> negative
        Income category  -> positive
        No category       -> preserve the supplied sign (for legacy v0.5 items)
        """
        amount = float(amount)

        if category_id is None:
            return amount

        row = self.conn.execute(
            "SELECT category_type FROM categories WHERE id = ?",
            (category_id,),
        ).fetchone()

        if not row:
            return amount

        category_type = (row["category_type"] or "").strip().casefold()

        if category_type == "expense":
            return -abs(amount)
        if category_type == "income":
            return abs(amount)

        return amount

    def add_budget_item(
        self,
        name,
        account_id,
        category_id,
        payee,
        memo,
        amount,
        frequency,
        next_date,
        end_date=None,
    ):
        amount = self.normalise_budget_amount(category_id, amount)
        self.conn.execute(
            """
            INSERT INTO budget_items
            (
                name, account_id, category_id, payee, memo,
                amount, frequency, next_date, end_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                account_id,
                category_id,
                payee,
                memo,
                amount,
                frequency,
                next_date,
                end_date,
            ),
        )
        self.conn.commit()

    def update_budget_item(
        self,
        item_id,
        name,
        account_id,
        category_id,
        payee,
        memo,
        amount,
        frequency,
        next_date,
        end_date=None,
    ):
        amount = self.normalise_budget_amount(category_id, amount)
        self.conn.execute(
            """
            UPDATE budget_items
            SET name = ?, account_id = ?, category_id = ?, payee = ?, memo = ?,
                amount = ?, frequency = ?, next_date = ?, end_date = ?
            WHERE id = ?
            """,
            (
                name,
                account_id,
                category_id,
                payee,
                memo,
                amount,
                frequency,
                next_date,
                end_date,
                item_id,
            ),
        )
        self.conn.commit()

    def delete_budget_item(self, item_id):
        self.conn.execute("DELETE FROM budget_items WHERE id = ?", (item_id,))
        self.conn.commit()

    def get_budget_item(self, item_id):
        return self.conn.execute(
            """
            SELECT
                b.*,
                COALESCE(c.name, '') AS category_name,
                COALESCE(c.category_type, '') AS category_type
            FROM budget_items b
            LEFT JOIN categories c ON c.id = b.category_id
            WHERE b.id = ?
            """,
            (item_id,),
        ).fetchone()

    def get_budget_items_for_account(self, account_id):
        return self.conn.execute(
            """
            SELECT
                b.id,
                b.name,
                b.account_id,
                b.category_id,
                COALESCE(c.name, '') AS category_name,
                COALESCE(c.category_type, '') AS category_type,
                COALESCE(b.payee, '') AS payee,
                COALESCE(b.memo, '') AS memo,
                b.amount,
                b.frequency,
                b.next_date,
                b.end_date,
                b.active
            FROM budget_items b
            LEFT JOIN categories c ON c.id = b.category_id
            WHERE b.account_id = ?
              AND b.active = 1
            ORDER BY b.next_date, b.name
            """,
            (account_id,),
        ).fetchall()

    def get_all_budget_items(self):
        return self.conn.execute(
            """
            SELECT
                b.id,
                b.name,
                b.account_id,
                a.name AS account_name,
                b.category_id,
                COALESCE(c.name, '') AS category_name,
                COALESCE(c.category_type, '') AS category_type,
                COALESCE(b.payee, '') AS payee,
                COALESCE(b.memo, '') AS memo,
                b.amount,
                b.frequency,
                b.next_date,
                b.end_date,
                b.active
            FROM budget_items b
            JOIN accounts a ON a.id = b.account_id
            LEFT JOIN categories c ON c.id = b.category_id
            WHERE b.active = 1
            ORDER BY b.next_date, b.name
            """
        ).fetchall()

    # ---------- Budget scenarios ----------

    def create_budget_scenario(
        self, name, account_id, starting_balance, rows
    ):
        payload = json.dumps(rows, ensure_ascii=False)
        cur = self.conn.execute(
            """
            INSERT INTO budget_scenarios
            (name, account_id, starting_balance, rows_json)
            VALUES (?, ?, ?, ?)
            """,
            (name, account_id, float(starting_balance), payload),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_budget_scenario(
        self, scenario_id, name, account_id, starting_balance, rows
    ):
        payload = json.dumps(rows, ensure_ascii=False)
        self.conn.execute(
            """
            UPDATE budget_scenarios
            SET name = ?, account_id = ?, starting_balance = ?,
                rows_json = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                name,
                account_id,
                float(starting_balance),
                payload,
                scenario_id,
            ),
        )
        self.conn.commit()

    def get_budget_scenarios(self):
        return self.conn.execute(
            """
            SELECT
                s.id,
                s.name,
                s.account_id,
                a.name AS account_name,
                s.starting_balance,
                s.created_at,
                s.updated_at
            FROM budget_scenarios s
            JOIN accounts a ON a.id = s.account_id
            ORDER BY s.name COLLATE NOCASE
            """
        ).fetchall()

    def get_budget_scenario(self, scenario_id):
        row = self.conn.execute(
            """
            SELECT
                s.id,
                s.name,
                s.account_id,
                a.name AS account_name,
                s.starting_balance,
                s.rows_json,
                s.created_at,
                s.updated_at
            FROM budget_scenarios s
            JOIN accounts a ON a.id = s.account_id
            WHERE s.id = ?
            """,
            (scenario_id,),
        ).fetchone()

        if not row:
            return None

        result = dict(row)
        try:
            result["rows"] = json.loads(result["rows_json"])
        except (TypeError, json.JSONDecodeError):
            result["rows"] = []
        return result

    def delete_budget_scenario(self, scenario_id):
        self.conn.execute(
            "DELETE FROM budget_scenarios WHERE id = ?",
            (scenario_id,),
        )
        self.conn.commit()

    # ---------- Backup / restore ----------

    def backup_to(self, destination):
        """
        Create a transactionally consistent SQLite backup while the application
        database is open.
        """
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        target = sqlite3.connect(destination)
        try:
            self.conn.backup(target)
            target.commit()
        finally:
            target.close()

        return destination

    @staticmethod
    def validate_backup(path):
        """
        Validate that a file is a readable Simple Finance SQLite database.
        Returns (True, message) or (False, reason).
        """
        path = Path(path)

        if not path.exists() or not path.is_file():
            return False, "Backup file does not exist."

        try:
            conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        except sqlite3.Error as exc:
            return False, f"Could not open backup: {exc}"

        try:
            integrity = conn.execute("PRAGMA integrity_check").fetchone()
            if not integrity or integrity[0] != "ok":
                return False, "SQLite integrity check failed."

            tables = {
                row[0]
                for row in conn.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    """
                ).fetchall()
            }

            required = {
                "accounts",
                "categories",
                "transactions",
                "scheduled_transactions",
            }
            missing = required - tables
            if missing:
                return (
                    False,
                    "This does not appear to be a Simple Finance backup. "
                    "Missing table(s): " + ", ".join(sorted(missing)),
                )

            return True, "Backup is valid."
        except sqlite3.Error as exc:
            return False, f"Backup validation failed: {exc}"
        finally:
            conn.close()

    def close(self):
        self.conn.close()


def _finish_modal_dialog(dialog, parent, focus_widget=None):
    """
    Finish laying out a Toplevel before it becomes modal.

    Opening a modal window directly from a Treeview double-click can otherwise
    leave some Linux/Tk window managers showing only a tiny blank shell.
    """
    dialog.update_idletasks()

    try:
        width = max(dialog.winfo_reqwidth(), 1)
        height = max(dialog.winfo_reqheight(), 1)

        parent.update_idletasks()
        x = parent.winfo_rootx() + max(
            0, (parent.winfo_width() - width) // 2
        )
        y = parent.winfo_rooty() + max(
            0, (parent.winfo_height() - height) // 2
        )
        dialog.geometry(f"+{x}+{y}")
    except tk.TclError:
        pass

    dialog.transient(parent)

    try:
        dialog.wait_visibility()
        dialog.grab_set()
    except tk.TclError:
        return

    dialog.lift()

    if focus_widget is not None:
        try:
            focus_widget.focus_set()
        except tk.TclError:
            pass


class AccountEditDialog(tk.Toplevel):
    """Edit an existing account's name, type and opening balance."""

    def __init__(self, parent, app, account_id):
        super().__init__(parent)
        self.app = app
        self.account_id = account_id
        self.result = False

        account = app.db.get_account(account_id)
        if not account:
            messagebox.showerror(
                "Account not found",
                "The selected account no longer exists.",
                parent=parent,
            )
            self.after(1, self.destroy)
            return

        self.title("Edit account")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Account name").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame, width=34)
        self.name_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 12))
        self.name_entry.insert(0, account["name"])

        ttk.Label(frame, text="Account type").grid(row=0, column=1, sticky="w")
        self.type_combo = ttk.Combobox(
            frame,
            state="readonly",
            values=["Current", "Savings", "Cash", "Credit Card", "Other"],
            width=20,
        )
        self.type_combo.grid(row=1, column=1, pady=(0, 12))
        self.type_combo.set(account["account_type"])

        ttk.Label(frame, text="Opening / starting balance").grid(
            row=2, column=0, sticky="w"
        )
        self.opening_entry = ttk.Entry(frame, width=20)
        self.opening_entry.grid(row=3, column=0, sticky="w", pady=(0, 8))
        self.opening_entry.insert(0, f'{account["opening_balance"]:.2f}')

        current_balance = account["balance"]
        ttk.Label(
            frame,
            text=(
                f"Current balance: {money(current_balance)}\n"
                "Changing the starting balance will recalculate this account's "
                "running and current balances."
            ),
            justify="left",
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(4, 14))

        buttons = ttk.Frame(frame)
        buttons.grid(row=5, column=0, columnspan=2, sticky="e")

        ttk.Button(
            buttons, text="Cancel", command=self.destroy
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            buttons, text="Save changes", command=self.save
        ).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Return>", lambda event: self.save())

        self.name_entry.selection_range(0, tk.END)
        _finish_modal_dialog(self, parent, self.name_entry)

    def save(self):
        name = self.name_entry.get().strip()
        account_type = self.type_combo.get().strip()

        if not name:
            messagebox.showerror(
                "Missing account name",
                "Please enter an account name.",
                parent=self,
            )
            return

        if not account_type:
            messagebox.showerror(
                "Missing account type",
                "Please select an account type.",
                parent=self,
            )
            return

        try:
            opening_balance = float(
                self.opening_entry.get().strip().replace("£", "").replace(",", "")
            )
        except ValueError:
            messagebox.showerror(
                "Invalid starting balance",
                "Starting balance must be a number.",
                parent=self,
            )
            return

        try:
            self.app.db.update_account(
                self.account_id,
                name,
                account_type,
                opening_balance,
            )
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate account",
                "Another account already uses that name.",
                parent=self,
            )
            return

        self.result = True
        self.destroy()


class CategoryEditDialog(tk.Toplevel):
    """Edit an existing category name and Income/Expense type."""

    def __init__(self, parent, app, category_id):
        row = app.db.get_category(category_id)
        if not row:
            raise ValueError("The selected category no longer exists.")

        super().__init__(parent)
        self.app = app
        self.category_id = category_id
        self.result = False

        self.original_type = row["category_type"]

        self.title("Edit category")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Category name").grid(
            row=0, column=0, sticky="w"
        )
        self.name_entry = ttk.Entry(frame, width=36)
        self.name_entry.grid(
            row=1, column=0, padx=(0, 12), pady=(0, 12)
        )
        self.name_entry.insert(0, row["name"])

        ttk.Label(frame, text="Type").grid(
            row=0, column=1, sticky="w"
        )
        self.type_combo = ttk.Combobox(
            frame,
            state="readonly",
            values=["Expense", "Income"],
            width=18,
        )
        self.type_combo.grid(row=1, column=1, pady=(0, 12))
        self.type_combo.set(row["category_type"])

        ttk.Label(
            frame,
            text=(
                "Renaming a category is safe: existing transactions remain linked to it.\n"
                "If you change Expense ↔ Income, future Scheduled and Budgetary "
                "transactions using this category will change direction too. "
                "Historic real transaction amounts are not changed."
            ),
            justify="left",
            wraplength=590,
        ).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=2, sticky="e")

        ttk.Button(
            buttons, text="Cancel", command=self.destroy
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            buttons, text="Save changes", command=self.save
        ).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Return>", lambda event: self.save())

        self.name_entry.focus_set()
        self.name_entry.selection_range(0, tk.END)

    def save(self):
        name = self.name_entry.get().strip()
        category_type = self.type_combo.get().strip()

        if not name:
            messagebox.showerror(
                "Missing category name",
                "Please enter a category name.",
                parent=self,
            )
            return

        if category_type not in ("Expense", "Income"):
            messagebox.showerror(
                "Invalid category type",
                "Choose Expense or Income.",
                parent=self,
            )
            return

        if category_type != self.original_type:
            if not messagebox.askyesno(
                "Change category type",
                f'Change this category from {self.original_type} to '
                f'{category_type}?\n\n'
                "Future Scheduled and Budgetary transactions using it will "
                "change direction to match the new type.",
                parent=self,
            ):
                return

        try:
            self.app.db.update_category(
                self.category_id,
                name,
                category_type,
            )
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate category",
                "Another category already uses that name.",
                parent=self,
            )
            return
        except ValueError as exc:
            messagebox.showerror(
                "Cannot save category",
                str(exc),
                parent=self,
            )
            return

        self.result = True
        self.destroy()


class ScheduledTransactionDialog(tk.Toplevel):
    """Edit an existing scheduled transaction."""

    def __init__(self, parent, app, schedule_id):
        row = app.db.get_schedule(schedule_id)
        if not row:
            raise ValueError(
                "The selected scheduled transaction no longer exists."
            )

        super().__init__(parent)
        self.app = app
        self.schedule_id = schedule_id
        self.result = False

        self.title("Edit scheduled transaction")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame, width=28)
        self.name_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))
        self.name_entry.insert(0, row["name"])

        ttk.Label(frame, text="Account").grid(row=0, column=1, sticky="w")
        self.account_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.account_combo.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

        ttk.Label(frame, text="Category").grid(row=0, column=2, sticky="w")
        self.category_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.category_combo.grid(row=1, column=2, pady=(0, 10))

        ttk.Label(frame, text="Payee").grid(row=2, column=0, sticky="w")
        self.payee_entry = ttk.Entry(frame, width=28)
        self.payee_entry.grid(row=3, column=0, padx=(0, 10), pady=(0, 10))
        self.payee_entry.insert(0, row["payee"] or "")

        ttk.Label(frame, text="Amount").grid(row=2, column=1, sticky="w")
        self.amount_entry = ttk.Entry(frame, width=18)
        self.amount_entry.grid(row=3, column=1, padx=(0, 10), pady=(0, 10))

        # For categorised schedules, make editing friendlier by showing a
        # positive figure; the category determines Income vs Expense.
        if row["category_type"] in ("Income", "Expense"):
            shown_amount = abs(row["amount"])
        else:
            shown_amount = row["amount"]
        self.amount_entry.insert(0, f"{shown_amount:.2f}")

        ttk.Label(frame, text="Frequency").grid(row=2, column=2, sticky="w")
        self.frequency_combo = ttk.Combobox(
            frame,
            state="readonly",
            values=["Daily", "Weekly", "Monthly", "Yearly"],
            width=18,
        )
        self.frequency_combo.grid(row=3, column=2, pady=(0, 10))
        self.frequency_combo.set(row["frequency"])

        ttk.Label(frame, text="Next date").grid(row=4, column=0, sticky="w")
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=5, column=0, padx=(0, 10), pady=(0, 10), sticky="w")

        self.date_entry = ttk.Entry(date_frame, width=12)
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, app.format_date(row["next_date"]))

        ttk.Button(
            date_frame,
            text="Select date…",
            command=self.select_date,
        ).pack(side="left", padx=(5, 0))

        ttk.Label(frame, text="Memo").grid(row=4, column=1, sticky="w")
        self.memo_entry = ttk.Entry(frame, width=50)
        self.memo_entry.grid(
            row=5, column=1, columnspan=2, sticky="ew", pady=(0, 10)
        )
        self.memo_entry.insert(0, row["memo"] or "")

        ttk.Label(
            frame,
            text=(
                "For Income/Expense categories you can enter the amount as a positive "
                "figure; the category controls whether it is money in or money out."
            ),
            justify="left",
        ).grid(row=6, column=0, columnspan=3, sticky="w", pady=(2, 12))

        buttons = ttk.Frame(frame)
        buttons.grid(row=7, column=0, columnspan=3, sticky="e")

        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(
            buttons, text="Save changes", command=self.save
        ).pack(side="right")

        account_names = list(app.account_name_to_id.keys())
        category_names = [""] + list(app.category_name_to_id.keys())

        self.account_combo["values"] = account_names
        self.category_combo["values"] = category_names
        self.account_combo.set(row["account_name"])
        self.category_combo.set(row["category_name"])

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())
        self.name_entry.selection_range(0, tk.END)
        _finish_modal_dialog(self, parent, self.name_entry)

    def select_date(self):
        try:
            initial = self.app.parse_user_date(self.date_entry.get())
        except ValueError:
            initial = date.today()

        picker = DatePickerDialog(self, initial)
        self.wait_window(picker)

        try:
            self.grab_set()
        except tk.TclError:
            pass

        if picker.result is not None:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.app.format_date(picker.result))

    def save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror(
                "Missing name",
                "Enter a name for the scheduled transaction.",
                parent=self,
            )
            return

        account_name = self.account_combo.get()
        account_id = self.app.account_name_to_id.get(account_name)
        if not account_id:
            messagebox.showerror(
                "No account", "Choose an account.", parent=self
            )
            return

        category_name = self.category_combo.get().strip()
        category_id = self.app.category_name_to_id.get(category_name)

        try:
            amount = float(
                self.amount_entry.get().strip().replace("£", "").replace(",", "")
            )
        except ValueError:
            messagebox.showerror(
                "Invalid amount", "Amount must be a number.", parent=self
            )
            return

        if amount == 0:
            messagebox.showerror(
                "Invalid amount", "Amount cannot be zero.", parent=self
            )
            return

        try:
            next_date = self.app.parse_user_date(
                self.date_entry.get()
            ).isoformat()
        except ValueError:
            messagebox.showerror(
                "Invalid date",
                f"Use date format {self.app.date_format_example()}.",
                parent=self,
            )
            return

        self.app.db.update_schedule(
            self.schedule_id,
            name,
            account_id,
            category_id,
            self.payee_entry.get().strip(),
            self.memo_entry.get().strip(),
            amount,
            self.frequency_combo.get(),
            next_date,
        )

        self.result = True
        self.destroy()


class BudgetItemDialog(tk.Toplevel):
    """Create or edit a forecast-only budgetary transaction."""

    def __init__(self, parent, app, item_id=None, preset_account=None):
        edit_row = None
        if item_id is not None:
            edit_row = app.db.get_budget_item(item_id)
            if not edit_row:
                raise ValueError(
                    "The selected budgetary transaction no longer exists."
                )

        super().__init__(parent)
        self.app = app
        self.item_id = item_id
        self.result = False

        self.title(
            "Edit budgetary transaction" if item_id else "Add budgetary transaction"
        )
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame, width=28)
        self.name_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))

        ttk.Label(frame, text="Account").grid(row=0, column=1, sticky="w")
        self.account_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.account_combo.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

        ttk.Label(frame, text="Category").grid(row=0, column=2, sticky="w")
        self.category_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.category_combo.grid(row=1, column=2, pady=(0, 10))

        ttk.Label(frame, text="Payee / Description").grid(row=2, column=0, sticky="w")
        self.payee_entry = ttk.Entry(frame, width=28)
        self.payee_entry.grid(row=3, column=0, padx=(0, 10), pady=(0, 10))

        ttk.Label(frame, text="Amount").grid(row=2, column=1, sticky="w")
        self.amount_entry = ttk.Entry(frame, width=18)
        self.amount_entry.grid(row=3, column=1, padx=(0, 10), pady=(0, 10))

        ttk.Label(frame, text="Frequency").grid(row=2, column=2, sticky="w")
        self.frequency_combo = ttk.Combobox(
            frame,
            state="readonly",
            values=["One-off", "Weekly", "Monthly", "Yearly"],
            width=18,
        )
        self.frequency_combo.grid(row=3, column=2, pady=(0, 10))
        self.frequency_combo.set("Monthly")

        ttk.Label(frame, text="First / next date").grid(row=4, column=0, sticky="w")
        next_frame = ttk.Frame(frame)
        next_frame.grid(row=5, column=0, padx=(0, 10), pady=(0, 10), sticky="w")
        self.next_date_entry = ttk.Entry(next_frame, width=12)
        self.next_date_entry.pack(side="left")
        ttk.Button(
            next_frame, text="Select date…", command=self.select_next_date
        ).pack(side="left", padx=(5, 0))

        ttk.Label(frame, text="End date (optional)").grid(row=4, column=1, sticky="w")
        end_frame = ttk.Frame(frame)
        end_frame.grid(row=5, column=1, padx=(0, 10), pady=(0, 10), sticky="w")
        self.end_date_entry = ttk.Entry(end_frame, width=12)
        self.end_date_entry.pack(side="left")
        ttk.Button(
            end_frame, text="Select date…", command=self.select_end_date
        ).pack(side="left", padx=(5, 0))
        ttk.Button(
            end_frame,
            text="Clear",
            command=lambda: self.end_date_entry.delete(0, tk.END),
        ).pack(side="left", padx=(5, 0))

        ttk.Label(frame, text="Memo").grid(row=6, column=0, sticky="w")
        self.memo_entry = ttk.Entry(frame, width=76)
        self.memo_entry.grid(
            row=7, column=0, columnspan=3, sticky="ew", pady=(0, 8)
        )

        ttk.Label(
            frame,
            text=(
                "Enter the amount as a positive figure. The selected Category decides "
                "whether it is Income or Expense. These entries affect only the forecast."
            ),
            justify="left",
        ).grid(row=8, column=0, columnspan=3, sticky="w", pady=(2, 12))

        buttons = ttk.Frame(frame)
        buttons.grid(row=9, column=0, columnspan=3, sticky="e")

        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(
            buttons,
            text="Save changes" if item_id else "Add budgetary transaction",
            command=self.save,
        ).pack(side="right")

        account_names = list(app.account_name_to_id.keys())
        category_names = [""] + list(app.category_name_to_id.keys())
        self.account_combo["values"] = account_names
        self.category_combo["values"] = category_names

        if item_id:
            row = edit_row

            self.name_entry.insert(0, row["name"])
            self.account_combo.set(app.account_id_to_name.get(row["account_id"], ""))
            self.category_combo.set(row["category_name"])
            self.payee_entry.insert(0, row["payee"] or "")
            self.amount_entry.insert(0, f'{abs(row["amount"]):.2f}')
            self.frequency_combo.set(row["frequency"])
            self.next_date_entry.insert(0, app.format_date(row["next_date"]))
            if row["end_date"]:
                self.end_date_entry.insert(0, app.format_date(row["end_date"]))
            self.memo_entry.insert(0, row["memo"] or "")
        else:
            if preset_account and preset_account in account_names:
                self.account_combo.set(preset_account)
            elif account_names:
                self.account_combo.set(account_names[0])

            self.next_date_entry.insert(0, app.format_date(date.today()))

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())
        _finish_modal_dialog(self, parent, self.name_entry)

    def _select_date_into(self, entry):
        try:
            initial = self.app.parse_user_date(entry.get())
        except ValueError:
            initial = date.today()

        picker = DatePickerDialog(self, initial)
        self.wait_window(picker)

        try:
            self.grab_set()
        except tk.TclError:
            pass

        if picker.result is not None:
            entry.delete(0, tk.END)
            entry.insert(0, self.app.format_date(picker.result))

    def select_next_date(self):
        self._select_date_into(self.next_date_entry)

    def select_end_date(self):
        self._select_date_into(self.end_date_entry)

    def save(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror(
                "Missing name",
                "Enter a name for this budgetary transaction.",
                parent=self,
            )
            return

        account_name = self.account_combo.get()
        account_id = self.app.account_name_to_id.get(account_name)
        if not account_id:
            messagebox.showerror("No account", "Choose an account.", parent=self)
            return

        category_name = self.category_combo.get().strip()
        category_id = self.app.category_name_to_id.get(category_name)
        if not category_id:
            messagebox.showerror(
                "No category",
                "Choose an Income or Expense category so the forecast knows "
                "whether this is money in or money out.",
                parent=self,
            )
            return

        try:
            amount = float(
                self.amount_entry.get().strip().replace("£", "").replace(",", "")
            )
        except ValueError:
            messagebox.showerror(
                "Invalid amount", "Amount must be a number.", parent=self
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Invalid amount",
                "Enter the amount as a positive number greater than zero.",
                parent=self,
            )
            return

        try:
            next_date = self.app.parse_user_date(self.next_date_entry.get()).isoformat()
        except ValueError:
            messagebox.showerror(
                "Invalid date",
                f"Use {self.app.date_format_example()} style for the first / next date.",
                parent=self,
            )
            return

        end_text = self.end_date_entry.get().strip()
        end_date = None
        if end_text:
            try:
                end_date = self.app.parse_user_date(end_text).isoformat()
            except ValueError:
                messagebox.showerror(
                    "Invalid end date",
                    f"Use {self.app.date_format_example()} style for the end date.",
                    parent=self,
                )
                return

            if end_date < next_date:
                messagebox.showerror(
                    "Invalid end date",
                    "End date cannot be before the first / next date.",
                    parent=self,
                )
                return

        args = (
            name,
            account_id,
            category_id,
            self.payee_entry.get().strip(),
            self.memo_entry.get().strip(),
            amount,
            self.frequency_combo.get(),
            next_date,
            end_date,
        )

        if self.item_id:
            self.app.db.update_budget_item(self.item_id, *args)
        else:
            self.app.db.add_budget_item(*args)

        self.result = True
        self.destroy()


class DatePickerDialog(tk.Toplevel):
    """Small standard-library calendar picker."""

    def __init__(self, parent, initial_date=None):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.selected_date = initial_date or date.today()
        self.display_year = self.selected_date.year
        self.display_month = self.selected_date.month

        self.title("Select date")
        self.resizable(False, False)
        self.transient(parent)

        outer = ttk.Frame(self, padding=10)
        outer.pack(fill="both", expand=True)

        nav = ttk.Frame(outer)
        nav.pack(fill="x", pady=(0, 8))

        ttk.Button(nav, text="◀", width=4, command=self.previous_month).pack(
            side="left"
        )

        self.month_label = ttk.Label(
            nav, text="", anchor="center", style="Heading.TLabel"
        )
        self.month_label.pack(side="left", fill="x", expand=True, padx=8)

        ttk.Button(nav, text="▶", width=4, command=self.next_month).pack(
            side="right"
        )

        self.calendar_frame = ttk.Frame(outer)
        self.calendar_frame.pack()

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(10, 0))

        ttk.Button(bottom, text="Today", command=self.choose_today).pack(side="left")
        ttk.Button(bottom, text="Cancel", command=self.cancel).pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", lambda event: self.cancel())

        self.draw_calendar()

        self.update_idletasks()
        try:
            parent_x = parent.winfo_rootx()
            parent_y = parent.winfo_rooty()
            parent_w = parent.winfo_width()
            parent_h = parent.winfo_height()
            own_w = self.winfo_reqwidth()
            own_h = self.winfo_reqheight()
            x = parent_x + max(0, (parent_w - own_w) // 2)
            y = parent_y + max(0, (parent_h - own_h) // 2)
            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

        self.grab_set()
        self.focus_set()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[self.display_month]
        self.month_label.config(text=f"{month_name} {self.display_year}")

        for col, weekday in enumerate(
            ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        ):
            ttk.Label(
                self.calendar_frame,
                text=weekday,
                width=4,
                anchor="center",
            ).grid(row=0, column=col, padx=1, pady=(0, 3))

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.display_year, self.display_month)

        for row_index, week in enumerate(weeks, start=1):
            for col_index, day_number in enumerate(week):
                if day_number == 0:
                    ttk.Label(
                        self.calendar_frame, text="", width=4
                    ).grid(row=row_index, column=col_index, padx=1, pady=1)
                    continue

                chosen = date(
                    self.display_year, self.display_month, day_number
                )

                ttk.Button(
                    self.calendar_frame,
                    text=str(day_number),
                    width=4,
                    command=lambda d=chosen: self.choose(d),
                ).grid(row=row_index, column=col_index, padx=1, pady=1)

    def previous_month(self):
        first = date(self.display_year, self.display_month, 1)
        previous = add_months(first, -1)
        self.display_year = previous.year
        self.display_month = previous.month
        self.draw_calendar()

    def next_month(self):
        first = date(self.display_year, self.display_month, 1)
        following = add_months(first, 1)
        self.display_year = following.year
        self.display_month = following.month
        self.draw_calendar()

    def choose_today(self):
        self.choose(date.today())

    def choose(self, chosen_date):
        self.result = chosen_date
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()

    def cancel(self):
        self.result = None
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()


class TransactionDialog(tk.Toplevel):
    def __init__(self, parent, app, txn_id=None, preset_account=None):
        # Resolve edit data BEFORE creating the Toplevel. If the row no longer
        # exists, do not leave an orphaned blank Tk window behind.
        edit_row = None
        if txn_id is not None:
            edit_row = app.db.get_transaction(txn_id)
            if edit_row is None:
                raise ValueError(
                    f"Transaction ID {txn_id} no longer exists."
                )

        super().__init__(parent)
        self.app = app
        self.txn_id = txn_id
        self.result = False

        try:
            self.title("Edit transaction" if txn_id else "Add transaction")
            self.resizable(False, False)

            frame = ttk.Frame(self, padding=14)
            frame.pack(fill="both", expand=True)

            ttk.Label(frame, text="Date").grid(
                row=0, column=0, sticky="w"
            )
            date_frame = ttk.Frame(frame)
            date_frame.grid(
                row=1,
                column=0,
                padx=(0, 8),
                pady=(0, 10),
                sticky="w",
            )

            self.date_entry = ttk.Entry(date_frame, width=12)
            self.date_entry.pack(side="left")

            ttk.Button(
                date_frame,
                text="Select date…",
                command=self.select_date,
            ).pack(side="left", padx=(5, 0))

            ttk.Label(frame, text="Account").grid(
                row=0, column=1, sticky="w"
            )
            self.account_combo = ttk.Combobox(
                frame, state="readonly", width=24
            )
            self.account_combo.grid(
                row=1,
                column=1,
                padx=(0, 8),
                pady=(0, 10),
            )

            ttk.Label(frame, text="Category").grid(
                row=0, column=2, sticky="w"
            )
            self.category_combo = ttk.Combobox(
                frame, state="readonly", width=24
            )
            self.category_combo.grid(
                row=1, column=2, pady=(0, 10)
            )

            ttk.Label(
                frame, text="Payee / Description"
            ).grid(row=2, column=0, sticky="w")
            self.payee_entry = ttk.Entry(frame, width=28)
            self.payee_entry.grid(
                row=3,
                column=0,
                padx=(0, 8),
                pady=(0, 10),
            )

            ttk.Label(frame, text="Amount").grid(
                row=2, column=1, sticky="w"
            )
            self.amount_entry = ttk.Entry(frame, width=18)
            self.amount_entry.grid(
                row=3,
                column=1,
                padx=(0, 8),
                pady=(0, 10),
            )

            ttk.Label(frame, text="Memo").grid(
                row=4, column=0, sticky="w"
            )
            self.memo_entry = ttk.Entry(frame, width=70)
            self.memo_entry.grid(
                row=5,
                column=0,
                columnspan=3,
                sticky="ew",
                pady=(0, 12),
            )

            note = ttk.Label(
                frame,
                text=(
                    "Negative = payment / money out. "
                    "Positive = deposit / money in."
                ),
            )
            note.grid(
                row=6,
                column=0,
                columnspan=3,
                sticky="w",
                pady=(0, 10),
            )

            buttons = ttk.Frame(frame)
            buttons.grid(
                row=7,
                column=0,
                columnspan=3,
                sticky="e",
            )

            ttk.Button(
                buttons,
                text="Cancel",
                command=self.destroy,
            ).pack(side="right", padx=(8, 0))

            ttk.Button(
                buttons,
                text="Save changes" if txn_id else "Add transaction",
                command=self.save,
            ).pack(side="right")

            account_names = list(app.account_name_to_id.keys())
            category_names = [""] + list(
                app.category_name_to_id.keys()
            )
            self.account_combo["values"] = account_names
            self.category_combo["values"] = category_names

            if txn_id is not None:
                if edit_row["transfer_group"]:
                    messagebox.showinfo(
                        "Transfer",
                        "Transfer entries cannot be edited individually yet.\n"
                        "Delete the transfer and create it again instead.",
                        parent=parent,
                    )
                    self.result = False
                    self.destroy()
                    return

                self.date_entry.insert(
                    0, app.format_date(edit_row["txn_date"])
                )
                self.account_combo.set(edit_row["account_name"])
                self.category_combo.set(
                    edit_row["category_name"] or ""
                )
                self.payee_entry.insert(
                    0, edit_row["payee"] or ""
                )
                self.amount_entry.insert(
                    0, f'{edit_row["amount"]:.2f}'
                )
                self.memo_entry.insert(
                    0, edit_row["memo"] or ""
                )
            else:
                self.date_entry.insert(
                    0, app.format_date(date.today())
                )
                if (
                    preset_account
                    and preset_account in account_names
                ):
                    self.account_combo.set(preset_account)
                elif account_names:
                    self.account_combo.set(account_names[0])
                self.category_combo.set("")

            # Complete layout before making the window modal. This avoids a
            # half-created 200x200 Toplevel if something goes wrong while the
            # transaction is being loaded.
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

            self.update_idletasks()

            # Place the dialog near the main application rather than wherever
            # the window manager happens to choose.
            self._centre_on_parent(parent)

            self.transient(parent)
            self.deiconify()
            self.lift()
            self.focus_force()

            # wait_visibility can fail if the window was destroyed above
            # (for example a linked transfer).
            try:
                self.wait_visibility()
                self.grab_set()
            except tk.TclError:
                return

            self.date_entry.focus_set()
            self.bind("<Return>", lambda event: self.save())
            self.bind("<Escape>", lambda event: self.destroy())

        except Exception:
            # Never strand an empty Edit transaction shell if construction
            # fails unexpectedly.
            try:
                self.destroy()
            except tk.TclError:
                pass
            raise

    def _centre_on_parent(self, parent):
        try:
            self.update_idletasks()

            width = max(self.winfo_reqwidth(), 1)
            height = max(self.winfo_reqheight(), 1)

            parent.update_idletasks()
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            pw = parent.winfo_width()
            ph = parent.winfo_height()

            x = px + max(0, (pw - width) // 2)
            y = py + max(0, (ph - height) // 2)

            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

    def select_date(self):
        try:
            initial = self.app.parse_user_date(self.date_entry.get())
        except ValueError:
            initial = date.today()

        picker = DatePickerDialog(self, initial)
        self.wait_window(picker)

        try:
            self.grab_set()
        except tk.TclError:
            pass

        if picker.result is not None:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.app.format_date(picker.result))
            self.date_entry.focus_set()

    def save(self):
        if not self.account_combo.get():
            messagebox.showerror("No account", "Please select an account.", parent=self)
            return

        try:
            txn_date = self.app.parse_user_date(self.date_entry.get()).isoformat()
        except ValueError:
            messagebox.showerror(
                "Invalid date", f"Use date format {self.app.date_format_example()}.", parent=self
            )
            return

        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid amount", "Amount must be a number.", parent=self
            )
            return

        account_id = self.app.account_name_to_id[self.account_combo.get()]
        category_id = self.app.category_name_to_id.get(self.category_combo.get())

        try:
            if self.txn_id:
                self.app.db.update_transaction(
                    self.txn_id,
                    txn_date,
                    account_id,
                    category_id,
                    self.payee_entry.get().strip(),
                    self.memo_entry.get().strip(),
                    amount,
                )
            else:
                self.app.db.add_transaction(
                    txn_date,
                    account_id,
                    category_id,
                    self.payee_entry.get().strip(),
                    self.memo_entry.get().strip(),
                    amount,
                )
        except ValueError as exc:
            messagebox.showerror("Cannot save", str(exc), parent=self)
            return

        self.result = True
        self.destroy()


class TransferDialog(tk.Toplevel):
    def __init__(self, parent, app, preset_from=None):
        super().__init__(parent)
        self.app = app
        self.result = False

        self.title("Transfer between accounts")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Date").grid(row=0, column=0, sticky="w")
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=1, column=0, padx=(0, 8), pady=(0, 10), sticky="w")

        self.date_entry = ttk.Entry(date_frame, width=12)
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, app.format_date(date.today()))

        ttk.Button(
            date_frame,
            text="Select date…",
            command=self.select_date,
        ).pack(side="left", padx=(5, 0))

        ttk.Label(frame, text="From account").grid(row=0, column=1, sticky="w")
        self.from_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.from_combo.grid(row=1, column=1, padx=(0, 8), pady=(0, 10))

        ttk.Label(frame, text="To account").grid(row=0, column=2, sticky="w")
        self.to_combo = ttk.Combobox(frame, state="readonly", width=24)
        self.to_combo.grid(row=1, column=2, pady=(0, 10))

        ttk.Label(frame, text="Amount").grid(row=2, column=0, sticky="w")
        self.amount_entry = ttk.Entry(frame, width=16)
        self.amount_entry.grid(row=3, column=0, padx=(0, 8), pady=(0, 10))

        ttk.Label(frame, text="Memo").grid(row=2, column=1, sticky="w")
        self.memo_entry = ttk.Entry(frame, width=50)
        self.memo_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=(0, 12))

        buttons = ttk.Frame(frame)
        buttons.grid(row=4, column=0, columnspan=3, sticky="e")
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(buttons, text="Create transfer", command=self.save).pack(side="right")

        names = list(app.account_name_to_id.keys())
        self.from_combo["values"] = names
        self.to_combo["values"] = names

        if preset_from and preset_from in names:
            self.from_combo.set(preset_from)
        elif names:
            self.from_combo.set(names[0])

        if len(names) > 1:
            self.to_combo.set(names[1] if names[0] == self.from_combo.get() else names[0])
        elif names:
            self.to_combo.set(names[0])

        self.bind("<Escape>", lambda event: self.destroy())

    def select_date(self):
        try:
            initial = self.app.parse_user_date(self.date_entry.get())
        except ValueError:
            initial = date.today()

        picker = DatePickerDialog(self, initial)
        self.wait_window(picker)

        try:
            self.grab_set()
        except tk.TclError:
            pass

        if picker.result is not None:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.app.format_date(picker.result))
            self.date_entry.focus_set()

    def save(self):
        try:
            txn_date = self.app.parse_user_date(self.date_entry.get()).isoformat()
        except ValueError:
            messagebox.showerror(
                "Invalid date", f"Use date format {self.app.date_format_example()}.", parent=self
            )
            return

        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid amount", "Amount must be a number.", parent=self
            )
            return

        if not self.from_combo.get() or not self.to_combo.get():
            messagebox.showerror(
                "Missing account", "Select both accounts.", parent=self
            )
            return

        from_id = self.app.account_name_to_id[self.from_combo.get()]
        to_id = self.app.account_name_to_id[self.to_combo.get()]

        try:
            self.app.db.add_transfer(
                txn_date,
                from_id,
                to_id,
                amount,
                self.memo_entry.get().strip(),
            )
        except ValueError as exc:
            messagebox.showerror("Cannot transfer", str(exc), parent=self)
            return

        self.result = True
        self.destroy()


class PDFStatementRowDialog(tk.Toplevel):
    def __init__(self, parent, app, row=None):
        super().__init__(parent)
        self.app = app
        self.row = row or {}
        self.result = None
        self.title("Edit PDF statement row" if row else "Add PDF statement row")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Date:").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(frame, width=18)
        self.date_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, sticky="w", pady=5)
        self.description_entry = ttk.Entry(frame, width=55)
        self.description_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Amount:").grid(row=2, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(frame, width=18)
        self.amount_entry.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(
            frame,
            text="Use a negative amount for money out and a positive amount for money in.",
        ).grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="Statement balance:").grid(row=4, column=0, sticky="w", pady=5)
        self.balance_entry = ttk.Entry(frame, width=18)
        self.balance_entry.grid(row=4, column=1, sticky="w", pady=5)
        ttk.Label(
            frame,
            text="Optional running balance shown on the PDF statement.",
        ).grid(row=5, column=1, sticky="w")

        if row:
            self.date_entry.insert(0, app.format_date(row["txn_date"]))
            self.description_entry.insert(0, row.get("description", ""))
            self.amount_entry.insert(0, f'{float(row.get("amount", 0.0)):.2f}')
            if row.get("statement_balance") is not None:
                self.balance_entry.insert(0, f'{float(row["statement_balance"]):.2f}')
        else:
            self.date_entry.insert(0, app.format_date(date.today()))
            self.amount_entry.insert(0, "0.00")

        buttons = ttk.Frame(frame)
        buttons.grid(row=6, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(buttons, text="Save", command=self.save).pack(side="right", padx=(0, 8))

        frame.columnconfigure(1, weight=1)
        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.destroy())
        self.date_entry.focus_set()

    def save(self):
        try:
            txn_date = self.app.parse_user_date(self.date_entry.get()).isoformat()
            amount = float(
                self.amount_entry.get().replace("£", "").replace(",", "").strip()
            )
            raw_balance = self.balance_entry.get().replace("£", "").replace(",", "").strip()
            statement_balance = float(raw_balance) if raw_balance else None
        except ValueError:
            messagebox.showerror(
                "Invalid value",
                "Check the date, amount and statement balance values.",
                parent=self,
            )
            return

        description = self.description_entry.get().strip() or "Statement transaction"
        self.result = {
            "txn_date": txn_date,
            "description": description,
            "amount": amount,
            "statement_balance": statement_balance,
        }
        self.destroy()


class PDFMatchChooserDialog(tk.Toplevel):
    def __init__(self, parent, app, candidates, statement_row):
        super().__init__(parent)
        self.app = app
        self.result = None
        self.title("Choose Account Transaction")
        self.geometry("850x390")
        self.transient(parent)
        self.grab_set()

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer,
            text=(
                f'Statement: {app.format_date(statement_row["txn_date"])}  '
                f'{statement_row["description"]}  {money(statement_row["amount"])}'
            ),
            style="Heading.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        ttk.Label(
            outer,
            text=(
                "Candidates have the same amount and are within 14 days of the statement date. "
                "Choose the transaction that represents this statement line."
            ),
            wraplength=800,
        ).pack(anchor="w", pady=(0, 8))

        columns = ("id", "date", "description", "memo", "amount", "reconciled")
        self.tree = ttk.Treeview(outer, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "ID", "date": "Date", "description": "Description",
            "memo": "Memo", "amount": "Amount", "reconciled": "Reconciled ✓",
        }
        widths = {"id": 55, "date": 100, "description": 250, "memo": 250, "amount": 100, "reconciled": 90}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="e" if col == "amount" else "w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda e: self.choose())

        for row in candidates:
            self.tree.insert(
                "", "end",
                values=(
                    row["id"], app.format_date(row["txn_date"]), row["payee"],
                    row["memo"], money(row["amount"]), "✓" if row["reconciled"] else "",
                ),
            )

        buttons = ttk.Frame(outer)
        buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(buttons, text="Use Selected", command=self.choose).pack(side="right", padx=(0, 8))

    def choose(self):
        selection = self.tree.selection()
        if not selection:
            return
        txn_id = int(self.tree.item(selection[0])["values"][0])
        self.result = txn_id
        self.destroy()


class PDFReconciliationDialog(tk.Toplevel):
    def __init__(self, parent, app, pdf_path, parsed, preset_account=None):
        super().__init__(parent)
        self.app = app
        self.pdf_path = Path(pdf_path)
        self.source_hash = hashlib.sha256(self.pdf_path.read_bytes()).hexdigest()
        self.statement_rows = [dict(row) for row in parsed.get("transactions", [])]
        self.parser_warnings = list(parsed.get("warnings", []))
        self.parsed_period_start = parsed.get("period_start")
        self.parsed_period_end = parsed.get("period_end")
        self.statement_paid_in = parsed.get("statement_paid_in")
        self.statement_withdrawn = parsed.get("statement_withdrawn")
        self.matches = {}
        self.manual_match_ids = {}
        self.confirmed_rows = set()
        self.cleared_rows = set()
        self.item_to_index = {}
        self.unmatched_account_rows = []
        self.result = False

        self.title("Reconcile PDF Bank Statement")
        self.geometry("1450x820")
        self.minsize(1100, 680)
        self.transient(parent)
        self.grab_set()

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="Account:", style="Heading.TLabel").pack(side="left")
        self.account_combo = ttk.Combobox(top, state="readonly", width=28)
        self.account_combo.pack(side="left", padx=(8, 16))
        account_names = list(app.account_name_to_id.keys())
        self.account_combo["values"] = account_names
        if preset_account in account_names:
            self.account_combo.set(preset_account)
        elif account_names:
            self.account_combo.set(account_names[0])
        self.account_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_matches())

        ttk.Label(top, text=f"PDF: {self.pdf_path.name}").pack(side="left")
        ttk.Button(top, text="Refresh Matches", command=self.refresh_matches).pack(side="right")

        balances = ttk.LabelFrame(outer, text="Statement balances", padding=8)
        balances.pack(fill="x", pady=(0, 8))

        ttk.Label(balances, text="Opening balance:").pack(side="left")
        self.opening_var = tk.StringVar(
            value="" if parsed.get("opening_balance") is None else f'{parsed["opening_balance"]:.2f}'
        )
        ttk.Entry(balances, textvariable=self.opening_var, width=14).pack(side="left", padx=(6, 18))

        ttk.Label(balances, text="Closing balance:").pack(side="left")
        self.closing_var = tk.StringVar(
            value="" if parsed.get("closing_balance") is None else f'{parsed["closing_balance"]:.2f}'
        )
        ttk.Entry(balances, textvariable=self.closing_var, width=14).pack(side="left", padx=(6, 18))

        ttk.Button(balances, text="Recalculate", command=self.refresh_matches).pack(side="left")

        self.period_var = tk.StringVar(value="Statement period: -")
        ttk.Label(balances, textvariable=self.period_var).pack(side="right")

        self.warning_var = tk.StringVar(value="  ".join(self.parser_warnings))
        self.warning_label = tk.Label(
            outer, textvariable=self.warning_var, anchor="w", justify="left",
            foreground="#8a5a00", wraplength=1360,
        )
        self.warning_label.pack(fill="x", pady=(0, 6))

        summary = ttk.LabelFrame(outer, text="Reconciliation checks", padding=8)
        summary.pack(fill="x", pady=(0, 8))

        self.statement_check_var = tk.StringVar(value="Statement check: -")
        self.statement_check_label = tk.Label(summary, textvariable=self.statement_check_var, anchor="w")
        self.statement_check_label.pack(fill="x")

        self.pdf_totals_var = tk.StringVar(value="PDF totals check: -")
        self.pdf_totals_label = tk.Label(
            summary, textvariable=self.pdf_totals_var, anchor="w"
        )
        self.pdf_totals_label.pack(fill="x")

        self.reconcile_check_var = tk.StringVar(value="Reconciliation difference: -")
        self.reconcile_check_label = tk.Label(summary, textvariable=self.reconcile_check_var, anchor="w")
        self.reconcile_check_label.pack(fill="x")

        self.ledger_check_var = tk.StringVar(value="Account ledger at statement end: -")
        self.ledger_check_label = tk.Label(summary, textvariable=self.ledger_check_var, anchor="w")
        self.ledger_check_label.pack(fill="x")

        self.unmatched_var = tk.StringVar(value="Unmatched account entries in period: -")
        self.unmatched_label = tk.Label(summary, textvariable=self.unmatched_var, anchor="w")
        self.unmatched_label.pack(fill="x")

        overall = ttk.LabelFrame(
            outer,
            text="Overall reconciliation status",
            padding=(10, 8),
        )
        overall.pack(fill="x", pady=(0, 8))

        self.overall_status_var = tk.StringVar(
            value="PDF: CHECKING...    Account: 0/0 matched    Remaining: -"
        )
        self.overall_status_label = tk.Label(
            overall,
            textvariable=self.overall_status_var,
            anchor="w",
            justify="left",
            font=("Sans", 12, "bold"),
        )
        self.overall_status_label.pack(fill="x")

        self.overall_help_var = tk.StringVar(
            value=(
                "Resolve any red/yellow statement rows. When every check passes, "
                "the final reconciliation button will become available."
            )
        )
        tk.Label(
            overall,
            textvariable=self.overall_help_var,
            anchor="w",
            justify="left",
            foreground="#555555",
        ).pack(fill="x", pady=(3, 0))

        columns = (
            "stmt_date", "stmt_desc", "stmt_amount", "stmt_balance", "pdf_check",
            "account_date", "account_desc", "account_amount", "status",
        )
        self.tree = ttk.Treeview(outer, columns=columns, show="headings", selectmode="browse")
        headings = {
            "stmt_date": "Statement Date", "stmt_desc": "Statement Description",
            "stmt_amount": "Statement Amount", "stmt_balance": "Statement Balance",
            "pdf_check": "PDF Check",
            "account_date": "Account Date", "account_desc": "Matched Account Transaction",
            "account_amount": "Account Amount", "status": "Status",
        }
        widths = {
            "stmt_date": 105, "stmt_desc": 260, "stmt_amount": 115, "stmt_balance": 120,
            "pdf_check": 95,
            "account_date": 105, "account_desc": 260, "account_amount": 115, "status": 165,
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col, width=widths[col],
                anchor="e" if col in ("stmt_amount", "stmt_balance", "account_amount") else "w",
            )
        self.tree.tag_configure("matched", background="#dff3df")
        self.tree.tag_configure("possible", background="#fff3b0")
        self.tree.tag_configure("missing", background="#ffd6d6")
        self.tree.tag_configure("already", foreground="#777777")
        self.tree.tag_configure("pdf_error", background="#ffb3b3")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda e: self.edit_statement_row())

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(8, 0))
        ttk.Button(controls, text="Edit PDF Row", command=self.edit_statement_row).pack(side="left")
        ttk.Button(controls, text="Add PDF Row", command=self.add_statement_row).pack(side="left", padx=(6, 0))
        ttk.Button(controls, text="Delete PDF Row", command=self.delete_statement_row).pack(side="left", padx=(6, 0))
        ttk.Separator(controls, orient="vertical").pack(side="left", fill="y", padx=10)
        ttk.Button(controls, text="Confirm Selected Match", command=self.confirm_selected_match).pack(side="left")
        ttk.Button(controls, text="Choose / Change Match...", command=self.choose_match).pack(side="left", padx=(6, 0))
        ttk.Button(controls, text="Clear Match", command=self.clear_match).pack(side="left", padx=(6, 0))
        ttk.Button(controls, text="Add Missing to Account...", command=self.add_missing_to_account).pack(side="left", padx=(6, 0))
        ttk.Button(controls, text="View Unmatched Account Entries", command=self.view_unmatched_account_entries).pack(side="left", padx=(6, 0))

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text="Cancel", command=self.destroy).pack(side="right")
        self.complete_button = ttk.Button(
            bottom,
            text="Confirm && Mark Reconciled ✓",
            command=self.complete_reconciliation,
            state="disabled",
        )
        self.complete_button.pack(side="right", padx=(0, 8))

        self.after(50, self.refresh_matches)

    def account_id(self):
        return self.app.account_name_to_id.get(self.account_combo.get())

    @staticmethod
    def _parse_balance_field(value):
        raw = (value or "").replace("£", "").replace(",", "").strip()
        if not raw:
            return None
        return float(raw)

    def selected_index(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.item_to_index.get(selection[0])

    def statement_period(self):
        if self.parsed_period_start and self.parsed_period_end:
            try:
                return (
                    parse_date(self.parsed_period_start),
                    parse_date(self.parsed_period_end),
                )
            except ValueError:
                pass

        if not self.statement_rows:
            return None, None

        dates = [parse_date(row["txn_date"]) for row in self.statement_rows]
        return min(dates), max(dates)


    def row_confirmed(self, index, match):
        if not match:
            return False
        if match.get("confidence") in ("likely", "already_reconciled"):
            return True
        if index in self.manual_match_ids or index in self.confirmed_rows:
            return True
        return False

    def refresh_matches(self):
        account_id = self.account_id()
        if not account_id:
            return

        auto_matches = self.app.db.auto_match_statement_transactions(
            account_id, self.statement_rows, date_window_days=4
        )

        self.matches = {}
        used_ids = set()
        for index in range(len(self.statement_rows)):
            if index in self.cleared_rows:
                continue
            manual_id = self.manual_match_ids.get(index)
            if manual_id:
                txn = self.app.db.get_transaction(manual_id)
                if txn and txn["account_id"] == account_id and abs(float(txn["amount"]) - float(self.statement_rows[index]["amount"])) < 0.005:
                    self.matches[index] = {
                        "id": txn["id"], "txn_date": txn["txn_date"],
                        "payee": txn["payee"] or "", "memo": txn["memo"] or "",
                        "amount": float(txn["amount"]), "reconciled": txn["reconciled"],
                        "confidence": "already_reconciled" if txn["reconciled"] else "manual",
                    }
                    used_ids.add(txn["id"])
                    continue
            match = auto_matches.get(index)
            if match and match["id"] not in used_ids:
                self.matches[index] = match
                used_ids.add(match["id"])

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.item_to_index = {}

        for index, row in enumerate(self.statement_rows):
            match = self.matches.get(index)
            tag = "missing"
            status = "Missing from account"
            account_date = account_desc = account_amount = ""

            if match:
                account_date = self.app.format_date(match["txn_date"])
                account_desc = match.get("payee") or match.get("memo") or "Account transaction"
                account_amount = money(match["amount"])
                if match.get("confidence") == "already_reconciled" or match.get("reconciled"):
                    status = "Already reconciled"
                    tag = "already"
                elif self.row_confirmed(index, match):
                    status = "Matched"
                    tag = "matched"
                else:
                    status = "Possible - confirm"
                    tag = "possible"

            stmt_balance = ""
            if row.get("statement_balance") is not None:
                stmt_balance = money(row["statement_balance"])

            pdf_check = ""
            pdf_diff = row.get("pdf_check_difference")
            if pdf_diff is not None:
                if abs(float(pdf_diff)) <= 0.01:
                    pdf_check = "OK"
                else:
                    pdf_check = f"Off {money(pdf_diff)}"
                    tag = "pdf_error"

            item = self.tree.insert(
                "", "end",
                values=(
                    self.app.format_date(row["txn_date"]), row["description"],
                    money(row["amount"]), stmt_balance, pdf_check,
                    account_date, account_desc, account_amount, status,
                ),
                tags=(tag,),
            )
            self.item_to_index[item] = index

        start, end = self.statement_period()
        if start and end:
            self.period_var.set(
                f"Statement period: {self.app.format_date(start)} to {self.app.format_date(end)}"
            )
            matched_ids = [m["id"] for m in self.matches.values()]
            self.unmatched_account_rows = self.app.db.get_unmatched_account_transactions(
                account_id, start.isoformat(), end.isoformat(), matched_ids
            )
        else:
            self.period_var.set("Statement period: -")
            self.unmatched_account_rows = []

        self.update_checks()

    def update_checks(self):
        try:
            opening = self._parse_balance_field(self.opening_var.get())
            closing = self._parse_balance_field(self.closing_var.get())
        except ValueError:
            opening = closing = None

        activity = sum(float(row["amount"]) for row in self.statement_rows)
        parsed_paid_in = sum(
            float(row["amount"])
            for row in self.statement_rows
            if float(row["amount"]) > 0
        )
        parsed_withdrawn = sum(
            -float(row["amount"])
            for row in self.statement_rows
            if float(row["amount"]) < 0
        )

        bad_pdf_rows = [
            row
            for row in self.statement_rows
            if row.get("pdf_check_difference") is not None
            and abs(float(row["pdf_check_difference"])) > 0.01
        ]

        if opening is not None and closing is not None:
            calculated = opening + activity
            difference = round(calculated - closing, 2)
            row_note = (
                f"; row checks failing: {len(bad_pdf_rows)}"
                if bad_pdf_rows
                else "; all running-balance row checks OK"
            )
            self.statement_check_var.set(
                f"Statement check: {money(opening)} + activity {money(activity)} = "
                f"{money(calculated)}; PDF closing {money(closing)}; difference {money(difference)}"
                f"{row_note}"
            )
            statement_ok = abs(difference) <= 0.01 and not bad_pdf_rows
            self.statement_check_label.configure(
                foreground="#157a2c" if statement_ok else "red"
            )
        else:
            self.statement_check_var.set("Statement check: enter/verify both opening and closing balances.")
            self.statement_check_label.configure(foreground="red")

        if (
            self.statement_paid_in is not None
            and self.statement_withdrawn is not None
        ):
            paid_diff = round(
                parsed_paid_in - float(self.statement_paid_in), 2
            )
            withdrawn_diff = round(
                parsed_withdrawn - float(self.statement_withdrawn), 2
            )
            totals_ok = (
                abs(paid_diff) <= 0.01
                and abs(withdrawn_diff) <= 0.01
            )
            self.pdf_totals_var.set(
                f"PDF totals check: Paid In PDF {money(self.statement_paid_in)} / "
                f"parsed {money(parsed_paid_in)}; "
                f"Withdrawn PDF {money(self.statement_withdrawn)} / "
                f"parsed {money(parsed_withdrawn)}; "
                f"{'OK' if totals_ok else 'DISCREPANCY'}"
            )
            self.pdf_totals_label.configure(
                foreground="#157a2c" if totals_ok else "red"
            )
        else:
            self.pdf_totals_var.set(
                "PDF totals check: summary Paid In/Withdrawn totals not available."
            )
            self.pdf_totals_label.configure(foreground="#666666")

        confirmed_activity = 0.0
        confirmed_count = 0
        for index, row in enumerate(self.statement_rows):
            match = self.matches.get(index)
            if match and self.row_confirmed(index, match):
                confirmed_activity += float(match["amount"])
                confirmed_count += 1

        if opening is not None and closing is not None:
            reconciled_closing = opening + confirmed_activity
            reconcile_difference = round(reconciled_closing - closing, 2)
            self.reconcile_check_var.set(
                f"Reconciliation: {confirmed_count}/{len(self.statement_rows)} statement rows matched/confirmed; "
                f"matched closing {money(reconciled_closing)}; difference {money(reconcile_difference)}"
            )
            all_matched = confirmed_count == len(self.statement_rows)
            ok = all_matched and abs(reconcile_difference) <= 0.01
            self.reconcile_check_label.configure(foreground="#157a2c" if ok else "red")
        else:
            self.reconcile_check_var.set("Reconciliation difference: waiting for valid statement balances.")
            self.reconcile_check_label.configure(foreground="red")

        start, end = self.statement_period()
        account_id = self.account_id()
        if account_id and end and closing is not None:
            ledger = self.app.db.get_account_balance_through_date(account_id, end.isoformat())
            ledger_diff = round(float(ledger) - closing, 2)
            self.ledger_check_var.set(
                f"Account ledger at {self.app.format_date(end)}: {money(ledger)}; "
                f"statement closing {money(closing)}; difference {money(ledger_diff)} "
                "(can include entries not yet cleared by the bank)"
            )
            self.ledger_check_label.configure(
                foreground="#157a2c" if abs(ledger_diff) <= 0.01 else "#8a5a00"
            )
        else:
            self.ledger_check_var.set("Account ledger at statement end: -")

        unmatched_total = sum(float(row["amount"]) for row in self.unmatched_account_rows)
        self.unmatched_var.set(
            f"Unmatched unreconciled Account Transactions inside the statement period: "
            f"{len(self.unmatched_account_rows)}  Total: {money(unmatched_total)}"
        )
        self.unmatched_label.configure(
            foreground="#8a5a00" if self.unmatched_account_rows else "#157a2c"
        )

        # --------------------------------------------------------------
        # Overall, easy-to-read reconciliation status.
        # --------------------------------------------------------------
        pdf_balance_ok = False
        if opening is not None and closing is not None:
            pdf_balance_ok = (
                abs(round(opening + activity - closing, 2)) <= 0.01
                and not bad_pdf_rows
            )

        if (
            self.statement_paid_in is not None
            and self.statement_withdrawn is not None
        ):
            pdf_totals_ok = (
                abs(round(parsed_paid_in - float(self.statement_paid_in), 2)) <= 0.01
                and abs(
                    round(
                        parsed_withdrawn - float(self.statement_withdrawn),
                        2,
                    )
                )
                <= 0.01
            )
        else:
            # Older/generic PDFs may not contain separate summary totals.
            pdf_totals_ok = True

        pdf_verified = pdf_balance_ok and pdf_totals_ok

        total_rows = len(self.statement_rows)
        remaining = max(0, total_rows - confirmed_count)

        reconciliation_zero = False
        if opening is not None and closing is not None:
            reconciliation_zero = (
                abs(
                    round(
                        opening + confirmed_activity - closing,
                        2,
                    )
                )
                <= 0.01
            )

        ready = (
            pdf_verified
            and total_rows > 0
            and confirmed_count == total_rows
            and reconciliation_zero
        )

        pdf_text = "PDF: VERIFIED ✓" if pdf_verified else "PDF: CHECK REQUIRED ✗"

        if ready:
            state_text = "READY TO MARK RECONCILED ✓"
            status_colour = "#157a2c"
            help_text = (
                "Everything agrees. Click “Confirm & Mark Reconciled ✓” to mark "
                "the matched Account Transactions as reconciled."
            )
            self.complete_button.configure(state="normal")
        else:
            state_text = "NOT READY"
            status_colour = "#8a5a00" if pdf_verified else "red"
            if not pdf_verified:
                help_text = (
                    "The PDF itself still has a balance/summary discrepancy. "
                    "Correct that before reconciling the account."
                )
            elif remaining:
                help_text = (
                    f"Resolve the remaining {remaining} red/yellow statement row(s). "
                    "Green Matched rows are already accepted."
                )
            else:
                help_text = (
                    "All rows are matched, but the matched Account Transactions "
                    "still do not reproduce the statement closing balance."
                )
            self.complete_button.configure(state="disabled")

        self.overall_status_var.set(
            f"{pdf_text}    |    "
            f"Account: {confirmed_count}/{total_rows} matched    |    "
            f"Remaining: {remaining}    |    {state_text}"
        )
        self.overall_status_label.configure(foreground=status_colour)
        self.overall_help_var.set(help_text)

    def edit_statement_row(self):
        index = self.selected_index()
        if index is None:
            return
        dialog = PDFStatementRowDialog(self, self.app, self.statement_rows[index])
        self.wait_window(dialog)
        if dialog.result:
            self.statement_rows[index] = dialog.result
            self.manual_match_ids.pop(index, None)
            self.confirmed_rows.discard(index)
            self.cleared_rows.discard(index)
            self.refresh_matches()

    def add_statement_row(self):
        dialog = PDFStatementRowDialog(self, self.app)
        self.wait_window(dialog)
        if dialog.result:
            self.statement_rows.append(dialog.result)
            self.statement_rows.sort(key=lambda r: r["txn_date"])
            self.manual_match_ids.clear()
            self.confirmed_rows.clear()
            self.cleared_rows.clear()
            self.refresh_matches()

    def delete_statement_row(self):
        index = self.selected_index()
        if index is None:
            return
        row = self.statement_rows[index]
        if not messagebox.askyesno(
            "Delete parsed statement row",
            f'Delete this row from the reconciliation copy?\n\n{row["description"]}  {money(row["amount"])}\n\n'
            "This does not alter the original PDF or Account Transactions.",
            parent=self,
        ):
            return
        del self.statement_rows[index]
        self.manual_match_ids.clear()
        self.confirmed_rows.clear()
        self.cleared_rows.clear()
        self.refresh_matches()

    def confirm_selected_match(self):
        index = self.selected_index()
        if index is None or index not in self.matches:
            return
        self.confirmed_rows.add(index)
        self.cleared_rows.discard(index)
        self.refresh_matches()

    def choose_match(self):
        index = self.selected_index()
        if index is None:
            return
        row = self.statement_rows[index]
        account_id = self.account_id()
        if not account_id:
            return
        candidates = self.app.db.get_reconciliation_candidates(
            account_id, row["txn_date"], row["amount"], date_window_days=14
        )
        used_elsewhere = {
            match["id"] for other, match in self.matches.items() if other != index
        }
        candidates = [c for c in candidates if c["id"] not in used_elsewhere]
        if not candidates:
            messagebox.showinfo(
                "No candidates",
                "No Account Transaction with the same amount was found within 14 days.\n\n"
                "If this transaction is genuinely missing, use 'Add Missing to Account...'.",
                parent=self,
            )
            return
        dialog = PDFMatchChooserDialog(self, self.app, candidates, row)
        self.wait_window(dialog)
        if dialog.result:
            self.manual_match_ids[index] = dialog.result
            self.confirmed_rows.add(index)
            self.cleared_rows.discard(index)
            self.refresh_matches()

    def clear_match(self):
        index = self.selected_index()
        if index is None:
            return
        self.manual_match_ids.pop(index, None)
        self.confirmed_rows.discard(index)
        self.cleared_rows.add(index)
        self.refresh_matches()

    def add_missing_to_account(self):
        index = self.selected_index()
        if index is None:
            return
        row = self.statement_rows[index]
        account_id = self.account_id()
        if not account_id:
            return
        if index in self.matches and self.row_confirmed(index, self.matches[index]):
            messagebox.showinfo("Already matched", "This statement row already has a confirmed match.", parent=self)
            return

        if not messagebox.askyesno(
            "Add missing transaction",
            f'Add this statement transaction to "{self.account_combo.get()}"?\n\n'
            f'Date: {self.app.format_date(row["txn_date"])}\n'
            f'Description: {row["description"]}\n'
            f'Amount: {money(row["amount"])}\n\n'
            "It will be added without a category. You can categorise it later in Account Transactions.",
            parent=self,
        ):
            return

        txn_id = self.app.db.add_transaction(
            row["txn_date"], account_id, None, row["description"],
            "Added from PDF statement reconciliation", row["amount"],
        )
        self.manual_match_ids[index] = txn_id
        self.confirmed_rows.add(index)
        self.cleared_rows.discard(index)
        self.app.refresh_all()
        self.refresh_matches()

    def view_unmatched_account_entries(self):
        if not self.unmatched_account_rows:
            messagebox.showinfo(
                "Unmatched account entries",
                "There are no unmatched unreconciled Account Transactions inside this statement period.",
                parent=self,
            )
            return
        window = tk.Toplevel(self)
        window.title("Unmatched Account Transactions")
        window.geometry("850x400")
        window.transient(self)
        frame = ttk.Frame(window, padding=10)
        frame.pack(fill="both", expand=True)
        ttk.Label(
            frame,
            text=(
                "These Account Transactions are dated inside the statement period but were not matched "
                "to a PDF statement row. They may simply be uncleared/pending entries."
            ),
            wraplength=800,
        ).pack(anchor="w", pady=(0, 8))
        columns = ("date", "description", "memo", "amount")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, heading, width in (
            ("date", "Date", 110), ("description", "Description", 280),
            ("memo", "Memo", 300), ("amount", "Amount", 110),
        ):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="e" if col == "amount" else "w")
        tree.pack(fill="both", expand=True)
        for row in self.unmatched_account_rows:
            tree.insert("", "end", values=(
                self.app.format_date(row["txn_date"]), row["payee"], row["memo"], money(row["amount"])
            ))
        ttk.Button(frame, text="Close", command=window.destroy).pack(anchor="e", pady=(8, 0))

    def complete_reconciliation(self):
        account_id = self.account_id()
        if not account_id or not self.statement_rows:
            return
        try:
            opening = self._parse_balance_field(self.opening_var.get())
            closing = self._parse_balance_field(self.closing_var.get())
        except ValueError:
            opening = closing = None
        if opening is None or closing is None:
            messagebox.showerror("Balances required", "Enter and verify the statement opening and closing balances.", parent=self)
            return

        activity = sum(float(row["amount"]) for row in self.statement_rows)
        parsed_paid_in = sum(
            float(row["amount"])
            for row in self.statement_rows
            if float(row["amount"]) > 0
        )
        parsed_withdrawn = sum(
            -float(row["amount"])
            for row in self.statement_rows
            if float(row["amount"]) < 0
        )

        if (
            self.statement_paid_in is not None
            and self.statement_withdrawn is not None
        ):
            paid_diff = round(
                parsed_paid_in - float(self.statement_paid_in), 2
            )
            withdrawn_diff = round(
                parsed_withdrawn - float(self.statement_withdrawn), 2
            )
            if abs(paid_diff) > 0.01 or abs(withdrawn_diff) > 0.01:
                messagebox.showerror(
                    "PDF summary totals do not agree",
                    "The parsed transactions do not match the Paid In/Withdrawn "
                    "totals printed in the PDF summary.\n\n"
                    f"Paid In difference: {money(paid_diff)}\n"
                    f"Withdrawn difference: {money(withdrawn_diff)}\n\n"
                    "Review the statement rows before reconciling.",
                    parent=self,
                )
                return

        bad_pdf_rows = [
            row
            for row in self.statement_rows
            if row.get("pdf_check_difference") is not None
            and abs(float(row["pdf_check_difference"])) > 0.01
        ]
        if bad_pdf_rows:
            messagebox.showerror(
                "PDF row discrepancies",
                f"{len(bad_pdf_rows)} parsed statement row(s) do not agree with "
                "the PDF running balance.\n\n"
                "Review the red PDF Check rows before reconciling.",
                parent=self,
            )
            return

        statement_diff = round(opening + activity - closing, 2)
        if abs(statement_diff) > 0.01:
            messagebox.showerror(
                "Statement does not balance",
                f"The parsed PDF does not balance by {money(statement_diff)}.\n\n"
                "Check the opening/closing balances and edit any incorrectly parsed PDF rows before reconciling.",
                parent=self,
            )
            return

        unconfirmed = []
        transaction_ids = []
        confirmed_activity = 0.0
        for index, row in enumerate(self.statement_rows):
            match = self.matches.get(index)
            if not match or not self.row_confirmed(index, match):
                unconfirmed.append(index)
                continue
            transaction_ids.append(match["id"])
            confirmed_activity += float(match["amount"])

        if unconfirmed:
            messagebox.showerror(
                "Unmatched statement rows",
                f"{len(unconfirmed)} statement transaction(s) are still missing or need confirmation.\n\n"
                "Resolve the red/yellow rows before completing reconciliation.",
                parent=self,
            )
            return

        reconciliation_diff = round(opening + confirmed_activity - closing, 2)
        if abs(reconciliation_diff) > 0.01:
            messagebox.showerror(
                "Reconciliation difference",
                f"The matched Account Transactions differ from the statement by {money(reconciliation_diff)}.",
                parent=self,
            )
            return

        existing = self.app.db.get_reconciliation_by_hash(account_id, self.source_hash)
        if existing:
            messagebox.showinfo(
                "Already reconciled",
                "This exact PDF statement has already been reconciled for this account.",
                parent=self,
            )
            return

        start, end = self.statement_period()
        if not messagebox.askyesno(
            "Complete reconciliation",
            f'Mark {len(set(transaction_ids))} Account Transaction(s) as reconciled?\n\n'
            f'Statement: {self.app.format_date(start)} to {self.app.format_date(end)}\n'
            f'Closing balance: {money(closing)}\n'
            'Reconciliation difference: £0.00',
            parent=self,
        ):
            return

        try:
            reconciliation_id = self.app.db.complete_reconciliation(
                account_id, start.isoformat(), end.isoformat(), opening, closing,
                transaction_ids, self.pdf_path.name, self.source_hash,
            )
        except (sqlite3.IntegrityError, ValueError) as exc:
            messagebox.showerror("Could not reconcile", str(exc), parent=self)
            return

        self.app.refresh_all()
        self.app.notebook.select(self.app.register_tab)
        self.result = True

        marked_count = len(set(transaction_ids))
        messagebox.showinfo(
            "Reconciliation complete",
            f"Statement reconciled successfully.\n\n"
            f"Reconciliation #{reconciliation_id}\n"
            f"Closing balance: {money(closing)}\n"
            f"Difference: £0.00\n\n"
            f"{marked_count} Account Transaction(s) were marked reconciled.\n"
            "They now show a ✓ in the Reconciled column on Account Transactions.",
            parent=self,
        )
        self.destroy()


class BankStatementImportDialog(tk.Toplevel):
    """Preview an OFX/QFX statement and choose which unseen transactions to import."""

    def __init__(self, parent, app, statements, source_path):
        super().__init__(parent)
        self.app = app
        self.statements = statements
        self.source_path = Path(source_path)
        self.result = False

        # Tree item -> transaction dictionary.
        self.item_to_txn = {}
        self.new_item_ids = []
        self.likely_manual_item_ids = []
        self.current_existing_ids = set()
        self.current_manual_matches = {}
        self.current_new_count = 0
        self.current_duplicate_count = 0
        self.current_likely_manual_count = 0
        self.current_possible_manual_count = 0

        self.title("Import bank statement")
        self.geometry("1080x690")
        self.minsize(920, 540)
        self.transient(parent)
        self.grab_set()

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        controls = ttk.LabelFrame(outer, text="Statement", padding=10)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="OFX account").grid(row=0, column=0, sticky="w")
        self.source_combo = ttk.Combobox(
            controls, state="readonly", width=34
        )
        self.source_combo.grid(row=1, column=0, padx=(0, 12), sticky="w")
        self.source_combo["values"] = [
            statement["source_label"] for statement in statements
        ]
        self.source_combo.current(0)
        self.source_combo.bind(
            "<<ComboboxSelected>>", lambda event: self.refresh_preview()
        )

        ttk.Label(controls, text="Import into Simple Finance account").grid(
            row=0, column=1, sticky="w"
        )
        self.target_combo = ttk.Combobox(
            controls, state="readonly", width=34
        )
        self.target_combo.grid(row=1, column=1, padx=(0, 12), sticky="w")

        account_names = list(app.account_name_to_id.keys())
        self.target_combo["values"] = account_names
        preferred = app.register_account.get()
        if preferred in account_names:
            self.target_combo.set(preferred)
        elif account_names:
            self.target_combo.set(account_names[0])

        self.target_combo.bind(
            "<<ComboboxSelected>>", lambda event: self.refresh_preview()
        )

        self.statement_info_var = tk.StringVar(value="")
        ttk.Label(
            controls,
            textvariable=self.statement_info_var,
            justify="left",
        ).grid(row=0, column=2, rowspan=2, sticky="w", padx=(8, 0))

        ttk.Label(
            outer,
            text=(
                "New transactions are selected automatically. "
                "Yellow/orange rows resemble manual Account Transactions. "
                "Select a manual match if you want the OFX version to replace "
                "that manual entry while preserving its category and reconciliation state."
            ),
        ).pack(anchor="w", pady=(0, 8))

        columns = (
            "date",
            "type",
            "description",
            "memo",
            "payment",
            "deposit",
            "status",
        )
        self.tree = ttk.Treeview(
            outer,
            columns=columns,
            show="headings",
            selectmode="extended",
        )

        headings = {
            "date": "Date",
            "type": "Type",
            "description": "Description",
            "memo": "Memo",
            "payment": "Payment",
            "deposit": "Deposit",
            "status": "Status",
        }
        widths = {
            "date": 100,
            "type": 90,
            "description": 230,
            "memo": 280,
            "payment": 105,
            "deposit": 105,
            "status": 300,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="e" if col in ("payment", "deposit") else "w",
            )

        self.tree.tag_configure(
            "likely_manual",
            background="#fff3b0",
        )
        self.tree.tag_configure(
            "possible_manual",
            background="#ffd8a8",
        )
        self.tree.tag_configure(
            "already_imported",
            foreground="#777777",
        )

        self.tree.pack(fill="both", expand=True)
        self.tree.bind(
            "<<TreeviewSelect>>", lambda event: self.update_selection_summary()
        )
        self.tree.bind("<Control-a>", self.select_all_new)
        self.tree.bind("<Control-A>", self.select_all_new)

        selection_bar = ttk.Frame(outer)
        selection_bar.pack(fill="x", pady=(8, 0))

        ttk.Button(
            selection_bar,
            text="Select All New",
            command=self.select_all_new,
        ).pack(side="left")

        ttk.Button(
            selection_bar,
            text="Select Likely Manual",
            command=self.select_likely_manual,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            selection_bar,
            text="Clear Selection",
            command=self.clear_selection,
        ).pack(side="left", padx=(8, 0))

        summary_frame = ttk.Frame(outer)
        summary_frame.pack(fill="x", pady=(10, 0))

        self.summary_var = tk.StringVar(value="")
        ttk.Label(
            summary_frame, textvariable=self.summary_var, style="Heading.TLabel"
        ).pack(side="left")

        ttk.Button(
            summary_frame, text="Cancel", command=self.destroy
        ).pack(side="right")

        self.import_button = ttk.Button(
            summary_frame,
            text="Import / Replace Selected",
            command=self.do_import,
        )
        self.import_button.pack(side="right", padx=(0, 8))

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda event: self.destroy())

        self.refresh_preview()

    def current_statement(self):
        index = self.source_combo.current()
        if index < 0:
            index = 0
        return self.statements[index]

    def selected_new_transactions(self):
        selected = []
        for item_id in self.tree.selection():
            txn = self.item_to_txn.get(item_id)
            if not txn:
                continue
            if txn["external_id"] in self.current_existing_ids:
                continue
            selected.append(txn)
        return selected

    def selected_import_actions(self):
        new_transactions = []
        replacements = []

        for item_id in self.tree.selection():
            txn = self.item_to_txn.get(item_id)
            if not txn:
                continue

            external_id = txn.get("external_id")
            if external_id in self.current_existing_ids:
                continue

            manual_match = self.current_manual_matches.get(external_id)
            if manual_match:
                replacements.append(
                    {
                        "manual_transaction_id": manual_match["transaction_id"],
                        "ofx_transaction": txn,
                        "confidence": manual_match["confidence"],
                        "manual_match": manual_match,
                    }
                )
            else:
                new_transactions.append(txn)

        return new_transactions, replacements

    def select_all_new(self, event=None):
        if self.new_item_ids:
            self.tree.selection_set(*self.new_item_ids)
            self.tree.focus(self.new_item_ids[0])
            self.tree.see(self.new_item_ids[0])
        self.update_selection_summary()
        return "break" if event is not None else None

    def select_likely_manual(self):
        if self.likely_manual_item_ids:
            current = list(self.tree.selection())
            combined = list(
                dict.fromkeys(current + self.likely_manual_item_ids)
            )
            self.tree.selection_set(*combined)
            self.tree.focus(self.likely_manual_item_ids[0])
            self.tree.see(self.likely_manual_item_ids[0])
        self.update_selection_summary()

    def clear_selection(self):
        selected = self.tree.selection()
        if selected:
            self.tree.selection_remove(*selected)
        self.update_selection_summary()

    def update_selection_summary(self):
        new_selected, replacements = self.selected_import_actions()
        selected = new_selected + [
            replacement["ofx_transaction"]
            for replacement in replacements
        ]

        payments = sum(
            abs(txn["amount"]) for txn in selected if txn["amount"] < 0
        )
        deposits = sum(
            txn["amount"] for txn in selected if txn["amount"] > 0
        )

        self.summary_var.set(
            f"Selected: {len(selected)} "
            f"({len(new_selected)} new + {len(replacements)} replace)    "
            f"New: {self.current_new_count}    "
            f"Likely manual: {self.current_likely_manual_count}    "
            f"Possible manual: {self.current_possible_manual_count}    "
            f"Already imported: {self.current_duplicate_count}    "
            f"Payments: {money(payments)}    Deposits: {money(deposits)}"
        )

        target_id = self.app.account_name_to_id.get(self.target_combo.get())
        if target_id and selected:
            self.import_button.state(["!disabled"])
        else:
            self.import_button.state(["disabled"])

    def refresh_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.item_to_txn.clear()
        self.new_item_ids = []
        self.likely_manual_item_ids = []

        statement = self.current_statement()
        target_name = self.target_combo.get()
        target_id = self.app.account_name_to_id.get(target_name)

        details = []
        if statement["start_date"] or statement["end_date"]:
            details.append(
                f'Period: {self.app.format_date(statement["start_date"]) if statement["start_date"] else "?"} to '
                f'{self.app.format_date(statement["end_date"]) if statement["end_date"] else "?"}'
            )
        details.append(f'Currency: {statement["currency"]}')
        if statement["ledger_balance"] is not None:
            details.append(
                f'OFX balance: {statement["ledger_balance"]:,.2f}'
            )
        self.statement_info_var.set("\n".join(details))

        external_ids = [
            txn["external_id"] for txn in statement["transactions"]
        ]
        self.current_existing_ids = (
            self.app.db.get_existing_external_ids(target_id, external_ids)
            if target_id
            else set()
        )

        unseen_transactions = [
            txn
            for txn in statement["transactions"]
            if txn["external_id"] not in self.current_existing_ids
        ]
        self.current_manual_matches = (
            self.app.db.find_manual_transaction_matches(
                target_id, unseen_transactions
            )
            if target_id
            else {}
        )

        new_count = 0
        duplicate_count = 0
        likely_manual_count = 0
        possible_manual_count = 0

        for txn in statement["transactions"]:
            duplicate = txn["external_id"] in self.current_existing_ids
            manual_match = self.current_manual_matches.get(txn["external_id"])

            tags = ()
            if duplicate:
                status = "Already imported"
                tags = ("already_imported",)
                duplicate_count += 1
            elif manual_match:
                match_name = (
                    manual_match.get("payee")
                    or manual_match.get("memo")
                    or "existing transaction"
                )
                if len(match_name) > 24:
                    match_name = match_name[:21] + "..."

                matched_date = self.app.format_date(
                    manual_match["txn_date"]
                )
                date_note = f" ({matched_date})"

                if manual_match["confidence"] == "likely":
                    status = (
                        f"Likely manual: {match_name}{date_note} — select to replace"
                    )
                    tags = ("likely_manual",)
                    likely_manual_count += 1
                else:
                    status = (
                        f"Possible manual: {match_name}{date_note} — select to replace"
                    )
                    tags = ("possible_manual",)
                    possible_manual_count += 1
            else:
                status = "New"
                new_count += 1

            item_id = self.tree.insert(
                "",
                "end",
                values=(
                    self.app.format_date(txn["txn_date"]),
                    txn["txn_type"],
                    txn["payee"],
                    txn["memo"],
                    money(abs(txn["amount"])) if txn["amount"] < 0 else "",
                    money(txn["amount"]) if txn["amount"] > 0 else "",
                    status,
                ),
                tags=tags,
            )

            self.item_to_txn[item_id] = txn

            # Only genuinely new rows are pre-selected.
            if not duplicate and manual_match is None:
                self.new_item_ids.append(item_id)
            elif (
                not duplicate
                and manual_match
                and manual_match["confidence"] == "likely"
            ):
                self.likely_manual_item_ids.append(item_id)

        self.current_new_count = new_count
        self.current_duplicate_count = duplicate_count
        self.current_likely_manual_count = likely_manual_count
        self.current_possible_manual_count = possible_manual_count

        # Start with every new transaction selected. The user can then remove
        # individual rows or ranges before importing.
        if self.new_item_ids:
            self.tree.selection_set(*self.new_item_ids)
            self.tree.focus(self.new_item_ids[0])
        else:
            self.tree.selection_set()

        self.update_selection_summary()

    def do_import(self):
        statement = self.current_statement()
        target_name = self.target_combo.get()
        target_id = self.app.account_name_to_id.get(target_name)

        if not target_id:
            messagebox.showerror(
                "No account",
                "Choose the Simple Finance account for this bank statement.",
                parent=self,
            )
            return

        if statement["currency"] not in {"GBP", "UKL"}:
            if not messagebox.askyesno(
                "Different currency",
                f'This statement reports currency {statement["currency"]}.\n\n'
                "Simple Finance currently displays account values in pounds.\n"
                "Import it anyway?",
                parent=self,
            ):
                return

        new_transactions, replacements = self.selected_import_actions()

        if not new_transactions and not replacements:
            messagebox.showinfo(
                "Nothing selected",
                "Select at least one New or manual-match transaction.",
                parent=self,
            )
            return

        selected_transactions = new_transactions + [
            replacement["ofx_transaction"]
            for replacement in replacements
        ]

        selected_ids = [
            txn["external_id"] for txn in selected_transactions
        ]
        existing_now = self.app.db.get_existing_external_ids(
            target_id, selected_ids
        )
        if existing_now:
            messagebox.showinfo(
                "Preview has changed",
                "One or more selected OFX transactions have already been "
                "imported since this preview was built.\n\n"
                "The preview will now refresh.",
                parent=self,
            )
            self.refresh_preview()
            return

        payments = sum(
            abs(txn["amount"])
            for txn in selected_transactions
            if txn["amount"] < 0
        )
        deposits = sum(
            txn["amount"]
            for txn in selected_transactions
            if txn["amount"] > 0
        )

        likely_replace_count = sum(
            1 for replacement in replacements
            if replacement["confidence"] == "likely"
        )
        possible_replace_count = sum(
            1 for replacement in replacements
            if replacement["confidence"] == "possible"
        )

        replacement_note = ""
        if replacements:
            replacement_note = (
                f"\n\nManual replacements: {len(replacements)} "
                f"({likely_replace_count} likely, "
                f"{possible_replace_count} possible).\n"
                "Existing Account Transactions are updated in place. "
                "Their categories and reconciliation state are preserved, "
                "while the bank's OFX date/description/FITID are applied."
            )

        if possible_replace_count:
            replacement_note += (
                "\n\nCAUTION: Possible manual matches are less certain. "
                "Check those orange rows carefully."
            )

        if not messagebox.askyesno(
            "Import / replace selected transactions",
            f"Process {len(selected_transactions)} selected transaction(s) into "
            f'"{target_name}"?\n\n'
            f"New imports: {len(new_transactions)}\n"
            f"Replace manual entries: {len(replacements)}\n"
            f"Payments: {money(payments)}\n"
            f"Deposits: {money(deposits)}"
            f"{replacement_note}",
            parent=self,
        ):
            return

        try:
            imported, replaced = (
                self.app.db.import_and_replace_bank_transactions(
                    target_id,
                    new_transactions,
                    replacements,
                    f"OFX:{self.source_path.name}",
                )
            )
        except (ValueError, sqlite3.IntegrityError) as exc:
            messagebox.showerror(
                "Import / replacement failed",
                str(exc),
                parent=self,
            )
            self.refresh_preview()
            return

        self.app.refresh_all()
        self.result = True

        messagebox.showinfo(
            "Import complete",
            f"Imported {imported} new transaction(s).\n"
            f"Replaced {replaced} manual transaction(s) with OFX data.\n\n"
            "Replaced entries keep their existing categories and reconciliation state.",
            parent=self,
        )

        self.destroy()


class SimpleFinanceApp(tk.Tk):
    def __init__(self):
        # className sets the X11/XWayland WM_CLASS so Linux desktops can
        # associate the running window with the Simple Finance .desktop file.
        super().__init__(className="SimpleFinance")
        try:
            self.tk.call("tk", "appname", "SimpleFinance")
        except tk.TclError:
            pass

        self.title(f"{APP_NAME} {APP_VERSION}")
        self._set_application_icon()
        self.geometry("1180x760")
        self.minsize(980, 620)

        self.db = FinanceDB()
        self.load_settings()

        self.account_name_to_id = {}
        self.account_id_to_name = {}
        self.category_name_to_id = {}

        self._configure_styles()
        self._build_ui()

        self.create_automatic_backup()
        created = self.db.process_due_schedules()
        self.refresh_all()

        if created:
            self.after(
                250,
                lambda: messagebox.showinfo(
                    "Scheduled transactions",
                    f"{created} scheduled transaction(s) were added.",
                ),
            )

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._update_banner = None
        self.after(1500, self._check_for_updates)

    def _check_for_updates(self):
        checker = UpdateChecker(GITHUB_REPO, APP_VERSION)
        checker.check_async(lambda release: self.after(0, self._on_update_check_result, release))

    def _on_update_check_result(self, release):
        if release is None:
            return
        self._show_update_banner(release)

    def _show_update_banner(self, release):
        if self._update_banner is not None:
            return
        banner = ttk.Frame(self, padding=(14, 6))
        banner.pack(fill="x", before=self.notebook)
        ttk.Label(
            banner,
            text=(
                f"A new version of {APP_NAME} is available: {release.tag} "
                f"(you have {APP_VERSION})."
            ),
            style="UpdateBanner.TLabel",
        ).pack(side="left")
        ttk.Button(
            banner,
            text="Update",
            style="Update.TButton",
            command=lambda: self._start_update(release),
        ).pack(side="right")
        ttk.Button(banner, text="Dismiss", command=banner.destroy).pack(
            side="right", padx=(0, 8)
        )
        self._update_banner = banner

    def _start_update(self, release):
        asset = pick_asset_for_platform(release.assets)
        if asset is None:
            webbrowser.open(release.html_url)
            return

        self.config(cursor="watch")

        def worker():
            try:
                path = download_asset(asset)
                error = None
            except Exception as exc:
                path = None
                error = exc
            self.after(0, self._finish_update, path, error, release)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_update(self, path, error, release):
        self.config(cursor="")
        if error is not None or path is None:
            messagebox.showerror(
                "Update failed",
                "Could not download the update:\n\n"
                f"{error}\n\nYou can download it manually from:\n{release.html_url}",
                parent=self,
            )
            return

        open_installer(path)
        messagebox.showinfo(
            "Update downloaded",
            f"The {release.tag} installer has been opened. "
            f"{APP_NAME} will now close so you can finish installing it "
            "(the running app would otherwise block replacing it).",
            parent=self,
        )
        self.on_close()

    def _icon_candidates(self):
        return [
            Path(__file__).resolve().with_name("icon.png"),
            paths.data_dir() / "simple-finance.png",
            Path.home()
            / ".local"
            / "share"
            / "icons"
            / "hicolor"
            / "512x512"
            / "apps"
            / "simple-finance.png",
        ]

    def _find_icon_path(self):
        for icon_path in self._icon_candidates():
            if icon_path.exists():
                return icon_path
        return None

    def _set_application_icon(self):
        """
        Set the icon on the live Tk window.

        Search a few locations so the icon works both from the installer and
        when running the downloaded .py file beside simple-finance.png.
        """
        self._icon_path = self._find_icon_path()

        if self._icon_path is None:
            self._window_icon = None
            return

        try:
            self._window_icon = tk.PhotoImage(file=str(self._icon_path))
            self.iconphoto(True, self._window_icon)
        except tk.TclError:
            self._window_icon = None

    def _create_header_icon(self, size=32):
        """
        Create a small in-window icon for the header next to the program name.
        """
        icon_path = getattr(self, "_icon_path", None) or self._find_icon_path()
        if icon_path is None:
            self._header_icon = None
            return None

        try:
            image = tk.PhotoImage(file=str(icon_path))
        except tk.TclError:
            self._header_icon = None
            return None

        width = max(1, int(image.width()))
        factor = max(1, round(width / size))
        if factor > 1:
            image = image.subsample(factor, factor)

        self._header_icon = image
        return image

    def load_settings(self):
        value = self.db.get_setting("date_format", "UK")
        if value not in DATE_FORMATS:
            value = "UK"
        self.date_format_key = value

    def date_format_info(self):
        return DATE_FORMATS.get(self.date_format_key, DATE_FORMATS["UK"])

    def date_format_example(self):
        return self.date_format_info()["example"]

    def format_date(self, value):
        """
        Format a date/date-like ISO string for display using the selected setting.
        Database dates remain YYYY-MM-DD internally.
        """
        if value is None or value == "":
            return ""

        if isinstance(value, datetime):
            d = value.date()
        elif isinstance(value, date):
            d = value
        else:
            d = parse_date(str(value))

        return d.strftime(self.date_format_info()["strftime"])

    def format_datetime(self, value):
        if isinstance(value, datetime):
            dt = value
        else:
            dt = datetime.fromtimestamp(value)
        return dt.strftime(self.date_format_info()["strftime"] + " %H:%M:%S")

    def parse_user_date(self, value):
        """
        Parse a manually entered date using the selected display format.

        ISO YYYY-MM-DD is also accepted as a fallback so older habits/files
        remain convenient after switching to UK display.
        """
        raw = (value or "").strip()
        if not raw:
            raise ValueError("Date is blank.")

        formats = [self.date_format_info()["strftime"]]
        if "%Y-%m-%d" not in formats:
            formats.append("%Y-%m-%d")

        for fmt in formats:
            try:
                return datetime.strptime(raw, fmt).date()
            except ValueError:
                pass

        raise ValueError(
            f"Use {self.date_format_info()['label'].split(' (', 1)[1].rstrip(')')} "
            f"(for example {self.date_format_example()})."
        )

    def _configure_styles(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("Title.TLabel", font=("Sans", 18, "bold"))
        style.configure("Heading.TLabel", font=("Sans", 11, "bold"))
        style.configure("Balance.TLabel", font=("Sans", 12, "bold"))
        style.configure("RegisterBalance.TLabel", font=("Sans", 14, "bold"))
        style.configure("Treeview", rowheight=26)

        style.configure("UpdateBanner.TLabel", foreground="#c62828", font=("Sans", 10, "bold"))
        style.configure(
            "Update.TButton", foreground="white", background="#c62828", font=("Sans", 10, "bold")
        )
        style.map(
            "Update.TButton",
            background=[("active", "#b71c1c"), ("pressed", "#b71c1c")],
            foreground=[("active", "white"), ("pressed", "white")],
        )

    def _build_ui(self):
        header = ttk.Frame(self, padding=(14, 12))
        header.pack(fill="x")

        left_header = ttk.Frame(header)
        left_header.pack(side="left")

        header_icon = self._create_header_icon(size=32)
        if header_icon is not None:
            ttk.Label(left_header, image=header_icon).pack(side="left", padx=(0, 10))

        ttk.Label(left_header, text=APP_NAME, style="Title.TLabel").pack(side="left")
        ttk.Label(
            left_header, text=f"Version {APP_VERSION}", foreground="#666666"
        ).pack(side="left", padx=(10, 0))

        self.total_balance_var = tk.StringVar(value="Total: £0.00")
        ttk.Label(
            header, textvariable=self.total_balance_var, style="Balance.TLabel"
        ).pack(side="right")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.accounts_tab = ttk.Frame(self.notebook, padding=10)
        self.register_tab = ttk.Frame(self.notebook, padding=10)
        self.budget_tab = ttk.Frame(self.notebook, padding=10)
        self.scenario_tab = ttk.Frame(self.notebook, padding=10)
        self.budgetary_tab = ttk.Frame(self.notebook, padding=10)
        self.categories_tab = ttk.Frame(self.notebook, padding=10)
        self.scheduled_tab = ttk.Frame(self.notebook, padding=10)
        self.backup_tab = ttk.Frame(self.notebook, padding=10)
        self.settings_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.accounts_tab, text="Accounts")
        self.notebook.add(self.register_tab, text="Account Transactions")
        self.notebook.add(self.budget_tab, text="6 Month Budget")
        self.notebook.add(self.scenario_tab, text="Scenario Sheet")
        self.notebook.add(self.budgetary_tab, text="Budgetary Transactions")
        self.notebook.add(self.scheduled_tab, text="Scheduled")
        self.notebook.add(self.categories_tab, text="Categories")
        self.notebook.add(self.backup_tab, text="Backup & Restore")
        self.notebook.add(self.settings_tab, text="Settings")

        self._build_accounts_tab()
        self._build_register_tab()
        self._build_budget_tab()
        self._build_scenario_tab()
        self._build_budgetary_tab()
        self._build_categories_tab()
        self._build_scheduled_tab()
        self._build_backup_tab()
        self._build_settings_tab()

    # ==========================================================
    # Settings tab
    # ==========================================================

    def _build_settings_tab(self):
        intro = ttk.Label(
            self.settings_tab,
            text=(
                "Program preferences are stored with your Simple Finance data, "
                "so they are included in backups and restored with the database."
            ),
            wraplength=850,
            justify="left",
        )
        intro.pack(anchor="w", pady=(0, 14))

        date_box = ttk.LabelFrame(
            self.settings_tab, text="Date format", padding=14
        )
        date_box.pack(fill="x", pady=(0, 12))

        ttk.Label(
            date_box,
            text="Choose how dates are displayed and entered:",
        ).grid(row=0, column=0, sticky="w")

        self.settings_date_format = ttk.Combobox(
            date_box,
            state="readonly",
            width=28,
            values=[DATE_FORMATS[key]["label"] for key in ("UK", "ISO", "US")],
        )
        self.settings_date_format.grid(
            row=1, column=0, sticky="w", pady=(6, 8)
        )

        current_label = DATE_FORMATS[self.date_format_key]["label"]
        self.settings_date_format.set(current_label)

        self.settings_date_example_var = tk.StringVar()
        ttk.Label(
            date_box,
            textvariable=self.settings_date_example_var,
        ).grid(row=2, column=0, sticky="w", pady=(0, 10))

        self.settings_date_format.bind(
            "<<ComboboxSelected>>",
            lambda event: self.update_settings_date_example(),
        )

        ttk.Button(
            date_box,
            text="Save Settings",
            command=self.save_settings,
        ).grid(row=3, column=0, sticky="w")

        future_box = ttk.LabelFrame(
            self.settings_tab, text="Future settings", padding=14
        )
        future_box.pack(fill="x")

        ttk.Label(
            future_box,
            text=(
                "This tab is now the home for program-wide preferences. "
                "We can add further options here as the program grows."
            ),
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        self.update_settings_date_example()

    def selected_date_format_key(self):
        label = self.settings_date_format.get()
        for key, info in DATE_FORMATS.items():
            if info["label"] == label:
                return key
        return "UK"

    def update_settings_date_example(self):
        if not hasattr(self, "settings_date_example_var"):
            return
        key = self.selected_date_format_key()
        self.settings_date_example_var.set(
            f"Example: {DATE_FORMATS[key]['example']}"
        )

    def save_settings(self):
        key = self.selected_date_format_key()
        self.db.set_setting("date_format", key)
        self.date_format_key = key
        self.refresh_all()

        messagebox.showinfo(
            "Settings saved",
            f"Date format changed to {DATE_FORMATS[key]['label']}.",
            parent=self,
        )

    # ==========================================================
    # Backup & Restore tab
    # ==========================================================

    def backup_directory(self):
        path = paths.data_dir() / "backups"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def automatic_backup_path(self):
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return self.backup_directory() / f"simple_finance_auto_{stamp}.sfbackup"

    def create_automatic_backup(self):
        """
        Create one startup backup and retain the ten most recent automatic copies.
        Fail quietly enough not to prevent the finance program starting.
        """
        try:
            backup_path = self.automatic_backup_path()
            self.db.backup_to(backup_path)

            backups = sorted(
                self.backup_directory().glob("simple_finance_auto_*.sfbackup"),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )

            for old_backup in backups[10:]:
                try:
                    old_backup.unlink()
                except OSError:
                    pass

            self.last_auto_backup = backup_path
        except (OSError, sqlite3.Error):
            self.last_auto_backup = None

    def _build_backup_tab(self):
        intro = ttk.Label(
            self.backup_tab,
            text=(
                "Backups contain the complete Simple Finance database: accounts, "
                "transactions, OFX import history, categories, scheduled transactions "
                "budgetary transactions and saved scenario sheets."
            ),
            wraplength=900,
            justify="left",
        )
        intro.pack(anchor="w", pady=(0, 14))

        manual_box = ttk.LabelFrame(
            self.backup_tab, text="Manual backup", padding=14
        )
        manual_box.pack(fill="x", pady=(0, 12))

        ttk.Label(
            manual_box,
            text=(
                "Save a complete copy somewhere safe. An external drive or another "
                "computer/cloud-synchronised folder is better protection than keeping "
                "the only backup on the same disk."
            ),
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            manual_box,
            text="Backup Now...",
            command=self.manual_backup,
        ).pack(anchor="w")

        restore_box = ttk.LabelFrame(
            self.backup_tab, text="Restore from backup", padding=14
        )
        restore_box.pack(fill="x", pady=(0, 12))

        ttk.Label(
            restore_box,
            text=(
                "Restore replaces the current Simple Finance database with the chosen "
                "backup. A safety copy of the current database is made automatically first."
            ),
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            restore_box,
            text="Restore Backup...",
            command=self.restore_backup,
        ).pack(anchor="w")

        auto_box = ttk.LabelFrame(
            self.backup_tab, text="Automatic backups", padding=14
        )
        auto_box.pack(fill="x", pady=(0, 12))

        self.backup_status_var = tk.StringVar(value="")
        ttk.Label(
            auto_box,
            textvariable=self.backup_status_var,
            wraplength=850,
            justify="left",
        ).pack(anchor="w")

        ttk.Button(
            auto_box,
            text="Open Backup Folder",
            command=self.open_backup_folder,
        ).pack(anchor="w", pady=(10, 0))

        self.refresh_backup_status()

    def refresh_backup_status(self):
        if not hasattr(self, "backup_status_var"):
            return

        backup_dir = self.backup_directory()
        backups = sorted(
            backup_dir.glob("simple_finance_auto_*.sfbackup"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

        if backups:
            latest = backups[0]
            when = self.format_datetime(
                datetime.fromtimestamp(latest.stat().st_mtime)
            )
            text = (
                f"Automatic backup folder:\n{backup_dir}\n\n"
                f"Latest automatic backup: {latest.name}\n"
                f"Created: {when}\n\n"
                f"Automatic backups retained: {len(backups)} of 10"
            )
        else:
            text = (
                f"Automatic backup folder:\n{backup_dir}\n\n"
                "No automatic backups found yet."
            )

        self.backup_status_var.set(text)

    def manual_backup(self):
        default_name = (
            "simple_finance_backup_"
            + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            + ".sfbackup"
        )

        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Simple Finance backup",
            defaultextension=".sfbackup",
            filetypes=[
                ("Simple Finance Backup", "*.sfbackup"),
                ("SQLite Database", "*.db"),
                ("All files", "*"),
            ],
            initialfile=default_name,
        )
        if not path:
            return

        try:
            self.db.backup_to(path)
        except (OSError, sqlite3.Error) as exc:
            messagebox.showerror(
                "Backup failed",
                f"Could not create the backup:\n\n{exc}",
                parent=self,
            )
            return

        valid, reason = FinanceDB.validate_backup(path)
        if not valid:
            messagebox.showerror(
                "Backup verification failed",
                "The backup file was created but could not be verified:\n\n"
                + reason,
                parent=self,
            )
            return

        messagebox.showinfo(
            "Backup complete",
            f"Simple Finance was backed up successfully to:\n\n{path}",
            parent=self,
        )
        self.refresh_backup_status()

    def restore_backup(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Restore Simple Finance backup",
            filetypes=[
                ("Simple Finance Backup", "*.sfbackup"),
                ("SQLite Database", "*.db"),
                ("All files", "*"),
            ],
        )
        if not path:
            return

        valid, reason = FinanceDB.validate_backup(path)
        if not valid:
            messagebox.showerror(
                "Invalid backup",
                reason,
                parent=self,
            )
            return

        if not messagebox.askyesno(
            "Restore backup",
            "This will replace the current Simple Finance data with the selected "
            "backup.\n\nA safety backup of the current database will be created "
            "automatically first.\n\nContinue?",
            parent=self,
        ):
            return

        current_db_path = Path(self.db.db_path)
        safety_path = (
            self.backup_directory()
            / (
                "simple_finance_pre_restore_"
                + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                + ".sfbackup"
            )
        )

        try:
            self.db.backup_to(safety_path)
        except (OSError, sqlite3.Error) as exc:
            messagebox.showerror(
                "Restore stopped",
                "Could not create the pre-restore safety backup.\n\n"
                f"No data has been changed.\n\n{exc}",
                parent=self,
            )
            return

        try:
            self.db.close()

            shutil.copy2(path, current_db_path)

            # Opening through FinanceDB performs any required schema migration.
            self.db = FinanceDB(current_db_path)
            self.load_settings()
            if hasattr(self, "settings_date_format"):
                self.settings_date_format.set(
                    DATE_FORMATS[self.date_format_key]["label"]
                )
                self.update_settings_date_example()

            # Ensure the restored database is usable before announcing success.
            restored_valid, restored_reason = FinanceDB.validate_backup(
                current_db_path
            )
            if not restored_valid:
                raise RuntimeError(restored_reason)

            self.refresh_all()
            self.refresh_backup_status()

        except Exception as exc:
            # Attempt to roll back to the safety copy.
            try:
                try:
                    self.db.close()
                except Exception:
                    pass
                shutil.copy2(safety_path, current_db_path)
                self.db = FinanceDB(current_db_path)
                self.load_settings()
                if hasattr(self, "settings_date_format"):
                    self.settings_date_format.set(
                        DATE_FORMATS[self.date_format_key]["label"]
                    )
                    self.update_settings_date_example()
                self.refresh_all()
            except Exception:
                pass

            messagebox.showerror(
                "Restore failed",
                "The restore could not be completed. Simple Finance attempted to "
                "put the pre-restore database back in place.\n\n"
                f"Safety backup:\n{safety_path}\n\n"
                f"Error:\n{exc}",
                parent=self,
            )
            return

        messagebox.showinfo(
            "Restore complete",
            "The backup has been restored successfully.\n\n"
            f"Pre-restore safety backup:\n{safety_path}",
            parent=self,
        )

    def open_backup_folder(self):
        folder = self.backup_directory()

        try:
            if sys.platform == "win32":
                os.startfile(str(folder))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as exc:
            messagebox.showinfo(
                "Backup folder",
                f"Automatic backups are stored here:\n\n{folder}\n\n"
                f"Could not open the folder automatically:\n{exc}",
                parent=self,
            )

    # ==========================================================
    # Accounts tab
    # ==========================================================

    def _build_accounts_tab(self):
        form = ttk.LabelFrame(self.accounts_tab, text="Add account", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        self.acc_name = ttk.Entry(form, width=30)
        self.acc_name.grid(row=1, column=0, padx=(0, 10))

        ttk.Label(form, text="Type").grid(row=0, column=1, sticky="w")
        self.acc_type = ttk.Combobox(
            form,
            state="readonly",
            values=["Current", "Savings", "Cash", "Credit Card", "Other"],
            width=18,
        )
        self.acc_type.grid(row=1, column=1, padx=(0, 10))
        self.acc_type.set("Current")

        ttk.Label(form, text="Opening balance").grid(row=0, column=2, sticky="w")
        self.acc_opening = ttk.Entry(form, width=18)
        self.acc_opening.grid(row=1, column=2, padx=(0, 10))
        self.acc_opening.insert(0, "0.00")

        ttk.Button(form, text="Add account", command=self.add_account).grid(
            row=1, column=3, padx=(5, 0)
        )

        columns = ("id", "name", "type", "opening", "balance")
        self.accounts_tree = ttk.Treeview(
            self.accounts_tab, columns=columns, show="headings"
        )
        self.accounts_tree.heading("id", text="ID")
        self.accounts_tree.heading("name", text="Account")
        self.accounts_tree.heading("type", text="Type")
        self.accounts_tree.heading("opening", text="Opening balance")
        self.accounts_tree.heading("balance", text="Current balance")

        self.accounts_tree.column("id", width=0, stretch=False)
        self.accounts_tree.column("name", width=300)
        self.accounts_tree.column("type", width=180)
        self.accounts_tree.column("opening", width=170, anchor="e")
        self.accounts_tree.column("balance", width=190, anchor="e")
        self.accounts_tree.pack(fill="both", expand=True)
        self.accounts_tree.bind("<Double-1>", self.open_selected_account_register)

        bottom = ttk.Frame(self.accounts_tab)
        bottom.pack(fill="x", pady=(8, 0))
        ttk.Button(
            bottom, text="Open account register", command=self.open_selected_account_register
        ).pack(side="left")

        ttk.Button(
            bottom, text="Edit selected account", command=self.edit_account
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            bottom, text="Delete selected account", command=self.delete_account
        ).pack(side="left", padx=(8, 0))

        ttk.Button(bottom, text="Refresh", command=self.refresh_all).pack(side="right")

    def add_account(self):
        name = self.acc_name.get().strip()
        if not name:
            messagebox.showerror("Missing account name", "Please enter an account name.")
            return

        try:
            opening = float(self.acc_opening.get().strip())
        except ValueError:
            messagebox.showerror("Invalid balance", "Opening balance must be a number.")
            return

        try:
            self.db.add_account(name, self.acc_type.get(), opening)
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate account", "An account with that name exists.")
            return

        self.acc_name.delete(0, tk.END)
        self.acc_opening.delete(0, tk.END)
        self.acc_opening.insert(0, "0.00")
        self.refresh_all()

    def edit_account(self):
        selected = self.accounts_tree.selection()
        if not selected:
            messagebox.showinfo(
                "No account selected",
                "Select an account first.",
                parent=self,
            )
            return

        account_id = int(self.accounts_tree.item(selected[0])["values"][0])
        old_name = self.account_id_to_name.get(account_id, "")

        dialog = AccountEditDialog(self, self, account_id)
        self.wait_window(dialog)

        if dialog.result:
            # Refresh account name mappings and balances.
            self.refresh_all()

            # If the edited account was the currently open register,
            # keep that same account selected even if it was renamed.
            updated = self.db.get_account(account_id)
            if updated:
                self.register_account.set(updated["name"])
                self.refresh_register()

    def delete_account(self):
        selected = self.accounts_tree.selection()
        if not selected:
            return

        account_id = int(self.accounts_tree.item(selected[0])["values"][0])

        if not messagebox.askyesno(
            "Delete account", "Delete the selected account?"
        ):
            return

        try:
            self.db.delete_account(account_id)
        except ValueError as exc:
            messagebox.showerror("Cannot delete account", str(exc))
            return

        self.refresh_all()

    def open_selected_account_register(self, event=None):
        selected = self.accounts_tree.selection()
        if not selected:
            return

        account_id = int(self.accounts_tree.item(selected[0])["values"][0])
        account_name = self.account_id_to_name.get(account_id)
        if account_name:
            self.register_account.set(account_name)
            self.refresh_register()
            self.notebook.select(self.register_tab)

    # ==========================================================
    # Register tab
    # ==========================================================

    def _build_register_tab(self):
        top = ttk.Frame(self.register_tab)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(top, text="Account:", style="Heading.TLabel").pack(side="left")
        self.register_account = ttk.Combobox(top, state="readonly", width=28)
        self.register_account.pack(side="left", padx=(8, 12))
        self.register_account.bind("<<ComboboxSelected>>", lambda e: self.refresh_register())

        ttk.Button(top, text="New transaction", command=self.new_register_transaction).pack(
            side="left"
        )
        ttk.Button(top, text="Transfer", command=self.new_transfer).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(top, text="Edit selected", command=self.edit_register_transaction).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(
            top, text="Select All", command=self.select_all_register_transactions
        ).pack(side="left", padx=(8, 0))
        ttk.Button(top, text="Delete selected", command=self.delete_register_transaction).pack(
            side="left", padx=(8, 0)
        )

        self.register_balance_var = tk.StringVar(value="Balance: £0.00")
        ttk.Label(
            top, textvariable=self.register_balance_var, style="RegisterBalance.TLabel"
        ).pack(side="right")

        hint = ttk.Label(
            self.register_tab,
            text=(
                "Double-click a transaction to edit it. Transfers are shown as linked entries "
                "in both accounts. A ✓ in Reconciled means the transaction has been confirmed "
                "against a completed bank-statement reconciliation."
            ),
        )
        hint.pack(anchor="w", pady=(0, 8))

        columns = (
            "id",
            "date",
            "description",
            "category",
            "memo",
            "payment",
            "deposit",
            "reconciled",
            "balance",
        )
        self.register_tree = ttk.Treeview(
            self.register_tab, columns=columns, show="headings"
        )

        headings = {
            "id": "ID",
            "date": "Date",
            "description": "Description",
            "category": "Category",
            "memo": "Memo",
            "payment": "Payment",
            "deposit": "Deposit",
            "reconciled": "Reconciled ✓",
            "balance": "Balance",
        }
        widths = {
            "id": 0,
            "date": 100,
            "description": 220,
            "category": 170,
            "memo": 250,
            "payment": 115,
            "deposit": 115,
            "reconciled": 90,
            "balance": 125,
        }

        for col in columns:
            self.register_tree.heading(col, text=headings[col])
            self.register_tree.column(
                col,
                width=widths[col],
                stretch=False if col == "id" else True,
                anchor="e" if col in ("payment", "deposit", "balance") else (
                    "center" if col == "reconciled" else "w"
                ),
            )

        self.register_tree.column("id", width=0, stretch=False)
        self.register_tree.pack(fill="both", expand=True)
        self.register_tree.bind(
            "<Double-1>",
            self.on_register_transaction_double_click,
        )
        self.register_tree.bind("<Control-a>", self.select_all_register_transactions)
        self.register_tree.bind("<Control-A>", self.select_all_register_transactions)

        bottom = ttk.Frame(self.register_tab)
        bottom.pack(fill="x", pady=(8, 0))

        ttk.Button(
            bottom,
            text="Import OFX/QFX...",
            command=self.import_bank_statement,
        ).pack(side="left")

        ttk.Button(
            bottom,
            text="Reconcile PDF Statement...",
            command=self.reconcile_pdf_statement,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(bottom, text="Refresh", command=self.refresh_register).pack(side="right")

    def current_register_account_id(self):
        return self.account_name_to_id.get(self.register_account.get())

    def import_bank_statement(self):
        if not self.account_name_to_id:
            messagebox.showerror(
                "No accounts",
                "Create a Simple Finance account before importing a bank statement.",
                parent=self,
            )
            return

        path = filedialog.askopenfilename(
            parent=self,
            title="Import OFX/QFX bank statement",
            filetypes=[
                ("OFX/QFX bank statements", "*.ofx *.qfx"),
                ("OFX files", "*.ofx"),
                ("QFX files", "*.qfx"),
                ("All files", "*"),
            ],
        )
        if not path:
            return

        try:
            statements = parse_ofx_file(path)
        except (OSError, ValueError) as exc:
            messagebox.showerror(
                "Could not import statement",
                str(exc),
                parent=self,
            )
            return

        dialog = BankStatementImportDialog(
            self, self, statements, path
        )
        self.wait_window(dialog)

    def reconcile_pdf_statement(self):
        if not self.account_name_to_id:
            messagebox.showerror(
                "No accounts",
                "Create a Simple Finance account before reconciling a statement.",
                parent=self,
            )
            return

        path = filedialog.askopenfilename(
            parent=self,
            title="Reconcile PDF bank statement",
            filetypes=[("PDF bank statements", "*.pdf"), ("All files", "*")],
        )
        if not path:
            return

        try:
            extracted_text = extract_pdf_statement_text(path)
            parsed = parse_pdf_statement_text(extracted_text)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Could not read PDF statement", str(exc), parent=self)
            return

        if not parsed["transactions"]:
            if not messagebox.askyesno(
                "No transactions detected",
                "No transaction rows were detected automatically.\n\n"
                "Open the reconciliation screen anyway and enter the statement rows manually?",
                parent=self,
            ):
                return

        dialog = PDFReconciliationDialog(
            self,
            self,
            path,
            parsed,
            preset_account=self.register_account.get() or None,
        )
        self.wait_window(dialog)

    def save_transaction_csv_template(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save transaction CSV template",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*")],
            initialfile="transactions_template.csv",
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(
                    ["Date", "Account", "Category", "Payee", "Payment", "Deposit", "Memo"]
                )
                writer.writerow(
                    [
                        "2026-09-01",
                        "Current Account",
                        "Groceries",
                        "Supermarket",
                        "42.50",
                        "",
                        "Weekly shopping",
                    ]
                )
                writer.writerow(
                    [
                        "2026-09-02",
                        "Current Account",
                        "Salary",
                        "Employer",
                        "",
                        "2500.00",
                        "Monthly salary",
                    ]
                )
        except OSError as exc:
            messagebox.showerror("Could not save CSV", str(exc), parent=self)
            return

        messagebox.showinfo(
            "CSV template saved",
            "Template saved successfully.\n\n"
            "Enter payments as positive values in the Payment column and "
            "deposits as positive values in the Deposit column.\n\n"
            "Replace the example account/category names with names that exist in Simple Finance.",
            parent=self,
        )

    @staticmethod
    def _parse_import_date(value):
        """
        Accept the program's normal ISO format plus common UK spreadsheet formats.
        """
        value = (value or "").strip()
        formats = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                pass
        raise ValueError(
            "date must be YYYY-MM-DD, DD/MM/YYYY or DD-MM-YYYY"
        )

    @staticmethod
    def _parse_csv_money(value):
        """
        Parse ordinary CSV money values.

        Accepts commas, £ signs and surrounding whitespace.
        Parentheses are treated as a negative value, e.g. (£42.50).
        """
        raw = (value or "").strip()
        if not raw:
            return None

        negative_parentheses = raw.startswith("(") and raw.endswith(")")
        if negative_parentheses:
            raw = raw[1:-1].strip()

        raw = (
            raw.replace("£", "")
            .replace(",", "")
            .replace(" ", "")
            .strip()
        )

        number = float(raw)
        if negative_parentheses:
            number = -abs(number)
        return number

    def import_transactions_csv(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Import transactions from CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*")],
        )
        if not path:
            return

        account_lookup = {
            self._normalise_lookup_name(row["name"]): (row["id"], row["name"])
            for row in self.db.get_account_choices()
        }
        category_lookup = {
            self._normalise_lookup_name(row["name"]): (row["id"], row["name"])
            for row in self.db.get_category_choices()
        }

        errors = []
        pending = []

        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)

                if not reader.fieldnames:
                    messagebox.showerror(
                        "Invalid CSV",
                        "The CSV does not contain a header row.",
                        parent=self,
                    )
                    return

                fields = {
                    self._normalise_csv_header(field): field
                    for field in reader.fieldnames
                    if field is not None
                }

                # Basic required columns.
                required = {
                    "date": "Date",
                    "account": "Account",
                    "category": "Category",
                    "payee": "Payee",
                }
                missing = [
                    label for key, label in required.items() if key not in fields
                ]

                # Money can be supplied as either:
                #   Payment + Deposit
                # or
                #   Amount
                has_amount = "amount" in fields
                has_payment = "payment" in fields
                has_deposit = "deposit" in fields
                has_payment_deposit = has_payment and has_deposit

                if missing or not (has_amount or has_payment_deposit):
                    details = []
                    if missing:
                        details.append(
                            "Missing required column(s): " + ", ".join(missing)
                        )
                    if not (has_amount or has_payment_deposit):
                        details.append(
                            'Include either an "Amount" column, or both '
                            '"Payment" and "Deposit" columns.'
                        )

                    messagebox.showerror(
                        "Invalid CSV",
                        "\n".join(details),
                        parent=self,
                    )
                    return

                date_col = fields["date"]
                account_col = fields["account"]
                category_col = fields["category"]
                payee_col = fields["payee"]
                memo_col = fields.get("memo")
                amount_col = fields.get("amount")
                payment_col = fields.get("payment")
                deposit_col = fields.get("deposit")

                for line_no, raw in enumerate(reader, start=2):
                    # Ignore completely blank lines.
                    if not any((value or "").strip() for value in raw.values()):
                        continue

                    date_text = (raw.get(date_col) or "").strip()
                    account_text = (raw.get(account_col) or "").strip()
                    category_text = (raw.get(category_col) or "").strip()
                    payee = (raw.get(payee_col) or "").strip()
                    memo = (raw.get(memo_col) or "").strip() if memo_col else ""

                    row_errors = []

                    try:
                        txn_date = self._parse_import_date(date_text).isoformat()
                    except ValueError as exc:
                        row_errors.append(str(exc))
                        txn_date = None

                    account_match = account_lookup.get(
                        self._normalise_lookup_name(account_text)
                    )
                    if not account_match:
                        row_errors.append(f'unknown account "{account_text}"')

                    # Blank category is allowed. A non-blank unknown category is not.
                    category_match = None
                    if category_text:
                        category_match = category_lookup.get(
                            self._normalise_lookup_name(category_text)
                        )
                        if not category_match:
                            row_errors.append(f'unknown category "{category_text}"')

                    if not payee:
                        row_errors.append("Payee is blank")

                    amount = None

                    # If Amount is present and non-blank, it takes precedence.
                    amount_text = (
                        (raw.get(amount_col) or "").strip()
                        if amount_col
                        else ""
                    )

                    if amount_text:
                        try:
                            amount = self._parse_csv_money(amount_text)
                        except ValueError:
                            row_errors.append(f'invalid amount "{amount_text}"')
                    elif has_payment_deposit:
                        payment_text = (raw.get(payment_col) or "").strip()
                        deposit_text = (raw.get(deposit_col) or "").strip()

                        try:
                            payment = self._parse_csv_money(payment_text)
                        except ValueError:
                            payment = None
                            row_errors.append(
                                f'invalid payment "{payment_text}"'
                            )

                        try:
                            deposit = self._parse_csv_money(deposit_text)
                        except ValueError:
                            deposit = None
                            row_errors.append(
                                f'invalid deposit "{deposit_text}"'
                            )

                        payment_present = payment is not None and abs(payment) > 0
                        deposit_present = deposit is not None and abs(deposit) > 0

                        if payment_present and deposit_present:
                            row_errors.append(
                                "enter either Payment or Deposit, not both"
                            )
                        elif payment_present:
                            amount = -abs(payment)
                        elif deposit_present:
                            amount = abs(deposit)
                        else:
                            row_errors.append(
                                "Payment and Deposit are both blank/zero"
                            )
                    else:
                        row_errors.append("Amount is blank")

                    if amount is not None and amount == 0:
                        row_errors.append("amount cannot be zero")

                    if row_errors:
                        errors.append(
                            f"Row {line_no}: " + "; ".join(row_errors)
                        )
                        continue

                    pending.append(
                        {
                            "txn_date": txn_date,
                            "account_id": account_match[0],
                            "category_id": (
                                category_match[0] if category_match else None
                            ),
                            "payee": payee,
                            "memo": memo,
                            "amount": amount,
                        }
                    )

        except (OSError, csv.Error) as exc:
            messagebox.showerror("Could not read CSV", str(exc), parent=self)
            return

        if errors:
            shown = errors[:15]
            extra = len(errors) - len(shown)
            details = "\n".join(shown)
            if extra:
                details += f"\n\n...and {extra} more error(s)."

            messagebox.showerror(
                "CSV import stopped",
                "Nothing was imported because the CSV contains errors:\n\n"
                + details,
                parent=self,
            )
            return

        if not pending:
            messagebox.showinfo(
                "Nothing to import",
                "No transactions were found in the CSV.",
                parent=self,
            )
            return

        total_in = sum(t["amount"] for t in pending if t["amount"] > 0)
        total_out = -sum(t["amount"] for t in pending if t["amount"] < 0)

        if not messagebox.askyesno(
            "Import transactions",
            f"Import {len(pending)} transaction(s)?\n\n"
            f"Payments: {money(total_out)}\n"
            f"Deposits: {money(total_in)}\n\n"
            "Note: importing the same CSV twice will create duplicate transactions.",
            parent=self,
        ):
            return

        self.db.add_transactions_bulk(pending)
        self.refresh_all()

        messagebox.showinfo(
            "Import complete",
            f"Imported {len(pending)} transaction(s).",
            parent=self,
        )

    def new_register_transaction(self):
        if not self.account_name_to_id:
            messagebox.showerror("No accounts", "Create an account first.")
            return

        dialog = TransactionDialog(
            self, self, preset_account=self.register_account.get() or None
        )
        self.wait_window(dialog)
        if dialog.result:
            self.refresh_all()

    def _open_register_transaction_editor(self, txn_id):
        row = self.db.get_transaction(txn_id)
        if row is None:
            messagebox.showerror(
                "Transaction not found",
                "That transaction is no longer present in the database.\n\n"
                "Refresh Account Transactions and try again.",
                parent=self,
            )
            self.refresh_register()
            return

        try:
            dialog = TransactionDialog(
                self,
                self,
                txn_id=txn_id,
            )
        except Exception as exc:
            messagebox.showerror(
                "Cannot open transaction",
                "Simple Finance could not open the transaction editor.\n\n"
                f"{exc}",
                parent=self,
            )
            return

        # A transfer dialog may destroy itself immediately after displaying
        # the linked-transfer message.
        try:
            if dialog.winfo_exists():
                self.wait_window(dialog)
        except tk.TclError:
            pass

        if getattr(dialog, "result", False):
            self.refresh_all()

    def on_register_transaction_double_click(self, event):
        # Treeview selection is updated as part of the mouse event sequence.
        # identify_row() guarantees we edit the row actually double-clicked,
        # rather than a previously-selected/stale row.
        item_id = self.register_tree.identify_row(event.y)
        if not item_id:
            return "break"

        values = self.register_tree.item(item_id, "values")
        if not values:
            return "break"

        try:
            txn_id = int(values[0])
        except (TypeError, ValueError, IndexError):
            messagebox.showerror(
                "Cannot edit transaction",
                "Simple Finance could not determine the selected transaction ID.",
                parent=self,
            )
            return "break"

        self.register_tree.selection_set(item_id)
        self.register_tree.focus(item_id)

        # Run after the mouse event finishes so the modal editor cannot consume
        # the tail end of the original double-click event.
        self.after_idle(
            lambda txn_id=txn_id: self._open_register_transaction_editor(
                txn_id
            )
        )
        return "break"

    def edit_register_transaction(self):
        selected = self.register_tree.selection()
        if not selected:
            return

        values = self.register_tree.item(selected[0], "values")
        if not values:
            return

        try:
            txn_id = int(values[0])
        except (TypeError, ValueError, IndexError):
            messagebox.showerror(
                "Cannot edit transaction",
                "Simple Finance could not determine the selected transaction ID.",
                parent=self,
            )
            return

        self._open_register_transaction_editor(txn_id)

    def select_all_register_transactions(self, event=None):
        items = self.register_tree.get_children()
        if items:
            self.register_tree.selection_set(items)
            self.register_tree.focus(items[0])
        return "break" if event is not None else None

    def delete_register_transaction(self):
        selected = self.register_tree.selection()
        if not selected:
            return

        txn_ids = []
        transfer_groups = set()

        for item_id in selected:
            values = self.register_tree.item(item_id)["values"]
            if not values:
                continue

            txn_id = int(values[0])
            txn_ids.append(txn_id)

            row = self.db.get_transaction(txn_id)
            if row and row["transfer_group"]:
                transfer_groups.add(row["transfer_group"])

        if not txn_ids:
            return

        count = len(txn_ids)

        if count == 1:
            prompt = "Delete the selected transaction?"
        else:
            prompt = f"Delete the {count} selected transactions?"

        if transfer_groups:
            if len(transfer_groups) == 1:
                prompt += (
                    "\n\nOne selected item belongs to a transfer. "
                    "Both sides of that transfer will also be deleted."
                )
            else:
                prompt += (
                    f"\n\nSelected items include {len(transfer_groups)} linked transfers. "
                    "Both sides of each transfer will also be deleted."
                )

        if not messagebox.askyesno("Delete transactions", prompt):
            return

        deleted = self.db.delete_transactions(txn_ids)
        self.refresh_all()

        if deleted > count:
            messagebox.showinfo(
                "Transactions deleted",
                f"Deleted {deleted} transaction entries, including linked transfer entries.",
            )

    def new_transfer(self):
        if len(self.account_name_to_id) < 2:
            messagebox.showerror(
                "Need two accounts", "Create at least two accounts before making a transfer."
            )
            return

        dialog = TransferDialog(
            self, self, preset_from=self.register_account.get() or None
        )
        self.wait_window(dialog)
        if dialog.result:
            self.refresh_all()

    # ==========================================================
    # Scenario Sheet tab
    # ==========================================================

    def _build_scenario_tab(self):
        self.scenario_name_to_id = {}
        self.current_scenario_id = None
        self.current_scenario_name = ""
        self.current_scenario_account_id = None
        self.current_scenario_starting_balance = 0.0
        self.current_scenario_rows = []
        self.scenario_item_to_index = {}
        self.scenario_editor = None

        top = ttk.Frame(self.scenario_tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Button(
            top,
            text="New from 6 Month Budget...",
            command=self.create_scenario_from_projection,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            top,
            text="Save",
            command=self.save_current_scenario,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            top,
            text="Rename...",
            command=self.rename_current_scenario,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            top,
            text="Delete",
            command=self.delete_current_scenario,
        ).pack(side="left")

        ttk.Button(
            top,
            text="Export CSV...",
            command=self.export_current_scenario_csv,
        ).pack(side="right")

        selector_box = ttk.LabelFrame(
            self.scenario_tab,
            text="Saved Scenarios",
            padding=8,
        )
        selector_box.pack(fill="x", pady=(0, 8))

        self._refreshing_scenario_list = False
        self.scenario_list = tk.Listbox(
            selector_box,
            height=3,
            exportselection=False,
        )
        self.scenario_list.pack(fill="x", expand=True)
        self.scenario_list.bind(
            "<<ListboxSelect>>",
            lambda event: self.load_selected_scenario(),
        )

        ttk.Label(
            selector_box,
            text=(
                "Select a saved scenario here. The last scenario you use will "
                "reopen automatically next time Simple Finance starts."
            ),
        ).pack(anchor="w", pady=(6, 0))

        info = ttk.Frame(self.scenario_tab)
        info.pack(fill="x", pady=(0, 8))

        self.scenario_info_var = tk.StringVar(
            value="Create or choose a scenario."
        )
        ttk.Label(
            info,
            textvariable=self.scenario_info_var,
        ).pack(side="left")

        ttk.Label(
            self.scenario_tab,
            text=(
                "This is a snapshot only. Editing this sheet never changes your "
                "real transactions, Scheduled transactions or Budgetary Transactions. "
                "Double-click Date, Description, Income or Spending to edit."
            ),
            wraplength=1050,
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        sheet_box = ttk.Frame(self.scenario_tab)
        sheet_box.pack(fill="both", expand=True)

        columns = (
            "date",
            "description",
            "source",
            "income",
            "spending",
            "balance",
        )

        self.scenario_tree = ttk.Treeview(
            sheet_box,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "date": "Date / Month",
            "description": "Description",
            "source": "Source",
            "income": "Income",
            "spending": "Spending",
            "balance": "Balance",
        }
        widths = {
            "date": 150,
            "description": 330,
            "source": 120,
            "income": 130,
            "spending": 130,
            "balance": 150,
        }

        for col in columns:
            self.scenario_tree.heading(col, text=headings[col])
            self.scenario_tree.column(
                col,
                width=widths[col],
                anchor="e" if col in ("income", "spending", "balance") else "w",
            )

        yscroll = ttk.Scrollbar(
            sheet_box,
            orient="vertical",
            command=self.scenario_tree.yview,
        )
        self.scenario_tree.configure(yscrollcommand=yscroll.set)

        self.scenario_tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        self.scenario_tree.tag_configure(
            "month_header",
            font=("Sans", 10, "bold"),
        )
        self.scenario_tree.tag_configure(
            "negative_balance",
            foreground="red",
        )
        self.scenario_tree.tag_configure(
            "negative_month_header",
            font=("Sans", 10, "bold"),
            foreground="red",
        )
        self.scenario_tree.bind(
            "<Double-1>", self.edit_scenario_cell
        )

        row_buttons = ttk.Frame(self.scenario_tab)
        row_buttons.pack(fill="x", pady=(8, 0))

        ttk.Button(
            row_buttons,
            text="Insert Row Below",
            command=self.insert_scenario_row_below,
        ).pack(side="left")

        ttk.Button(
            row_buttons,
            text="Clear Row",
            command=self.clear_scenario_row,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            row_buttons,
            text="Delete Row",
            command=self.delete_scenario_row,
        ).pack(side="left", padx=(8, 0))

        ttk.Label(
            row_buttons,
            text="Blank rows carry the current balance forward until you enter an amount.",
        ).pack(side="right")

    def refresh_scenario_choices(self):
        if not hasattr(self, "scenario_list"):
            return

        rows = self.db.get_budget_scenarios()
        self.scenario_name_to_id = {
            row["name"]: row["id"] for row in rows
        }
        self.scenario_list_ids = [row["id"] for row in rows]
        self.scenario_list_names = [row["name"] for row in rows]

        target_id = self.current_scenario_id

        if target_id is None:
            saved_id = self.db.get_setting("last_scenario_id", "")
            try:
                target_id = int(saved_id) if saved_id else None
            except (TypeError, ValueError):
                target_id = None

        valid_ids = set(self.scenario_list_ids)
        if target_id not in valid_ids:
            target_id = self.scenario_list_ids[0] if self.scenario_list_ids else None

        self._refreshing_scenario_list = True
        try:
            self.scenario_list.delete(0, tk.END)
            for name in self.scenario_list_names:
                self.scenario_list.insert(tk.END, name)

            if target_id is not None:
                index = self.scenario_list_ids.index(target_id)
                self.scenario_list.selection_set(index)
                self.scenario_list.activate(index)
                self.scenario_list.see(index)
        finally:
            self._refreshing_scenario_list = False

        # The old selector only selected a name; it didn't actually load it
        # during startup. Now the chosen/remembered scenario is loaded.
        if target_id is not None and self.current_scenario_id != target_id:
            self.load_scenario_by_id(target_id)
        elif target_id is None and self.current_scenario_id is None:
            self.render_scenario_sheet()

    def select_scenario_in_list(self, scenario_id):
        if not hasattr(self, "scenario_list"):
            return
        if scenario_id not in getattr(self, "scenario_list_ids", []):
            return

        index = self.scenario_list_ids.index(scenario_id)

        self._refreshing_scenario_list = True
        try:
            self.scenario_list.selection_clear(0, tk.END)
            self.scenario_list.selection_set(index)
            self.scenario_list.activate(index)
            self.scenario_list.see(index)
        finally:
            self._refreshing_scenario_list = False

    def remember_current_scenario(self):
        self.db.set_setting(
            "last_scenario_id",
            "" if self.current_scenario_id is None else str(self.current_scenario_id),
        )

    def load_scenario_by_id(self, scenario_id):
        row = self.db.get_budget_scenario(scenario_id)
        if not row:
            return False

        self.current_scenario_id = row["id"]
        self.current_scenario_name = row["name"]
        self.current_scenario_account_id = row["account_id"]
        self.current_scenario_starting_balance = float(row["starting_balance"])
        self.current_scenario_rows = row["rows"]

        self.remember_current_scenario()
        self.select_scenario_in_list(self.current_scenario_id)
        self.render_scenario_sheet()
        return True

    def load_selected_scenario(self):
        if getattr(self, "_refreshing_scenario_list", False):
            return

        selected = self.scenario_list.curselection()
        if not selected:
            return

        index = selected[0]
        if index >= len(self.scenario_list_ids):
            return

        self.load_scenario_by_id(self.scenario_list_ids[index])

    def make_scenario_rows_from_projection(self):
        """
        Copy the currently displayed six-month projection into a flat,
        spreadsheet-like set of rows. Eight blank rows are added to every month.
        """
        self.refresh_budget_projection()

        account_id = self.current_budget_account_id()
        if not account_id:
            raise ValueError("Choose an account on the 6 Month Budget tab first.")

        account = self.db.get_account(account_id)
        if not account:
            raise ValueError("The selected account could not be found.")

        rows = []

        for item_id in self.budget_summary_tree.get_children():
            data = self.projection_month_data.get(item_id)
            if not data:
                continue

            # Recover the month from the first detailed row when possible,
            # otherwise parse the English month label.
            month_date = None
            if data["rows"]:
                month_date = data["rows"][0]["date"].replace(day=1)
            else:
                try:
                    month_date = datetime.strptime(
                        data["label"], "%B %Y"
                    ).date().replace(day=1)
                except ValueError:
                    month_date = date.today().replace(day=1)

            month_key = month_date.strftime("%Y-%m")

            rows.append(
                {
                    "type": "month",
                    "month": month_key,
                    "label": data["label"],
                }
            )

            for entry in data["rows"]:
                amount = float(entry["amount"])
                rows.append(
                    {
                        "type": "entry",
                        "month": month_key,
                        "date": entry["date"].isoformat(),
                        "description": entry["description"],
                        "source": entry["source"],
                        "income": amount if amount > 0 else 0.0,
                        "spending": abs(amount) if amount < 0 else 0.0,
                    }
                )

            # Spreadsheet-style spare lines for scenario changes.
            for _ in range(8):
                rows.append(
                    {
                        "type": "entry",
                        "month": month_key,
                        "date": "",
                        "description": "",
                        "source": "",
                        "income": 0.0,
                        "spending": 0.0,
                    }
                )

        return account_id, float(account["balance"]), rows

    def create_scenario_from_projection(self):
        try:
            account_id, starting_balance, rows = (
                self.make_scenario_rows_from_projection()
            )
        except ValueError as exc:
            messagebox.showerror(
                "Cannot create scenario",
                str(exc),
                parent=self,
            )
            return

        name = simpledialog.askstring(
            "New budget scenario",
            "Give this scenario a name:",
            initialvalue="Budget Scenario",
            parent=self,
        )
        if name is None:
            return

        name = name.strip()
        if not name:
            messagebox.showerror(
                "Missing name",
                "Enter a name for the scenario.",
                parent=self,
            )
            return

        try:
            scenario_id = self.db.create_budget_scenario(
                name,
                account_id,
                starting_balance,
                rows,
            )
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate scenario name",
                "A scenario with that name already exists.",
                parent=self,
            )
            return

        self.current_scenario_id = scenario_id
        self.current_scenario_name = name
        self.current_scenario_account_id = account_id
        self.current_scenario_starting_balance = starting_balance
        self.current_scenario_rows = rows

        self.remember_current_scenario()
        self.refresh_scenario_choices()
        self.select_scenario_in_list(scenario_id)
        self.render_scenario_sheet()
        self.notebook.select(self.scenario_tab)

    def save_current_scenario(self, silent=False):
        if not self.current_scenario_id:
            if not silent:
                messagebox.showinfo(
                    "No scenario",
                    "Create or choose a scenario first.",
                    parent=self,
                )
            return

        try:
            self.db.update_budget_scenario(
                self.current_scenario_id,
                self.current_scenario_name,
                self.current_scenario_account_id,
                self.current_scenario_starting_balance,
                self.current_scenario_rows,
            )
        except sqlite3.IntegrityError as exc:
            if not silent:
                messagebox.showerror(
                    "Could not save scenario",
                    str(exc),
                    parent=self,
                )
            return

        self.remember_current_scenario()

        if not silent:
            messagebox.showinfo(
                "Scenario saved",
                f'"{self.current_scenario_name}" has been saved.',
                parent=self,
            )

    def rename_current_scenario(self):
        if not self.current_scenario_id:
            return

        new_name = simpledialog.askstring(
            "Rename scenario",
            "Scenario name:",
            initialvalue=self.current_scenario_name,
            parent=self,
        )
        if new_name is None:
            return

        new_name = new_name.strip()
        if not new_name:
            return

        old_name = self.current_scenario_name
        self.current_scenario_name = new_name

        try:
            self.db.update_budget_scenario(
                self.current_scenario_id,
                self.current_scenario_name,
                self.current_scenario_account_id,
                self.current_scenario_starting_balance,
                self.current_scenario_rows,
            )
        except sqlite3.IntegrityError:
            self.current_scenario_name = old_name
            messagebox.showerror(
                "Duplicate scenario name",
                "A scenario with that name already exists.",
                parent=self,
            )
            return

        self.remember_current_scenario()
        self.refresh_scenario_choices()
        self.select_scenario_in_list(self.current_scenario_id)
        self.render_scenario_sheet()

    def delete_current_scenario(self):
        if not self.current_scenario_id:
            return

        if not messagebox.askyesno(
            "Delete scenario",
            f'Delete the saved scenario "{self.current_scenario_name}"?\n\n'
            "This does not affect the real six-month budget or account data.",
            parent=self,
        ):
            return

        self.db.delete_budget_scenario(self.current_scenario_id)

        self.current_scenario_id = None
        self.current_scenario_name = ""
        self.current_scenario_account_id = None
        self.current_scenario_starting_balance = 0.0
        self.current_scenario_rows = []

        self.db.set_setting("last_scenario_id", "")
        self.refresh_scenario_choices()

        if self.scenario_list_ids:
            self.load_scenario_by_id(self.scenario_list_ids[0])
        else:
            self.render_scenario_sheet()

    def calculate_scenario_display_rows(self):
        """
        Return (row, running_balance) for every row in sheet order.
        Month headers and blank rows both display the carried balance.
        """
        running = float(self.current_scenario_starting_balance)
        calculated = []

        for row in self.current_scenario_rows:
            if row.get("type") == "month":
                calculated.append((row, running))
                continue

            income = float(row.get("income") or 0.0)
            spending = float(row.get("spending") or 0.0)
            running += income - spending
            calculated.append((row, running))

        return calculated

    def render_scenario_sheet(self, select_index=None):
        if not hasattr(self, "scenario_tree"):
            return

        if self.scenario_editor is not None:
            try:
                self.scenario_editor.destroy()
            except tk.TclError:
                pass
            self.scenario_editor = None

        for item in self.scenario_tree.get_children():
            self.scenario_tree.delete(item)

        self.scenario_item_to_index = {}

        if not self.current_scenario_id:
            self.scenario_info_var.set(
                "Create a scenario from the 6 Month Budget to begin."
            )
            return

        account_name = self.account_id_to_name.get(
            self.current_scenario_account_id, "Unknown account"
        )
        self.scenario_info_var.set(
            f'{self.current_scenario_name}    |    Account: {account_name}    |    '
            f'Starting balance: {money(self.current_scenario_starting_balance)}'
        )

        selected_item = None

        for index, (row, balance) in enumerate(
            self.calculate_scenario_display_rows()
        ):
            if row.get("type") == "month":
                values = (
                    row.get("label", ""),
                    "",
                    "",
                    "",
                    "",
                    money(balance),
                )
                month_tags = (
                    ("negative_month_header",)
                    if balance < 0
                    else ("month_header",)
                )
                item = self.scenario_tree.insert(
                    "",
                    "end",
                    values=values,
                    tags=month_tags,
                )
            else:
                date_text = ""
                if row.get("date"):
                    try:
                        date_text = self.format_date(row["date"])
                    except ValueError:
                        date_text = row["date"]

                income = float(row.get("income") or 0.0)
                spending = float(row.get("spending") or 0.0)

                values = (
                    date_text,
                    row.get("description", ""),
                    row.get("source", ""),
                    money(income) if income else "",
                    money(spending) if spending else "",
                    money(balance),
                )
                row_tags = ("negative_balance",) if balance < 0 else ()
                item = self.scenario_tree.insert(
                    "",
                    "end",
                    values=values,
                    tags=row_tags,
                )

            self.scenario_item_to_index[item] = index
            if select_index == index:
                selected_item = item

        if selected_item:
            self.scenario_tree.selection_set(selected_item)
            self.scenario_tree.focus(selected_item)
            self.scenario_tree.see(selected_item)

    def scenario_selected_index(self):
        selected = self.scenario_tree.selection()
        if not selected:
            return None
        return self.scenario_item_to_index.get(selected[0])

    def edit_scenario_cell(self, event):
        item = self.scenario_tree.identify_row(event.y)
        column_id = self.scenario_tree.identify_column(event.x)

        if not item or not column_id:
            return

        index = self.scenario_item_to_index.get(item)
        if index is None:
            return

        row = self.current_scenario_rows[index]
        if row.get("type") == "month":
            return

        column_number = int(column_id[1:]) - 1
        editable = {
            0: "date",
            1: "description",
            3: "income",
            4: "spending",
        }
        field = editable.get(column_number)
        if not field:
            return

        bbox = self.scenario_tree.bbox(item, column_id)
        if not bbox:
            return

        x, y, width, height = bbox

        if self.scenario_editor is not None:
            try:
                self.scenario_editor.destroy()
            except tk.TclError:
                pass

        editor = ttk.Entry(self.scenario_tree)
        self.scenario_editor = editor

        if field == "date":
            value = ""
            if row.get("date"):
                try:
                    value = self.format_date(row["date"])
                except ValueError:
                    value = row["date"]
        elif field in ("income", "spending"):
            amount = float(row.get(field) or 0.0)
            value = f"{amount:.2f}" if amount else ""
        else:
            value = row.get(field, "")

        editor.insert(0, value)
        editor.select_range(0, tk.END)
        editor.place(x=x, y=y, width=width, height=height)
        editor.focus_set()

        def commit(_event=None):
            if self.scenario_editor is not editor:
                return

            new_value = editor.get().strip()

            try:
                if field == "date":
                    if new_value:
                        parsed = self.parse_user_date(new_value)
                        expected_month = row.get("month", "")
                        if parsed.strftime("%Y-%m") != expected_month:
                            raise ValueError(
                                "The date must stay within this month section."
                            )
                        row["date"] = parsed.isoformat()
                    else:
                        row["date"] = ""

                elif field == "description":
                    row["description"] = new_value

                elif field in ("income", "spending"):
                    if new_value:
                        cleaned = (
                            new_value.replace("£", "")
                            .replace(",", "")
                            .strip()
                        )
                        amount = float(cleaned)
                        if amount < 0:
                            amount = abs(amount)
                    else:
                        amount = 0.0

                    row[field] = amount

                    # A scenario row acts like a normal transaction line:
                    # it is either income or spending, not both.
                    if amount:
                        other = "spending" if field == "income" else "income"
                        row[other] = 0.0

                # Any change to a copied projection row makes it a scenario override.
                if (
                    row.get("date")
                    or row.get("description")
                    or float(row.get("income") or 0)
                    or float(row.get("spending") or 0)
                ):
                    if row.get("source") not in ("Scenario", ""):
                        row["source"] = "Scenario"
                    elif not row.get("source"):
                        row["source"] = "Scenario"
                else:
                    row["source"] = ""

            except (ValueError, TypeError) as exc:
                messagebox.showerror(
                    "Invalid scenario value",
                    str(exc),
                    parent=self,
                )
                editor.focus_set()
                return

            editor.destroy()
            self.scenario_editor = None
            self.save_current_scenario(silent=True)
            self.render_scenario_sheet(select_index=index)

        def cancel(_event=None):
            if self.scenario_editor is editor:
                editor.destroy()
                self.scenario_editor = None

        editor.bind("<Return>", commit)
        editor.bind("<FocusOut>", commit)
        editor.bind("<Escape>", cancel)

    def insert_scenario_row_below(self):
        if not self.current_scenario_id:
            return

        index = self.scenario_selected_index()
        if index is None:
            return

        selected_row = self.current_scenario_rows[index]
        month_key = selected_row.get("month")
        if not month_key:
            return

        new_row = {
            "type": "entry",
            "month": month_key,
            "date": "",
            "description": "",
            "source": "",
            "income": 0.0,
            "spending": 0.0,
        }

        self.current_scenario_rows.insert(index + 1, new_row)
        self.save_current_scenario(silent=True)
        self.render_scenario_sheet(select_index=index + 1)

    def clear_scenario_row(self):
        index = self.scenario_selected_index()
        if index is None:
            return

        row = self.current_scenario_rows[index]
        if row.get("type") == "month":
            return

        row.update(
            {
                "date": "",
                "description": "",
                "source": "",
                "income": 0.0,
                "spending": 0.0,
            }
        )
        self.save_current_scenario(silent=True)
        self.render_scenario_sheet(select_index=index)

    def delete_scenario_row(self):
        index = self.scenario_selected_index()
        if index is None:
            return

        row = self.current_scenario_rows[index]
        if row.get("type") == "month":
            return

        del self.current_scenario_rows[index]
        self.save_current_scenario(silent=True)
        self.render_scenario_sheet(
            select_index=min(index, len(self.current_scenario_rows) - 1)
        )

    def export_current_scenario_csv(self):
        if not self.current_scenario_id:
            messagebox.showinfo(
                "No scenario",
                "Create or choose a scenario first.",
                parent=self,
            )
            return

        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            self.current_scenario_name,
        ).strip("_") or "scenario"

        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export scenario for LibreOffice Calc",
            defaultextension=".csv",
            filetypes=[
                ("CSV spreadsheet", "*.csv"),
                ("All files", "*"),
            ],
            initialfile=f"{safe_name}.csv",
        )
        if not path:
            return

        calculated = self.calculate_scenario_display_rows()

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(
                    [
                        "Date / Month",
                        "Description",
                        "Source",
                        "Income",
                        "Spending",
                        "Balance",
                    ]
                )

                for row, balance in calculated:
                    if row.get("type") == "month":
                        writer.writerow(
                            [
                                row.get("label", ""),
                                "",
                                "",
                                "",
                                "",
                                f"{balance:.2f}",
                            ]
                        )
                        continue

                    date_text = ""
                    if row.get("date"):
                        date_text = self.format_date(row["date"])

                    income = float(row.get("income") or 0.0)
                    spending = float(row.get("spending") or 0.0)

                    writer.writerow(
                        [
                            date_text,
                            row.get("description", ""),
                            row.get("source", ""),
                            f"{income:.2f}" if income else "",
                            f"{spending:.2f}" if spending else "",
                            f"{balance:.2f}",
                        ]
                    )

        except OSError as exc:
            messagebox.showerror(
                "Export failed",
                f"Could not write the CSV file:\n\n{exc}",
                parent=self,
            )
            return

        messagebox.showinfo(
            "Scenario exported",
            "The scenario has been exported successfully.\n\n"
            "LibreOffice Calc can open the CSV directly.",
            parent=self,
        )

    def _tree_database_id_from_double_click(self, tree, event):
        item_id = tree.identify_row(event.y)
        if not item_id:
            return None

        values = tree.item(item_id, "values")
        if not values:
            return None

        try:
            database_id = int(values[0])
        except (TypeError, ValueError, IndexError):
            return None

        tree.selection_set(item_id)
        tree.focus(item_id)
        return database_id

    # ==========================================================
    # Budgetary Transactions tab
    # ==========================================================

    def _build_budgetary_tab(self):
        intro = ttk.Label(
            self.budgetary_tab,
            text=(
                "Budgetary Transactions are forecast-only. They are included in the "
                "6 Month Budget but are never posted into the real Account Register."
            ),
        )
        intro.pack(anchor="w", pady=(0, 10))

        top = ttk.Frame(self.budgetary_tab)
        top.pack(fill="x", pady=(0, 10))

        ttk.Button(
            top,
            text="Add Budgetary Transaction",
            command=self.add_budgetary_transaction,
        ).pack(side="left")

        ttk.Button(
            top,
            text="Edit selected",
            command=self.edit_budgetary_transaction,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            top,
            text="Delete selected",
            command=self.delete_budgetary_transaction,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            top,
            text="Refresh",
            command=self.refresh_all,
        ).pack(side="right")

        columns = (
            "id",
            "name",
            "account",
            "category",
            "payee",
            "amount",
            "frequency",
            "next_date",
            "end_date",
        )
        self.budgetary_tree = ttk.Treeview(
            self.budgetary_tab,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "id": "ID",
            "name": "Name",
            "account": "Account",
            "category": "Category",
            "payee": "Payee / Description",
            "amount": "Amount",
            "frequency": "Frequency",
            "next_date": "Next Date",
            "end_date": "End Date",
        }
        widths = {
            "id": 0,
            "name": 180,
            "account": 160,
            "category": 150,
            "payee": 210,
            "amount": 110,
            "frequency": 100,
            "next_date": 110,
            "end_date": 110,
        }

        for col in columns:
            self.budgetary_tree.heading(col, text=headings[col])
            self.budgetary_tree.column(
                col,
                width=widths[col],
                stretch=False if col == "id" else True,
                anchor="e" if col == "amount" else "w",
            )

        self.budgetary_tree.column("id", width=0, stretch=False)
        self.budgetary_tree.pack(fill="both", expand=True)
        self.budgetary_tree.bind(
            "<Double-1>", self.on_budgetary_transaction_double_click
        )

    def add_budgetary_transaction(self):
        if not self.account_name_to_id:
            messagebox.showerror("No accounts", "Create an account first.", parent=self)
            return

        preset = self.budget_account.get() if hasattr(self, "budget_account") else None
        dialog = BudgetItemDialog(self, self, preset_account=preset)
        self.wait_window(dialog)
        if dialog.result:
            self.refresh_all()

    def _open_budgetary_transaction_editor(self, item_id):
        try:
            dialog = BudgetItemDialog(
                self, self, item_id=item_id
            )
        except Exception as exc:
            messagebox.showerror(
                "Cannot edit budgetary transaction",
                str(exc),
                parent=self,
            )
            return

        self.wait_window(dialog)
        if getattr(dialog, "result", False):
            self.refresh_all()

    def on_budgetary_transaction_double_click(self, event):
        item_id = self._tree_database_id_from_double_click(
            self.budgetary_tree, event
        )
        if item_id is None:
            return "break"

        self.after_idle(
            lambda item_id=item_id:
            self._open_budgetary_transaction_editor(item_id)
        )
        return "break"

    def edit_budgetary_transaction(self):
        selected = self.budgetary_tree.selection()
        if not selected:
            return

        item_id = int(
            self.budgetary_tree.item(selected[0])["values"][0]
        )
        self._open_budgetary_transaction_editor(item_id)

    def delete_budgetary_transaction(self):
        selected = self.budgetary_tree.selection()
        if not selected:
            return

        values = self.budgetary_tree.item(selected[0])["values"]
        item_id = int(values[0])
        name = values[1]

        if messagebox.askyesno(
            "Delete budgetary transaction",
            f'Delete "{name}" from the forecast?',
            parent=self,
        ):
            self.db.delete_budget_item(item_id)
            self.refresh_all()

    def refresh_budgetary_transactions(self):
        if not hasattr(self, "budgetary_tree"):
            return

        for item in self.budgetary_tree.get_children():
            self.budgetary_tree.delete(item)

        for row in self.db.get_all_budget_items():
            if row["category_type"]:
                amount = self.db.normalise_budget_amount(
                    row["category_id"], row["amount"]
                )
            else:
                amount = row["amount"]

            self.budgetary_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["name"],
                    row["account_name"],
                    row["category_name"] or "(Uncategorised)",
                    row["payee"],
                    money(amount),
                    row["frequency"],
                    self.format_date(row["next_date"]),
                    self.format_date(row["end_date"]) if row["end_date"] else "",
                ),
            )

    # ==========================================================
    # Six Month Budget tab
    # ==========================================================

    def _build_budget_tab(self):
        self.projection_month_data = {}

        top = ttk.Frame(self.budget_tab)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="Project account:", style="Heading.TLabel").pack(side="left")
        self.budget_account = ttk.Combobox(top, state="readonly", width=28)
        self.budget_account.pack(side="left", padx=(8, 12))
        self.budget_account.bind(
            "<<ComboboxSelected>>", lambda event: self.refresh_budget_projection()
        )

        ttk.Button(
            top,
            text="Create Scenario Sheet...",
            command=self.create_scenario_from_projection,
        ).pack(side="left", padx=(0, 12))

        self.budget_start_balance_var = tk.StringVar(value="Starting balance: £0.00")
        ttk.Label(
            top,
            textvariable=self.budget_start_balance_var,
            style="RegisterBalance.TLabel",
        ).pack(side="right")

        intro = ttk.Label(
            self.budget_tab,
            text=(
                "Projection starts with the account's current balance and includes "
                "future Scheduled transactions plus forecast-only Budgetary Transactions."
            ),
        )
        intro.pack(anchor="w", pady=(0, 8))

        summary_box = ttk.LabelFrame(
            self.budget_tab, text="Six-month projection", padding=8
        )
        summary_box.pack(fill="x", pady=(0, 8))

        summary_columns = ("month", "opening", "income", "spending", "closing")
        self.budget_summary_tree = ttk.Treeview(
            summary_box,
            columns=summary_columns,
            show="headings",
            height=6,
            selectmode="browse",
        )

        summary_headings = {
            "month": "Month",
            "opening": "Starting Balance",
            "income": "Income",
            "spending": "Spending",
            "closing": "Ending Balance",
        }
        for col in summary_columns:
            self.budget_summary_tree.heading(col, text=summary_headings[col])
            self.budget_summary_tree.column(
                col,
                width=180 if col == "month" else 160,
                anchor="e" if col != "month" else "w",
            )

        self.budget_summary_tree.pack(fill="x")
        self.budget_summary_tree.bind(
            "<<TreeviewSelect>>", lambda event: self.refresh_budget_month_detail()
        )

        detail_box = ttk.LabelFrame(
            self.budget_tab, text="Selected month detail", padding=8
        )
        detail_box.pack(fill="both", expand=True, pady=(0, 8))

        detail_columns = (
            "date",
            "description",
            "source",
            "income",
            "spending",
            "balance",
        )
        self.budget_detail_tree = ttk.Treeview(
            detail_box, columns=detail_columns, show="headings"
        )

        detail_headings = {
            "date": "Date",
            "description": "Description",
            "source": "Source",
            "income": "Income",
            "spending": "Spending",
            "balance": "Projected Balance",
        }
        detail_widths = {
            "date": 105,
            "description": 290,
            "source": 115,
            "income": 120,
            "spending": 120,
            "balance": 150,
        }

        for col in detail_columns:
            self.budget_detail_tree.heading(col, text=detail_headings[col])
            self.budget_detail_tree.column(
                col,
                width=detail_widths[col],
                anchor="e" if col in ("income", "spending", "balance") else "w",
            )

        self.budget_detail_tree.pack(fill="both", expand=True)

        items_box = ttk.LabelFrame(
            self.budget_tab, text="Budgetary Transactions (forecast only)", padding=8
        )
        items_box.pack(fill="x")

        item_columns = (
            "id", "name", "category", "payee", "amount", "frequency", "next_date", "end_date"
        )
        self.budget_items_tree = ttk.Treeview(
            items_box,
            columns=item_columns,
            show="headings",
            height=5,
            selectmode="browse",
        )
        item_headings = {
            "id": "ID",
            "name": "Name",
            "category": "Category",
            "payee": "Payee / Description",
            "amount": "Amount",
            "frequency": "Frequency",
            "next_date": "First / Next Date",
            "end_date": "End Date",
        }
        item_widths = {
            "id": 0,
            "name": 180,
            "category": 140,
            "payee": 190,
            "amount": 110,
            "frequency": 100,
            "next_date": 125,
            "end_date": 125,
        }

        for col in item_columns:
            self.budget_items_tree.heading(col, text=item_headings[col])
            self.budget_items_tree.column(
                col,
                width=item_widths[col],
                stretch=False if col == "id" else True,
                anchor="e" if col == "amount" else "w",
            )
        self.budget_items_tree.column("id", width=0, stretch=False)
        self.budget_items_tree.pack(fill="x")
        self.budget_items_tree.bind(
            "<Double-1>", self.on_budget_item_double_click
        )

        item_buttons = ttk.Frame(items_box)
        item_buttons.pack(fill="x", pady=(8, 0))

        ttk.Button(
            item_buttons, text="Add Budgetary Transaction", command=self.add_budget_item
        ).pack(side="left")
        ttk.Button(
            item_buttons, text="Edit selected", command=self.edit_budget_item
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            item_buttons, text="Delete selected", command=self.delete_budget_item
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            item_buttons, text="Refresh Projection", command=self.refresh_budget_projection
        ).pack(side="right")

    def current_budget_account_id(self):
        return self.account_name_to_id.get(self.budget_account.get())

    def add_budget_item(self):
        if not self.account_name_to_id:
            messagebox.showerror("No accounts", "Create an account first.", parent=self)
            return

        dialog = BudgetItemDialog(
            self,
            self,
            preset_account=self.budget_account.get() or None,
        )
        self.wait_window(dialog)
        if dialog.result:
            self.refresh_all()

    def _open_budget_item_editor(self, item_id):
        try:
            dialog = BudgetItemDialog(
                self, self, item_id=item_id
            )
        except Exception as exc:
            messagebox.showerror(
                "Cannot edit budgetary transaction",
                str(exc),
                parent=self,
            )
            return

        self.wait_window(dialog)
        if getattr(dialog, "result", False):
            self.refresh_all()

    def on_budget_item_double_click(self, event):
        item_id = self._tree_database_id_from_double_click(
            self.budget_items_tree, event
        )
        if item_id is None:
            return "break"

        self.after_idle(
            lambda item_id=item_id:
            self._open_budget_item_editor(item_id)
        )
        return "break"

    def edit_budget_item(self):
        selected = self.budget_items_tree.selection()
        if not selected:
            return

        item_id = int(
            self.budget_items_tree.item(selected[0])["values"][0]
        )
        self._open_budget_item_editor(item_id)

    def delete_budget_item(self):
        selected = self.budget_items_tree.selection()
        if not selected:
            return

        item_id = int(self.budget_items_tree.item(selected[0])["values"][0])
        name = self.budget_items_tree.item(selected[0])["values"][1]

        if messagebox.askyesno(
            "Delete budget item",
            f'Delete the budgetary transaction "{name}" from the forecast?',
            parent=self,
        ):
            self.db.delete_budget_item(item_id)
            self.refresh_all()

    def build_projection_events(self, account_id, from_date, to_date):
        events = []

        # Scheduled transactions already in the finance database.
        for row in self.db.get_active_schedules_for_account(account_id):
            try:
                first = parse_date(row["next_date"])
            except ValueError:
                continue

            for occurrence in projection_dates(
                first, row["frequency"], from_date, to_date
            ):
                description = row["name"] or row["payee"] or "Scheduled transaction"
                category_type = (row["category_type"] or "").strip().casefold()
                if category_type == "expense":
                    projected_amount = -abs(row["amount"])
                elif category_type == "income":
                    projected_amount = abs(row["amount"])
                else:
                    projected_amount = row["amount"]

                events.append(
                    {
                        "date": occurrence,
                        "description": description,
                        "source": "Scheduled",
                        "amount": projected_amount,
                    }
                )

        # Projection-only budget items.
        for row in self.db.get_budget_items_for_account(account_id):
            try:
                first = parse_date(row["next_date"])
            except ValueError:
                continue

            end = None
            if row["end_date"]:
                try:
                    end = parse_date(row["end_date"])
                except ValueError:
                    end = None

            for occurrence in projection_dates(
                first,
                row["frequency"],
                from_date,
                to_date,
                end,
            ):
                category_type = (row["category_type"] or "").strip().casefold()
                if category_type == "expense":
                    projected_amount = -abs(row["amount"])
                elif category_type == "income":
                    projected_amount = abs(row["amount"])
                else:
                    projected_amount = row["amount"]

                description = row["payee"] or row["name"] or "Budgetary transaction"

                events.append(
                    {
                        "date": occurrence,
                        "description": description,
                        "source": "Budgetary",
                        "amount": projected_amount,
                    }
                )

        # Income first when multiple items share a date, then spending.
        events.sort(
            key=lambda event: (
                event["date"],
                0 if event["amount"] > 0 else 1,
                event["description"].casefold(),
            )
        )
        return events

    def refresh_budget_items(self):
        for item in self.budget_items_tree.get_children():
            self.budget_items_tree.delete(item)

        account_id = self.current_budget_account_id()
        if not account_id:
            return

        for row in self.db.get_budget_items_for_account(account_id):
            amount = self.db.normalise_budget_amount(
                row["category_id"], row["amount"]
            )
            self.budget_items_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["name"],
                    row["category_name"] or "(Uncategorised)",
                    row["payee"],
                    money(amount),
                    row["frequency"],
                    self.format_date(row["next_date"]),
                    self.format_date(row["end_date"]) if row["end_date"] else "",
                ),
            )

    def refresh_budget_projection(self):
        if not hasattr(self, "budget_summary_tree"):
            return

        previous_month = None
        selection = self.budget_summary_tree.selection()
        if selection:
            previous_month = self.budget_summary_tree.item(selection[0])["values"][0]

        for item in self.budget_summary_tree.get_children():
            self.budget_summary_tree.delete(item)
        for item in self.budget_detail_tree.get_children():
            self.budget_detail_tree.delete(item)

        self.projection_month_data = {}

        account_id = self.current_budget_account_id()
        if not account_id:
            self.budget_start_balance_var.set("Starting balance: £0.00")
            self.refresh_budget_items()
            return

        account = self.db.get_account(account_id)
        if not account:
            return

        today = date.today()
        first_month = month_start(today)
        last_month = add_months(first_month, 5)
        horizon_end = month_end(last_month)

        events = self.build_projection_events(
            account_id,
            today,
            horizon_end,
        )

        current_balance = float(account["balance"])
        self.budget_start_balance_var.set(
            f"Starting balance: {money(current_balance)}"
        )

        event_index = 0
        running_balance = current_balance
        inserted_items = []

        for month_offset in range(6):
            m_start = add_months(first_month, month_offset)
            m_end = month_end(m_start)

            visible_start = today if month_offset == 0 else m_start
            opening_balance = running_balance

            month_events = []
            while event_index < len(events):
                event = events[event_index]
                if event["date"] > m_end:
                    break
                if event["date"] >= visible_start:
                    month_events.append(event)
                event_index += 1

            income = sum(
                event["amount"] for event in month_events if event["amount"] > 0
            )
            spending = sum(
                abs(event["amount"]) for event in month_events if event["amount"] < 0
            )

            detail_rows = []
            month_running = opening_balance
            for event in month_events:
                month_running += event["amount"]
                detail_rows.append(
                    {
                        **event,
                        "balance": month_running,
                    }
                )

            closing_balance = month_running
            running_balance = closing_balance

            label = m_start.strftime("%B %Y")
            tree_item = self.budget_summary_tree.insert(
                "",
                "end",
                values=(
                    label,
                    money(opening_balance),
                    money(income),
                    money(spending),
                    money(closing_balance),
                ),
            )

            self.projection_month_data[tree_item] = {
                "label": label,
                "opening": opening_balance,
                "income": income,
                "spending": spending,
                "closing": closing_balance,
                "rows": detail_rows,
            }
            inserted_items.append(tree_item)

        self.refresh_budget_items()

        # Restore month selection when possible.
        target_item = None
        if previous_month:
            for item_id in inserted_items:
                if self.budget_summary_tree.item(item_id)["values"][0] == previous_month:
                    target_item = item_id
                    break

        if target_item is None and inserted_items:
            target_item = inserted_items[0]

        if target_item:
            self.budget_summary_tree.selection_set(target_item)
            self.budget_summary_tree.focus(target_item)
            self.refresh_budget_month_detail()

    def refresh_budget_month_detail(self):
        for item in self.budget_detail_tree.get_children():
            self.budget_detail_tree.delete(item)

        selection = self.budget_summary_tree.selection()
        if not selection:
            return

        data = self.projection_month_data.get(selection[0])
        if not data:
            return

        for row in data["rows"]:
            self.budget_detail_tree.insert(
                "",
                "end",
                values=(
                    self.format_date(row["date"]),
                    row["description"],
                    row["source"],
                    money(row["amount"]) if row["amount"] > 0 else "",
                    money(abs(row["amount"])) if row["amount"] < 0 else "",
                    money(row["balance"]),
                ),
            )

    # ==========================================================
    # Categories tab
    # ==========================================================

    def _build_categories_tab(self):
        form = ttk.LabelFrame(self.categories_tab, text="Add category", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        self.cat_name = ttk.Entry(form, width=35)
        self.cat_name.grid(row=1, column=0, padx=(0, 10))

        ttk.Label(form, text="Type").grid(row=0, column=1, sticky="w")
        self.cat_type = ttk.Combobox(
            form, state="readonly", values=["Expense", "Income"], width=18
        )
        self.cat_type.grid(row=1, column=1, padx=(0, 10))
        self.cat_type.set("Expense")

        ttk.Button(form, text="Add category", command=self.add_category).grid(
            row=1, column=2
        )

        columns = ("id", "name", "type")
        self.categories_tree = ttk.Treeview(
            self.categories_tab, columns=columns, show="headings"
        )
        self.categories_tree.heading("id", text="ID")
        self.categories_tree.heading("name", text="Category")
        self.categories_tree.heading("type", text="Type")
        self.categories_tree.column("id", width=70)
        self.categories_tree.column("name", width=350)
        self.categories_tree.column("type", width=150)
        self.categories_tree.pack(fill="both", expand=True)
        self.categories_tree.bind(
            "<Double-1>", self.on_category_double_click
        )

        bottom = ttk.Frame(self.categories_tab)
        bottom.pack(fill="x", pady=(8, 0))
        ttk.Button(
            bottom, text="Edit selected category", command=self.edit_category
        ).pack(side="left")

        ttk.Button(
            bottom, text="Delete selected category", command=self.delete_category
        ).pack(side="left", padx=(8, 0))

        ttk.Button(bottom, text="Refresh", command=self.refresh_all).pack(side="right")

    def add_category(self):
        name = self.cat_name.get().strip()
        if not name:
            messagebox.showerror("Missing category name", "Please enter a category name.")
            return

        try:
            self.db.add_category(name, self.cat_type.get())
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate category", "A category with that name already exists."
            )
            return

        self.cat_name.delete(0, tk.END)
        self.refresh_all()

    def _open_category_editor(self, category_id):
        try:
            dialog = CategoryEditDialog(
                self, self, category_id
            )
        except Exception as exc:
            messagebox.showerror(
                "Cannot edit category",
                str(exc),
                parent=self,
            )
            return

        self.wait_window(dialog)
        if getattr(dialog, "result", False):
            self.refresh_all()

    def on_category_double_click(self, event):
        category_id = self._tree_database_id_from_double_click(
            self.categories_tree, event
        )
        if category_id is None:
            return "break"

        self.after_idle(
            lambda category_id=category_id:
            self._open_category_editor(category_id)
        )
        return "break"

    def edit_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            messagebox.showinfo(
                "No category selected",
                "Select a category first.",
                parent=self,
            )
            return

        category_id = int(
            self.categories_tree.item(selected[0])["values"][0]
        )
        self._open_category_editor(category_id)

    def delete_category(self):
        selected = self.categories_tree.selection()
        if not selected:
            return

        category_id = self.categories_tree.item(selected[0])["values"][0]

        if not messagebox.askyesno(
            "Delete category", "Delete the selected category?"
        ):
            return

        try:
            self.db.delete_category(category_id)
        except ValueError as exc:
            messagebox.showerror("Cannot delete category", str(exc))
            return

        self.refresh_all()

    # ==========================================================
    # Scheduled tab
    # ==========================================================

    def _build_scheduled_tab(self):
        form = ttk.LabelFrame(
            self.scheduled_tab, text="Add scheduled transaction", padding=10
        )
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        self.sch_name = ttk.Entry(form, width=22)
        self.sch_name.grid(row=1, column=0, padx=(0, 8))

        ttk.Label(form, text="Account").grid(row=0, column=1, sticky="w")
        self.sch_account = ttk.Combobox(form, state="readonly", width=20)
        self.sch_account.grid(row=1, column=1, padx=(0, 8))

        ttk.Label(form, text="Category").grid(row=0, column=2, sticky="w")
        self.sch_category = ttk.Combobox(form, state="readonly", width=20)
        self.sch_category.grid(row=1, column=2, padx=(0, 8))

        ttk.Label(form, text="Payee").grid(row=0, column=3, sticky="w")
        self.sch_payee = ttk.Entry(form, width=20)
        self.sch_payee.grid(row=1, column=3, padx=(0, 8))

        ttk.Label(form, text="Amount").grid(row=0, column=4, sticky="w")
        self.sch_amount = ttk.Entry(form, width=12)
        self.sch_amount.grid(row=1, column=4, padx=(0, 8))

        ttk.Label(form, text="Frequency").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.sch_frequency = ttk.Combobox(
            form,
            state="readonly",
            values=["Daily", "Weekly", "Monthly", "Yearly"],
            width=18,
        )
        self.sch_frequency.grid(row=3, column=0, padx=(0, 8))
        self.sch_frequency.set("Monthly")

        ttk.Label(form, text="Next date").grid(row=2, column=1, sticky="w", pady=(8, 0))
        sch_date_frame = ttk.Frame(form)
        sch_date_frame.grid(row=3, column=1, padx=(0, 8), sticky="w")

        self.sch_next_date = ttk.Entry(sch_date_frame, width=12)
        self.sch_next_date.pack(side="left")
        self.sch_next_date.insert(0, self.format_date(date.today()))

        ttk.Button(
            sch_date_frame,
            text="Select date…",
            command=self.select_schedule_date,
        ).pack(side="left", padx=(5, 0))

        ttk.Label(form, text="Memo").grid(row=2, column=2, sticky="w", pady=(8, 0))
        self.sch_memo = ttk.Entry(form, width=42)
        self.sch_memo.grid(row=3, column=2, columnspan=2, sticky="ew", padx=(0, 8))

        ttk.Button(form, text="Add schedule", command=self.add_schedule).grid(
            row=3, column=4, sticky="ew"
        )

        columns = (
            "id",
            "name",
            "account",
            "category",
            "payee",
            "amount",
            "frequency",
            "next_date",
        )
        self.scheduled_tree = ttk.Treeview(
            self.scheduled_tab, columns=columns, show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Name",
            "account": "Account",
            "category": "Category",
            "payee": "Payee",
            "amount": "Amount",
            "frequency": "Frequency",
            "next_date": "Next date",
        }
        widths = {
            "id": 55,
            "name": 170,
            "account": 145,
            "category": 145,
            "payee": 145,
            "amount": 105,
            "frequency": 100,
            "next_date": 105,
        }

        for col in columns:
            self.scheduled_tree.heading(col, text=headings[col])
            self.scheduled_tree.column(
                col,
                width=widths[col],
                anchor="e" if col == "amount" else "w",
            )

        self.scheduled_tree.pack(fill="both", expand=True)
        self.scheduled_tree.bind(
            "<Double-1>", self.on_schedule_double_click
        )

        bottom = ttk.Frame(self.scheduled_tab)
        bottom.pack(fill="x", pady=(8, 0))

        ttk.Button(
            bottom,
            text="Process due transactions now",
            command=self.process_schedules,
        ).pack(side="left")

        ttk.Button(
            bottom, text="Import CSV...", command=self.import_schedules_csv
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            bottom, text="CSV template...", command=self.save_schedule_csv_template
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            bottom, text="Edit selected schedule", command=self.edit_schedule
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            bottom, text="Delete selected schedule", command=self.delete_schedule
        ).pack(side="left", padx=(8, 0))

        ttk.Button(bottom, text="Refresh", command=self.refresh_all).pack(side="right")

    def select_schedule_date(self):
        try:
            initial = self.parse_user_date(self.sch_next_date.get())
        except ValueError:
            initial = date.today()

        picker = DatePickerDialog(self, initial)
        self.wait_window(picker)

        if picker.result is not None:
            self.sch_next_date.delete(0, tk.END)
            self.sch_next_date.insert(0, self.format_date(picker.result))
            self.sch_next_date.focus_set()

    def add_schedule(self):
        if not self.sch_account.get():
            messagebox.showerror("No account", "Create and select an account first.")
            return

        name = self.sch_name.get().strip()
        if not name:
            messagebox.showerror("Missing name", "Enter a name for the schedule.")
            return

        try:
            next_date = self.parse_user_date(self.sch_next_date.get()).isoformat()
        except ValueError:
            messagebox.showerror("Invalid date", f"Use date format {self.date_format_example()}.")
            return

        try:
            amount = float(self.sch_amount.get().strip())
        except ValueError:
            messagebox.showerror("Invalid amount", "Amount must be a number.")
            return

        account_id = self.account_name_to_id[self.sch_account.get()]
        category_id = self.category_name_to_id.get(self.sch_category.get())

        self.db.add_schedule(
            name,
            account_id,
            category_id,
            self.sch_payee.get().strip(),
            self.sch_memo.get().strip(),
            amount,
            self.sch_frequency.get(),
            next_date,
        )

        self.sch_name.delete(0, tk.END)
        self.sch_payee.delete(0, tk.END)
        self.sch_memo.delete(0, tk.END)
        self.sch_amount.delete(0, tk.END)
        self.refresh_all()

    def save_schedule_csv_template(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save scheduled transaction CSV template",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*")],
            initialfile="scheduled_transactions_template.csv",
        )
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(
                    ["Day of Month", "Account", "Category", "Payee", "Amount", "Frequency"]
                )
                writer.writerow([1, "Current Account", "Mortgage / Rent", "Mortgage", "-577.00", "Monthly"])
                writer.writerow([15, "Current Account", "Salary", "Salary", "2500.00", "Monthly"])
        except OSError as exc:
            messagebox.showerror("Could not save CSV", str(exc), parent=self)
            return

        messagebox.showinfo(
            "CSV template saved",
            "Template saved successfully. Replace the example account names with names that exist in Simple Finance.",
            parent=self,
        )

    @staticmethod
    def _normalise_csv_header(value):
        return " ".join((value or "").replace("_", " ").strip().lower().split())

    @staticmethod
    def _normalise_lookup_name(value):
        """
        Normalise account/category names for forgiving CSV matching.

        This deliberately treats common Unicode punctuation variants as the same,
        e.g. an en dash (–) or em dash (—) in a spreadsheet matches a normal
        hyphen (-) in Simple Finance. It also ignores repeated whitespace and
        spacing around hyphens.
        """
        value = unicodedata.normalize("NFKC", value or "")
        replacements = {
            "–": "-",
            "—": "-",
            "−": "-",
            "‑": "-",
            "‘": "'",
            "’": "'",
            "“": '"',
            "”": '"',
            " ": " ",  # non-breaking space
        }
        for old, new in replacements.items():
            value = value.replace(old, new)
        value = " ".join(value.strip().split())
        value = value.replace(" - ", "-").replace("- ", "-").replace(" -", "-")
        return value.casefold()

    def import_schedules_csv(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Import scheduled transactions from CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*")],
        )
        if not path:
            return

        # Case-insensitive lookups while preserving the actual database IDs.
        account_lookup = {
            self._normalise_lookup_name(row["name"]): (row["id"], row["name"])
            for row in self.db.get_account_choices()
        }
        category_lookup = {
            self._normalise_lookup_name(row["name"]): (row["id"], row["name"])
            for row in self.db.get_category_choices()
        }

        required = {
            "day of month": "Day of Month",
            "account": "Account",
            "category": "Category",
            "payee": "Payee",
            "amount": "Amount",
            "frequency": "Frequency",
        }
        frequency_lookup = {
            "daily": "Daily",
            "day": "Daily",
            "weekly": "Weekly",
            "week": "Weekly",
            "monthly": "Monthly",
            "month": "Monthly",
            "yearly": "Yearly",
            "year": "Yearly",
            "annual": "Yearly",
            "annually": "Yearly",
        }

        errors = []
        pending = []

        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    messagebox.showerror(
                        "Invalid CSV", "The CSV does not contain a header row.", parent=self
                    )
                    return

                normalised_fields = {
                    self._normalise_csv_header(field): field for field in reader.fieldnames
                }
                missing = [label for key, label in required.items() if key not in normalised_fields]
                if missing:
                    messagebox.showerror(
                        "Invalid CSV",
                        "Missing required column(s): " + ", ".join(missing),
                        parent=self,
                    )
                    return

                actual = {key: normalised_fields[key] for key in required}

                for line_no, raw in enumerate(reader, start=2):
                    # Ignore completely blank rows.
                    if not any((value or "").strip() for value in raw.values()):
                        continue

                    day_text = (raw.get(actual["day of month"]) or "").strip()
                    account_text = (raw.get(actual["account"]) or "").strip()
                    category_text = (raw.get(actual["category"]) or "").strip()
                    payee = (raw.get(actual["payee"]) or "").strip()
                    amount_text = (raw.get(actual["amount"]) or "").strip()
                    frequency_text = (raw.get(actual["frequency"]) or "").strip()

                    row_errors = []

                    try:
                        day_of_month = int(day_text)
                        if not 1 <= day_of_month <= 31:
                            raise ValueError
                    except ValueError:
                        row_errors.append("Day of Month must be 1-31")
                        day_of_month = None

                    account_match = account_lookup.get(self._normalise_lookup_name(account_text))
                    if not account_match:
                        row_errors.append(f'unknown account "{account_text}"')

                    category_match = category_lookup.get(self._normalise_lookup_name(category_text))
                    if not category_match:
                        row_errors.append(f'unknown category "{category_text}"')

                    if not payee:
                        row_errors.append("Payee is blank")

                    try:
                        amount = float(amount_text.replace(",", "").replace("£", "").strip())
                    except ValueError:
                        row_errors.append(f'invalid amount "{amount_text}"')
                        amount = None

                    frequency = frequency_lookup.get(frequency_text.casefold())
                    if not frequency:
                        row_errors.append(
                            f'frequency must be Daily, Weekly, Monthly or Yearly (got "{frequency_text}")'
                        )

                    if row_errors:
                        errors.append(f"Row {line_no}: " + "; ".join(row_errors))
                        continue

                    next_date = first_due_date_from_day(day_of_month).isoformat()
                    pending.append(
                        {
                            "name": payee,
                            "account_id": account_match[0],
                            "category_id": category_match[0],
                            "payee": payee,
                            "memo": "Imported from CSV",
                            "amount": amount,
                            "frequency": frequency,
                            "next_date": next_date,
                        }
                    )
        except (OSError, csv.Error) as exc:
            messagebox.showerror("Could not read CSV", str(exc), parent=self)
            return

        if errors:
            shown = errors[:15]
            extra = len(errors) - len(shown)
            details = "\n".join(shown)
            if extra:
                details += f"\n\n...and {extra} more error(s)."
            messagebox.showerror(
                "CSV import stopped",
                "Nothing was imported because the CSV contains errors:\n\n" + details,
                parent=self,
            )
            return

        if not pending:
            messagebox.showinfo(
                "Nothing to import", "No scheduled transactions were found in the CSV.", parent=self
            )
            return

        if not messagebox.askyesno(
            "Import scheduled transactions",
            f"Import {len(pending)} scheduled transaction(s)?\n\n"
            "The Payee will also be used as the schedule name.\n"
            "Day of Month determines the first next due date.",
            parent=self,
        ):
            return

        self.db.add_schedules_bulk(pending)
        self.refresh_all()
        messagebox.showinfo(
            "Import complete",
            f"Imported {len(pending)} scheduled transaction(s).",
            parent=self,
        )

    def _open_schedule_editor(self, schedule_id):
        try:
            dialog = ScheduledTransactionDialog(
                self, self, schedule_id
            )
        except Exception as exc:
            messagebox.showerror(
                "Cannot edit scheduled transaction",
                str(exc),
                parent=self,
            )
            return

        self.wait_window(dialog)
        if getattr(dialog, "result", False):
            self.refresh_all()

    def on_schedule_double_click(self, event):
        schedule_id = self._tree_database_id_from_double_click(
            self.scheduled_tree, event
        )
        if schedule_id is None:
            return "break"

        self.after_idle(
            lambda schedule_id=schedule_id:
            self._open_schedule_editor(schedule_id)
        )
        return "break"

    def edit_schedule(self):
        selected = self.scheduled_tree.selection()
        if not selected:
            messagebox.showinfo(
                "No schedule selected",
                "Select a scheduled transaction first.",
                parent=self,
            )
            return

        schedule_id = int(
            self.scheduled_tree.item(selected[0])["values"][0]
        )
        self._open_schedule_editor(schedule_id)

    def delete_schedule(self):
        selected = self.scheduled_tree.selection()
        if not selected:
            return

        schedule_id = self.scheduled_tree.item(selected[0])["values"][0]

        if messagebox.askyesno(
            "Delete schedule", "Delete the selected scheduled transaction?"
        ):
            self.db.delete_schedule(schedule_id)
            self.refresh_all()

    def process_schedules(self):
        created = self.db.process_due_schedules()
        self.refresh_all()
        messagebox.showinfo(
            "Scheduled transactions",
            f"{created} scheduled transaction(s) were added.",
        )

    # ==========================================================
    # Refresh
    # ==========================================================

    def refresh_all(self):
        self.refresh_accounts()
        self.refresh_categories()
        self.refresh_choices()
        self.refresh_register()
        self.refresh_schedules()
        self.refresh_budgetary_transactions()
        self.refresh_budget_projection()
        self.refresh_scenario_choices()
        self.refresh_backup_status()

        if hasattr(self, "settings_date_format"):
            expected = DATE_FORMATS[self.date_format_key]["label"]
            if self.settings_date_format.get() != expected:
                self.settings_date_format.set(expected)
            self.update_settings_date_example()

    def refresh_accounts(self):
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)

        total = 0.0
        for row in self.db.get_accounts():
            total += row["balance"]
            self.accounts_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["name"],
                    row["account_type"],
                    money(row["opening_balance"]),
                    money(row["balance"]),
                ),
            )

        self.total_balance_var.set(f"Total: {money(total)}")

    def refresh_categories(self):
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)

        for row in self.db.get_categories():
            self.categories_tree.insert(
                "", "end", values=(row["id"], row["name"], row["category_type"])
            )

    def refresh_choices(self):
        accounts = self.db.get_account_choices()
        self.account_name_to_id = {row["name"]: row["id"] for row in accounts}
        self.account_id_to_name = {row["id"]: row["name"] for row in accounts}
        account_names = list(self.account_name_to_id.keys())

        current_register = self.register_account.get()
        current_schedule = self.sch_account.get()
        current_budget = self.budget_account.get() if hasattr(self, "budget_account") else ""

        self.register_account["values"] = account_names
        self.sch_account["values"] = account_names
        if hasattr(self, "budget_account"):
            self.budget_account["values"] = account_names

        if current_register in account_names:
            self.register_account.set(current_register)
        elif account_names:
            self.register_account.set(account_names[0])
        else:
            self.register_account.set("")

        if current_schedule in account_names:
            self.sch_account.set(current_schedule)
        elif account_names:
            self.sch_account.set(account_names[0])
        else:
            self.sch_account.set("")


        if hasattr(self, "budget_account"):
            if current_budget in account_names:
                self.budget_account.set(current_budget)
            elif current_register in account_names:
                self.budget_account.set(current_register)
            elif account_names:
                self.budget_account.set(account_names[0])
            else:
                self.budget_account.set("")

        categories = self.db.get_category_choices()
        self.category_name_to_id = {row["name"]: row["id"] for row in categories}
        category_names = list(self.category_name_to_id.keys())

        current_sch_category = self.sch_category.get()
        self.sch_category["values"] = category_names
        if current_sch_category in category_names:
            self.sch_category.set(current_sch_category)
        elif category_names:
            self.sch_category.set(category_names[0])

    def refresh_register(self):
        for item in self.register_tree.get_children():
            self.register_tree.delete(item)

        account_id = self.current_register_account_id()
        if not account_id:
            self.register_balance_var.set("Balance: £0.00")
            return

        account = self.db.get_account(account_id)
        rows = self.db.get_register_transactions(account_id)

        for row in reversed(rows):
            payment = money(abs(row["amount"])) if row["amount"] < 0 else ""
            deposit = money(row["amount"]) if row["amount"] > 0 else ""
            category = row["category_name"]
            if row["transfer_group"]:
                category = "Transfer"

            self.register_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    self.format_date(row["txn_date"]),
                    row["payee"],
                    category,
                    row["memo"],
                    payment,
                    deposit,
                    "✓" if row["reconciled"] else "",
                    money(row["balance"]),
                ),
            )

        self.register_balance_var.set(f'Balance: {money(account["balance"])}')

        children = self.register_tree.get_children()
        if children:
            self.register_tree.see(children[0])

    def refresh_schedules(self):
        for item in self.scheduled_tree.get_children():
            self.scheduled_tree.delete(item)

        for row in self.db.get_schedules():
            self.scheduled_tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["name"],
                    row["account_name"],
                    row["category_name"],
                    row["payee"],
                    money(row["amount"]),
                    row["frequency"],
                    self.format_date(row["next_date"]),
                ),
            )

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = SimpleFinanceApp()
    app.mainloop()
