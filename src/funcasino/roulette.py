import random

RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
EVEN = set(range(2, 37, 2))
ODD = set(range(1, 37, 2))
LOW = set(range(1, 19))
HIGH = set(range(19, 37))

FIRST_DOZEN = set(range(1, 13))
SECOND_DOZEN = set(range(13, 25))
THIRD_DOZEN = set(range(25, 37))

FIRST_COLUMN = set(range(1, 37, 3))
SECOND_COLUMN = set(range(2, 37, 3))
THIRD_COLUMN = set(range(3, 37, 3))

STRAIGHTS = {}
for pocket in range(37):
    STRAIGHTS[pocket] = {pocket}

TABLE_ROWS = []
for first in range(1, 37, 3):
    TABLE_ROWS.append([first, first + 1, first + 2])

SPLITS = {}
for pockets in TABLE_ROWS[0]:
    SPLITS[(0, pocket)] = {0, pocket}

STREETS = {}
CORNERS = {}
SIX_LINES = {}

for row in TABLE_ROWS:
    STREETS[row[0]] = set(row)
    for column in range(2):
        left = row[column]
        right = row[column + 1]
        SPLITS[(left, right)] = {left, right}

for row_index in range(len(TABLE_ROWS) - 1):
    top_row = TABLE_ROWS[row_index]
    bottom_row = TABLE_ROWS[row_index + 1]
    SIX_LINES[top_row[0]] = set(top_row + bottom_row)

    for column in range(3):
        above = top_row[column]
        below = bottom_row[column]
        SPLITS[(above, below)] = {above, below}

    for column in range(2):
        top_left = top_row[column]
        top_right = top_row[column + 1]
        bottom_left = bottom_row[column]
        bottom_right = bottom_row[column + 1]
        CORNERS[top_left] = {top_left, top_right, bottom_left, bottom_right}

STARTING_BALANCE = 100

HELP = """bet <chips> <type> [numbers]
Examples: bet 5 red, bet 10 straight 17, bet 10 split 17 20
Other types: black, even, odd, low, high, dozen 1–3, column 1–3
For street and six-line, use the first number in the first row.
For corner, use the smallest number it covers (e.g. corner 16).
Commands: spin, clear, help, quit"""


def spin():
    return random.randrange(37)


def settle_bet(pocket, bet, stake):
    winning_pockets, payout = bet
    if pocket in winning_pockets:
        return payout * stake
    return -stake


def build_bets():
    bets = {
        "red": (RED.copy(), 1),
        "black": (BLACK.copy(), 1),
        "even": (EVEN.copy(), 1),
        "odd": (ODD.copy(), 1),
        "low": (LOW.copy(), 1),
        "high": (HIGH.copy(), 1),
        "dozen 1": (FIRST_DOZEN.copy(), 2),
        "dozen 2": (SECOND_DOZEN.copy(), 2),
        "dozen 3": (THIRD_DOZEN.copy(), 2),
        "column 1": (FIRST_COLUMN.copy(), 2),
        "column 2": (SECOND_COLUMN.copy(), 2),
        "column 3": (THIRD_COLUMN.copy(), 2),
    }

    unique_bets = (
        ("straight", STRAIGHTS, 35),
        ("street", STREETS, 11),
        ("corner", CORNERS, 8),
        ("six-line", SIX_LINES, 5),
    )

    for bet_type, selections, payout in unique_bets:
        for number, pockets in selections.items():
            bets[f"{bet_type} {number}"] = (pockets.copy(), payout)

    for (first, second), pockets in SPLITS.items():
        bets[f"split {first} {second}"] = (
            pockets.copy(),
            17,
        )  # 17 is payout for splits

    return bets
