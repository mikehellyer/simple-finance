"""Generates the Simple Finance user manual as a PDF.

    python docs/build_manual.py [version] [output_path]

`version` defaults to the app's own src/simplefinance/version.py value;
`output_path` defaults to dist/installers/Simple-Finance-User-Manual.pdf
(matching where the CI workflow expects release assets to land).
"""

import itertools
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

ICON_PATH = os.path.join(ROOT, "src", "simplefinance", "icon.png")

if len(sys.argv) > 1:
    APP_VERSION = sys.argv[1]
else:
    from simplefinance.version import __version__ as APP_VERSION

OUTPUT_PATH = (
    sys.argv[2]
    if len(sys.argv) > 2
    else os.path.join(ROOT, "dist", "installers", "Simple-Finance-User-Manual.pdf")
)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

RED = colors.HexColor("#c62828")
DARK = colors.HexColor("#222222")
GREY = colors.HexColor("#555555")
LIGHT_GREY = colors.HexColor("#dddddd")
NOTE_BG = colors.HexColor("#fff3cd")
NOTE_BORDER = colors.HexColor("#e0a800")
IMPORTANT_BG = colors.HexColor("#fde2e1")
IMPORTANT_BORDER = RED

# ---------------------------------------------------------------- styles ---

base = getSampleStyleSheet()

styles = {
    "CoverTitle": ParagraphStyle(
        "CoverTitle", parent=base["Title"], fontSize=32, leading=38,
        textColor=DARK, spaceAfter=6, alignment=TA_CENTER,
    ),
    "CoverSubtitle": ParagraphStyle(
        "CoverSubtitle", parent=base["Normal"], fontSize=16, leading=20,
        textColor=GREY, alignment=TA_CENTER, spaceAfter=4,
    ),
    "CoverMeta": ParagraphStyle(
        "CoverMeta", parent=base["Normal"], fontSize=11, leading=14,
        textColor=GREY, alignment=TA_CENTER,
    ),
    "H1": ParagraphStyle(
        "H1", parent=base["Heading1"], fontSize=18, leading=22,
        textColor=DARK, spaceBefore=18, spaceAfter=10,
        borderColor=LIGHT_GREY, borderWidth=0, borderPadding=0,
    ),
    "H2": ParagraphStyle(
        "H2", parent=base["Heading2"], fontSize=13, leading=17,
        textColor=RED, spaceBefore=14, spaceAfter=6,
    ),
    "Body": ParagraphStyle(
        "Body", parent=base["Normal"], fontSize=10.3, leading=14.5,
        textColor=DARK, spaceAfter=8,
    ),
    "Bullet": ParagraphStyle(
        "Bullet", parent=base["Normal"], fontSize=10.3, leading=14.5,
        textColor=DARK, leftIndent=16, bulletIndent=4, spaceAfter=4,
    ),
    "TOCHeading": ParagraphStyle(
        "TOCHeading", parent=base["Heading1"], fontSize=20, spaceAfter=14,
    ),
}

toc_style1 = ParagraphStyle(
    "TOCLevel1", parent=base["Normal"], fontSize=11.5, leading=16,
    firstLineIndent=0, leftIndent=0, textColor=DARK, spaceAfter=4,
)
toc_style2 = ParagraphStyle(
    "TOCLevel2", parent=base["Normal"], fontSize=10, leading=13,
    firstLineIndent=0, leftIndent=18, textColor=GREY, spaceAfter=2,
)

# ---------------------------------------------------------- doc template ---


class ManualDoc(BaseDocTemplate):
    def build(self, flowables, **kw):
        self._bookmark_counter = itertools.count()
        return super().build(flowables, **kw)

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "H1":
                key = f"toc-{next(self._bookmark_counter)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=0, closed=0)
                self.notify("TOCEntry", (0, text, self.page, key))
            elif style_name == "H2":
                key = f"toc-{next(self._bookmark_counter)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=1, closed=1)
                self.notify("TOCEntry", (1, text, self.page, key))


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(
        letter[0] / 2, 0.5 * inch, f"Simple Finance User Manual  |  Page {doc.page}"
    )
    canvas.restoreState()


def draw_cover(canvas, doc):
    pass  # cover content is in the flowables; no footer on the cover


doc = ManualDoc(
    OUTPUT_PATH,
    pagesize=letter,
    topMargin=0.85 * inch,
    bottomMargin=0.85 * inch,
    leftMargin=0.9 * inch,
    rightMargin=0.9 * inch,
    title="Simple Finance User Manual",
    author="Simple Finance",
)

frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="cover")

doc.addPageTemplates(
    [
        PageTemplate(id="Cover", frames=cover_frame, onPage=draw_cover),
        PageTemplate(id="Normal", frames=frame, onPage=draw_footer),
    ]
)

# ------------------------------------------------------------- helpers -----


def h1(text):
    return Paragraph(text, styles["H1"])


def h2(text):
    return Paragraph(text, styles["H2"])


def body(text):
    return Paragraph(text, styles["Body"])


def bullets(items):
    out = []
    for item in items:
        out.append(Paragraph(f"&bull;&nbsp;&nbsp;{item}", styles["Bullet"]))
    return out


def note(text, kind="Tip"):
    bg = IMPORTANT_BG if kind == "Important" else NOTE_BG
    border = IMPORTANT_BORDER if kind == "Important" else NOTE_BORDER
    p = Paragraph(f"<b>{kind}:</b> {text}", styles["Body"])
    t = Table([[p]], colWidths=[doc.width])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 1, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def sp(height=8):
    return Spacer(1, height)


# --------------------------------------------------------------- content ---

story = []

# Cover page
story.append(sp(1.2 * inch))
story.append(Image(ICON_PATH, width=1.3 * inch, height=1.3 * inch))
story.append(sp(0.35 * inch))
story.append(Paragraph("Simple Finance", styles["CoverTitle"]))
story.append(Paragraph("User Manual", styles["CoverSubtitle"]))
story.append(sp(0.25 * inch))
story.append(
    Paragraph(
        "Personal finance, budgeting, forecasting and bank reconciliation",
        styles["CoverMeta"],
    )
)
story.append(sp(0.6 * inch))
story.append(Paragraph(f"Version {APP_VERSION}", styles["CoverMeta"]))
story.append(
    Paragraph(
        'github.com/mikehellyer/simple-finance',
        styles["CoverMeta"],
    )
)

story.append(NextPageTemplate("Normal"))
story.append(PageBreak())

# Table of contents
story.append(Paragraph("Contents", styles["TOCHeading"]))
toc = TableOfContents()
toc.levelStyles = [toc_style1, toc_style2]
story.append(toc)
story.append(PageBreak())

# 1. Getting started
story.append(h1("1. Getting Started"))
story.append(
    body(
        "Simple Finance is a personal finance program for tracking accounts and "
        "transactions, budgeting, forecasting your balance months ahead, and "
        "reconciling your records against real bank statements. All of your data "
        "stays on your own computer &mdash; nothing is sent anywhere else."
    )
)

story.append(h2("Installing"))
story.append(
    body(
        "Download the installer for your operating system from the "
        "<b>Releases</b> page of the project's GitHub repository, then run it:"
    )
)
story.extend(
    bullets(
        [
            "<b>Windows</b> &mdash; run <i>SimpleFinance-Setup.exe</i> and follow the "
            "installer. It adds a Start Menu entry and can add a desktop shortcut.",
            "<b>macOS</b> &mdash; open the <i>.dmg</i> file and drag Simple Finance into "
            "your Applications folder. The first time you open it, macOS may say it "
            "can't verify the developer &mdash; right-click (or Control-click) the app "
            "and choose <b>Open</b>, then confirm, instead of double-clicking.",
            "<b>Linux</b> &mdash; install the <i>.deb</i> file (double-click it, or run "
            "<i>sudo dpkg -i simplefinance_&lt;version&gt;_amd64.deb</i> in a terminal). "
            "This adds a menu entry with an icon.",
        ]
    )
)

story.append(h2("Starting the program for the first time"))
story.append(
    body(
        "Simple Finance opens with an empty set of accounts. The first thing to do "
        "is add at least one account (see the next section) so you have somewhere "
        "to record transactions."
    )
)
story.append(
    note(
        "Your data (accounts, transactions, categories, backups &mdash; everything) is "
        "stored privately on your own computer, not in the cloud. See "
        "<b>Backup &amp; Restore</b> (section 10) for exactly where and why it "
        "matters to back it up yourself."
    )
)

story.append(h2("The main window"))
story.append(
    body(
        "Across the top is the program name, its version number, and your total "
        "balance across all accounts. Below that is a row of tabs &mdash; each one is "
        "a different area of the program, covered in its own section below: "
        "<b>Accounts</b>, <b>Account Transactions</b>, <b>6 Month Budget</b>, "
        "<b>Scenario Sheet</b>, <b>Budgetary Transactions</b>, <b>Scheduled</b>, "
        "<b>Categories</b>, <b>Backup &amp; Restore</b> and <b>Settings</b>."
    )
)

# 2. Accounts
story.append(h1("2. Accounts"))
story.append(
    body(
        "An account represents one real place your money lives or is owed &mdash; a "
        "current/checking account, a savings account, cash, or a credit card."
    )
)
story.append(h2("Adding an account"))
story.append(
    body(
        "On the <b>Accounts</b> tab, fill in a <b>Name</b>, choose a <b>Type</b> "
        "(Current, Savings, Cash, Credit Card, or Other), enter the "
        "<b>Opening balance</b> &mdash; the balance the account actually had on the "
        "day you started tracking it here &mdash; and click <b>Add account</b>."
    )
)
story.append(h2("Viewing, editing and deleting"))
story.append(
    body(
        "The account list shows each account's type, opening balance and live "
        "current balance. Double-click an account (or select it and click "
        "<b>Open account register</b>) to see its transactions. Use <b>Edit "
        "selected account</b> to change its name, type or opening balance, or "
        "<b>Delete selected account</b> to remove it."
    )
)
story.append(
    note(
        "Changing an account's <b>opening balance</b> recalculates its entire running "
        "balance from that point forward &mdash; it isn't a one-off adjustment. Renaming "
        "an account is always safe; its transactions stay linked to it.",
        kind="Important",
    )
)

# 3. Categories
story.append(h1("3. Categories"))
story.append(
    body(
        "Categories classify what a transaction is for (Groceries, Salary, "
        "Insurance, and so on) and, just as importantly, whether it's "
        "<b>Income</b> or an <b>Expense</b>. Several other features &mdash; Scheduled "
        "Transactions, Budgetary Transactions, and the 6 Month Budget &mdash; rely on a "
        "category's type to work out automatically whether an amount should count "
        "as money in or money out."
    )
)
story.append(
    body(
        "On the <b>Categories</b> tab, add a category by giving it a name and "
        "choosing Expense or Income. Double-click an existing one to rename it or "
        "change its type."
    )
)
story.append(
    note(
        "Renaming a category is always safe. But if you switch a category between "
        "Expense and Income, every <i>future</i> Scheduled or Budgetary transaction "
        "using it will change direction too. Your past, already-recorded "
        "transactions are never altered.",
        kind="Important",
    )
)

# 4. Account Transactions
story.append(h1("4. Account Transactions"))
story.append(
    body(
        "This is your day-to-day ledger &mdash; the real, actual transactions for one "
        "account at a time. Choose which account to view from the dropdown at the "
        "top."
    )
)
story.append(h2("Adding a transaction"))
story.append(
    body(
        "Click <b>New transaction</b> and fill in the Date, Category, Payee/"
        "Description, Amount and an optional Memo."
    )
)
story.append(
    note(
        "For an ordinary transaction, type the sign yourself: a <b>negative</b> "
        "amount is money going out (a payment), and a <b>positive</b> amount is "
        "money coming in (a deposit). This is different from Scheduled and "
        "Budgetary transactions (sections 8 and 9), where you always type a "
        "positive number and the category decides the direction &mdash; it's easy to "
        "mix the two up.",
        kind="Important",
    )
)
story.append(h2("Editing and deleting"))
story.append(
    body(
        "Double-click any transaction to edit it, or select one or more rows and "
        "click <b>Delete selected</b>. The <b>Reconciled</b> column shows a "
        "checkmark once a transaction has been confirmed as part of a completed "
        "statement reconciliation (section 6) &mdash; not simply because it was "
        "imported."
    )
)
story.append(h2("Transfers between accounts"))
story.append(
    body(
        "To move money between two of your own accounts (for example, from "
        "Current to Savings), click <b>Transfer</b> instead of New transaction. "
        "Choose the From and To accounts and enter the amount as a "
        "<b>positive</b> number &mdash; Simple Finance subtracts it from one account "
        "and adds it to the other automatically, creating one linked entry in "
        "each account's register."
    )
)
story.append(
    note(
        "A transfer can't be edited as an individual transaction afterwards. If "
        "you need to change one, delete it (deleting either half deletes both) "
        "and create it again.",
        kind="Important",
    )
)

# 5. OFX import
story.append(h1("5. Importing Bank Transactions (OFX/QFX)"))
story.append(
    body(
        "Most banks let you export your recent transactions as an OFX or QFX "
        "file. Importing this file is the fastest way to bring your real bank "
        "activity into Simple Finance without typing it all in by hand."
    )
)
story.append(h2("Importing a file"))
story.append(
    body(
        "On the <b>Account Transactions</b> tab, click <b>Import OFX/QFX...</b> "
        "and choose the file you downloaded from your bank. A preview screen "
        "opens showing every transaction in the file before anything is actually "
        "imported."
    )
)
story.append(h2("Understanding the preview"))
story.append(
    body("Each row is marked with a status, shown by its colour:")
)
story.extend(
    bullets(
        [
            "<b>New</b> &mdash; not seen before. These are selected automatically and "
            "will simply be added as new transactions.",
            "<b>Already imported</b> (grey) &mdash; this exact bank transaction has "
            "already been imported previously and is protected from being added "
            "twice.",
            "<b>Likely manual</b> (yellow) and <b>Possible manual</b> (orange) &mdash; "
            "Simple Finance thinks this bank transaction matches one you already "
            "typed in by hand.",
        ]
    )
)
story.append(
    note(
        "If you already typed in &ldquo;Tesco &pound;42.50&rdquo; yourself and then import "
        "your bank statement, the same purchase will show up highlighted as a "
        "<b>Likely manual</b> match. Select it before importing, and the bank's "
        "version will <i>replace</i> your hand-typed entry &mdash; keeping the category "
        "you already chose and its reconciled status &mdash; instead of creating a "
        "duplicate. Rows you leave unselected are left alone."
    )
)
story.append(
    body(
        "Use <b>Select All New</b>, <b>Select Likely Manual</b> or <b>Clear "
        "Selection</b> to adjust what's selected, then click <b>Import / Replace "
        "Selected</b> to finish. The button also tells you afterwards how many "
        "rows were new imports versus replacements."
    )
)

# 6. PDF reconciliation
story.append(h1("6. Reconciling Against a Statement (PDF)"))
story.append(
    body(
        "Reconciliation is a more thorough check than OFX import: it walks "
        "through an actual bank statement, line by line, and confirms every "
        "entry in Simple Finance matches it exactly, so you can be confident "
        "your records are correct for that period."
    )
)
story.append(
    note(
        "This feature reads text-based PDF statements using a free tool called "
        "Poppler. If it isn't already installed, Simple Finance will tell you "
        "when you try to use this feature. On macOS, install it with "
        "<i>brew install poppler</i> in Terminal (you'll need Homebrew: "
        "brew.sh). On Debian/Ubuntu-based Linux, use "
        "<i>sudo apt install poppler-utils</i>. On Windows, search for "
        "&ldquo;Poppler for Windows&rdquo; and add it to your PATH after installing.",
        kind="Important",
    )
)
story.append(h2("Starting a reconciliation"))
story.append(
    body(
        "Click <b>Reconcile PDF Statement...</b> and choose the statement PDF. "
        "Simple Finance reads it and opens a matching screen, with the "
        "statement's opening and closing balance pre-filled where it can read "
        "them &mdash; check these are correct before continuing."
    )
)
story.append(h2("Matching statement lines to your transactions"))
story.append(
    body("Each statement line is colour-coded against your Account Transactions:")
)
story.extend(
    bullets(
        [
            "<b>Green</b> &mdash; matched automatically.",
            "<b>Yellow</b> &mdash; a possible match Simple Finance found, waiting for "
            "you to confirm it.",
            "<b>Red/pink</b> &mdash; on the statement but missing from your account.",
            "<b>Grey</b> &mdash; already reconciled in an earlier statement.",
        ]
    )
)
story.append(
    body(
        "Use <b>Confirm Selected Match</b> to accept a suggested match, "
        "<b>Choose/Change Match...</b> to manually pick a different transaction, "
        "<b>Clear Match</b> to undo one, or <b>Add Missing to Account...</b> if a "
        "statement line genuinely has no matching transaction yet. If the "
        "statement itself was misread, use <b>Edit/Add/Delete PDF Row</b> to "
        "correct it."
    )
)
story.append(h2("Finishing"))
story.append(
    body(
        "A status banner at the top tells you when everything lines up exactly "
        "&mdash; every line matched and the confirmed total equal to the closing "
        "balance to the penny. Only then does <b>Confirm &amp; Mark Reconciled</b> "
        "become available. Clicking it puts a checkmark against every matched "
        "transaction and permanently records that this statement has been "
        "reconciled, so it can't be reconciled twice by mistake."
    )
)
story.append(
    note(
        "Reconciliation is exact and all-or-nothing by design &mdash; it won't let you "
        "finish with anything left unmatched or a balance that's out by even a "
        "penny. Expect your first reconciliation for an account to take a little "
        "time while you match everything up; it gets quicker afterwards."
    )
)

# 7. Scheduled transactions
story.append(h1("7. Scheduled Transactions"))
story.append(
    body(
        "Scheduled transactions are recurring items &mdash; rent, salary, "
        "subscriptions &mdash; that Simple Finance adds to your <b>real</b> Account "
        "Transactions for you automatically, on time, every time."
    )
)
story.append(h2("Adding a schedule"))
story.append(
    body(
        "On the <b>Scheduled</b> tab, fill in a Name, Account, Category, Payee, "
        "Amount, how often it repeats (Daily, Weekly, Monthly or Yearly) and the "
        "next date it's due, then click <b>Add schedule</b>."
    )
)
story.append(
    note(
        "Enter the amount as a <b>positive</b> number. The Category you choose "
        "decides whether it's treated as money in or money out &mdash; an Expense "
        "category always makes it negative, an Income category always makes it "
        "positive, automatically.",
        kind="Important",
    )
)
story.append(h2("How schedules apply automatically"))
story.append(
    body(
        "Every time you open Simple Finance, it checks for anything due and adds "
        "it straight into your Account Transactions, correctly dated, then moves "
        "the schedule on to its next due date. You can also trigger this check "
        "manually with <b>Process due transactions now</b>."
    )
)
story.append(
    note(
        "If you haven't opened Simple Finance for a while, several missed "
        "occurrences will all be created at once, each correctly backdated to "
        "when it was actually due &mdash; this is expected behaviour, not a fault. "
        "A popup tells you how many were added."
    )
)
story.append(
    body(
        "You can also bulk-add several schedules at once using <b>Import "
        "CSV...</b> &mdash; use the <b>CSV template...</b> button first to get a "
        "starter file in the right format."
    )
)

# 8. Budgetary transactions
story.append(h1("8. Budgetary Transactions"))
story.append(
    body(
        "Budgetary transactions are <b>forecast-only</b>: unlike Scheduled "
        "Transactions, they are never added to your real Account Transactions. "
        "They exist purely to shape your 6 Month Budget forecast (section 9) "
        "with things you're planning for, without committing them as real "
        "entries."
    )
)
story.append(h2("Adding a budgetary transaction"))
story.append(
    body(
        "On the <b>Budgetary Transactions</b> tab, fill in a Name, Account, "
        "Category, Payee/Description and Amount, choose a <b>Frequency</b>, and "
        "set the first date it applies from."
    )
)
story.append(
    note(
        "Just like Scheduled Transactions, enter the Amount as a <b>positive</b> "
        "number &mdash; the Category decides the direction.",
        kind="Important",
    )
)
story.append(h2("A single, one-off future item"))
story.append(
    body(
        "Choose <b>One-off</b> as the Frequency when something will only happen "
        "once, on a specific future date &mdash; for example a one-time car repair, a "
        "single irregular bill, or a gift you're planning three months from now. "
        "Set the date under <b>First / next date</b>. It will appear exactly once, "
        "on that date, in your forecast, and will never repeat."
    )
)
story.append(
    body(
        "For something that repeats, choose <b>Weekly</b>, <b>Monthly</b> or "
        "<b>Yearly</b> instead, and optionally set an <b>End date</b> if it "
        "shouldn't continue forever."
    )
)

# 9. 6 Month Budget
story.append(h1("9. The 6 Month Budget (Forecast)"))
story.append(
    body(
        "This tab shows a live, rolling six-month forecast for one account at a "
        "time, built from that account's current balance plus everything due "
        "from its Scheduled Transactions and Budgetary Transactions."
    )
)
story.append(
    body(
        "Choose which account to project from the dropdown. The top grid "
        "summarises each of the next six months (starting balance, income, "
        "spending, ending balance); click a month to see every individual line "
        "for that month below, including a <b>Source</b> column showing whether "
        "it came from a Scheduled or a Budgetary transaction."
    )
)
story.append(
    note(
        "The forecast always recalculates itself live and can't be edited "
        "directly. If you want to experiment with &ldquo;what if&rdquo; changes without "
        "touching your real schedules, use <b>Create Scenario Sheet...</b> to "
        "snapshot it into an editable copy (see the next section)."
    )
)

# 10. Scenario Sheet
story.append(h1("10. Scenario Sheets (What-If Planning)"))
story.append(
    body(
        "A Scenario Sheet is a saved, freely-editable copy of a forecast for "
        "exploring &ldquo;what if&rdquo; ideas. Editing one never changes your real "
        "transactions, schedules or budgetary items."
    )
)
story.append(
    body(
        "Create one from the 6 Month Budget tab with <b>Create Scenario "
        "Sheet...</b>, or from the Scenario Sheet tab with <b>New from 6 Month "
        "Budget...</b>, and give it a name. Several blank spare rows are added to "
        "each month so you have room to type in new hypothetical items."
    )
)
story.append(
    body(
        "Double-click a Date, Description, Income or Spending cell to edit it "
        "directly; the Balance column recalculates automatically. Use <b>Insert "
        "Row Below</b>, <b>Clear Row</b> or <b>Delete Row</b> to manage rows, and "
        "<b>Save</b>, <b>Rename...</b> or <b>Delete</b> to manage the scenario "
        "itself. <b>Export CSV...</b> saves it (balances included) for opening in "
        "Excel or LibreOffice Calc."
    )
)
story.append(
    note(
        "A scenario is a frozen snapshot taken at the moment you created it "
        "&mdash; it won't automatically update later if you go on to change the real "
        "schedules or budgetary items it was based on."
    )
)

# 11. Backup & Restore
story.append(h1("11. Backup &amp; Restore"))
story.append(
    body(
        "Everything Simple Finance knows &mdash; accounts, transactions, categories, "
        "schedules, budgetary items and saved scenarios &mdash; lives in one file on "
        "your own computer. Backing it up is the only way to protect it."
    )
)
story.append(h2("Automatic backups"))
story.append(
    body(
        "A backup is created quietly every time you open Simple Finance. The "
        "10 most recent are kept automatically; older ones are cleared out for "
        "you. Use <b>Open Backup Folder</b> on the <b>Backup &amp; Restore</b> tab "
        "to see them."
    )
)
story.append(h2("Manual backup and restore"))
story.append(
    body(
        "Click <b>Backup Now...</b> at any time to save a copy wherever you "
        "choose &mdash; an external drive or a cloud-synced folder gives real "
        "protection, since a copy sitting on the same disk won't survive that "
        "disk failing. To bring an older backup back, click <b>Restore "
        "Backup...</b> and choose the file."
    )
)
story.append(
    note(
        "Restoring replaces everything currently in Simple Finance with the "
        "backup you chose. As a safety net, Simple Finance automatically saves a "
        "copy of your <i>current</i> data first, before restoring &mdash; so even a "
        "restore you didn't mean to do can always be undone.",
        kind="Important",
    )
)

# 12. Settings
story.append(h1("12. Settings"))
story.append(
    body(
        "Currently the one setting is <b>Date format</b> &mdash; choose UK "
        "(DD/MM/YYYY), ISO (YYYY-MM-DD) or US (MM/DD/YYYY). It controls how "
        "dates are shown and typed everywhere in the program, and is saved with "
        "your data, so it's included in your backups and restored along with "
        "them."
    )
)

# 13. Updates
story.append(h1("13. Checking for Updates"))
story.append(
    body(
        "Simple Finance quietly checks for a newer version each time it starts. "
        "This never interrupts normal use &mdash; if it can't reach the internet, "
        "nothing happens."
    )
)
story.append(
    body(
        "If a newer version is available, a red banner appears above the tabs "
        "naming the new version, with an <b>Update</b> button. Clicking it "
        "downloads the new installer for your operating system and opens it for "
        "you; Simple Finance then closes itself automatically so nothing blocks "
        "you finishing the install. Nothing is ever downloaded or installed "
        "without you clicking Update yourself."
    )
)
story.append(
    body(
        "You can also check the latest release at any time on GitHub: "
        "github.com/mikehellyer/simple-finance/releases"
    )
)

# Appendix
story.append(h1("Quick Reference: Things Worth Remembering"))
story.extend(
    bullets(
        [
            "<b>Sign conventions differ.</b> Ordinary Account Transactions use a "
            "signed amount you type yourself (negative = out, positive = in). "
            "Scheduled and Budgetary transactions always want a positive number "
            "&mdash; the category decides the direction.",
            "<b>Transfers</b> are always entered as a positive amount and can't be "
            "edited afterwards &mdash; delete and recreate them instead.",
            "<b>Changing an account's opening balance</b> recalculates its whole "
            "running balance, not just from today forward.",
            "<b>Changing a category's Income/Expense type</b> only affects future "
            "Scheduled and Budgetary occurrences &mdash; past transactions are never "
            "altered.",
            "<b>OFX &ldquo;Likely/Possible manual&rdquo; matches replace, not duplicate</b> "
            "&mdash; select them so a hand-typed entry is upgraded to the bank-verified "
            "version, keeping its category.",
            "<b>PDF reconciliation needs Poppler installed</b> on your computer "
            "(see section 6).",
            "<b>Missed scheduled transactions catch up automatically</b>, backdated "
            "to when they were actually due, next time you open the program.",
            "<b>Scenario Sheets are snapshots</b> &mdash; editing one never touches your "
            "real data, and it won't update itself if the real data changes later.",
        ]
    )
)

doc.multiBuild(story)
print(f"Wrote {OUTPUT_PATH}")
