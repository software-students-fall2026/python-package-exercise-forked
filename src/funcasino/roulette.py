import random

class Roulette:
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

    def __init__(self, starting_balance = STARTING_BALANCE):
        if type(starting_balance) is not int or starting_balance < 0:
            raise ValueError("Starting balance must be a nonnegative whole number.")
        self.balance = starting_balance
        self._bets = self.build_bets()
        self._pending_bets = []

    def available_chips(self):
        available = self.balance
        for _, stake in self._pending_bets:
            available -= stake
        return available

    def place_bet(self, name, stake):
        if type(stake) is not int:
            raise ValueError("Enter the stake as a whole number of chips.")
        available = self.available_chips()
        if not 1 <= stake <= available:
            if available == 0:
                raise ValueError("No chips available.")
            raise ValueError(f"You can stake 1 to {available} chips.")

        words = name.lower().split()
        if not words:
            raise ValueError("Enter a bet type.")
        bet_type = words[0]
        numbers = []
        try:
            for word in words[1:]:
                numbers.append(int(word))
        except ValueError:
            raise ValueError("Enter the bet's number as whole numbers.") from None
        if bet_type == "split":
            numbers.sort()

        name_parts = [bet_type]
        for number in numbers:
            name_parts.append(str(number))
        bet_name = " ".join(name_parts)
        if bet_name not in self._bets:
            raise ValueError("That bet is unavailable. Type 'help' for legal bets and examples")
        self._pending_bets.append((bet_name, stake))

    def clear_bets(self):
        self._pending_bets.clear()

    def spin(self):
        if not self._pending_bets:
            raise ValueError("Place at least one bet before spinning.")

        pocket = random.randrange(37)
        results = []

        for name, stake in self._pending_bets:
            winning_pockets, payout = self._bets[name]
            if pocket in winning_pockets:
                change = payout * stake
            else:
                change = -stake
            self.balance += change
            results.append((name, change))
        self.clear_bets()
        return pocket, results

    def build_bets(self):
        bets = {
            "red": (self.RED.copy(), 1),
            "black": (self.BLACK.copy(), 1),
            "even": (self.EVEN.copy(), 1),
            "odd": (self.ODD.copy(), 1),
            "low": (self.LOW.copy(), 1),
            "high": (self.HIGH.copy(), 1),
            "dozen 1": (self.FIRST_DOZEN.copy(), 2),
            "dozen 2": (self.SECOND_DOZEN.copy(), 2),
            "dozen 3": (self.THIRD_DOZEN.copy(), 2),
            "column 1": (self.FIRST_COLUMN.copy(), 2),
            "column 2": (self.SECOND_COLUMN.copy(), 2),
            "column 3": (self.THIRD_COLUMN.copy(), 2),
        }

        unique_bets = (
            ("straight", self.STRAIGHTS, 35),
            ("street", self.STREETS, 11),
            ("corner", self.CORNERS, 8),
            ("six-line", self.SIX_LINES, 5),
        )

        for bet_type, selections, payout in unique_bets:
            for number, pockets in selections.items():
                bets[f"{bet_type} {number}"] = (pockets.copy(), payout)

        for (first, second), pockets in self.SPLITS.items():
            bets[f"split {first} {second}"] = (
                pockets.copy(),
                17,
            )  # 17 is payout for splits

        return bets


    def parse_bet(self, words):
        if len(words) < 1:
            raise ValueError("Use 'bet <chips> <type> [numbers]'. Type 'help' for examples.")

        try:
            stake = int(words[1])
        except ValueError:
            raise ValueError("Enter the stake as a whole number of chips") from None
        return " ".join(words[2:]), stake

    def print_spin(self, pocket, results):
        if pocket == 0:
            color = "green"
        elif pocket in self.RED:
            color = "red"
        else:
            color = "black"
        print(f"Spin: {pocket} ({color})")

        for name, change in results:
            print(f"{name}: {change:+d}")
        print(f"Balance: {self.balance}")

    def run(self):
        print("Type 'help' for commands.")

        while self.balance > 0:
            available = self.available_chips()

            try:
                words = input(f"{available} chips available > ").lower().split()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not words:
                continue
            if words == ["quit"]:
                break
            if words == ["help"]:
                print(self.HELP)
            elif words == ["clear"]:
                self.clear_bets()
                print("Pending bets cleared")
            elif words[0] == "bet":
                try:
                    name, stake = self.parse_bet(words)
                    self.place_bet(name, stake)
                except ValueError as error:
                    print(error)
            elif words == ["spin"]:
                try:
                    pocket, results = self.spin()
                except ValueError as error:
                    print(error)
                    continue
                self.print_spin(pocket, results)
            else:
                print("Unknown command. Type 'help' for available commands.")

        print(f"final balance: {self.balance} chips.")

if __name__ == "__main__":
    Roulette().run()