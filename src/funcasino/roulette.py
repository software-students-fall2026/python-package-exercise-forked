import random
from funcasino.wallet import Wallet, InsufficientFunds

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
    for pocket in TABLE_ROWS[0]:
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

    BET_MENU = (
        ("Red or black", "", "Enter red or black: "),
        ("Even or odd", "", "Enter even or odd: "),
        ("Low or high", "", "Enter low (1–18) or high (19–36): "),
        ("Dozen", "dozen", "Enter 1 (1–12), 2 (13–24), or 3 (25–36): "),
        ("Column", "column", "Enter 1 (1, 4, …), 2 (2, 5, …), or 3 (3, 6, …): "),
        ("Straight", "straight", "Enter one pocket (0–36): "),
        ("Split", "split", "Enter two neighboring pockets, e.g. 17 20: "),
        ("Street", "street", "Enter the first number of the row, e.g. 16: "),
        ("Corner", "corner", "Enter the smallest of the four numbers, e.g. 16: "),
        (
            "Six line",
            "six-line",
            "Enter the first number of two neighboring rows, e.g. 16: ",
        ),
    )

    HELP = (
        "\n--- ROULETTE RULES & PAYOUTS ---\n"
        "Place one or more bets, then spin. Every bet uses the same winning pocket.\n"
        "The wheel has pockets 0–36. Green 0 loses all outside bets.\n"
        "Payouts below show profit per $1 wagered.\n\n"
        "Red/black, even/odd, low/high   1 to 1\n"
        "Dozen or column               2 to 1\n"
        "Straight (one pocket)        35 to 1\n"
        "Split (two neighbors)        17 to 1\n"
        "Street (one row of three)    11 to 1\n"
        "Corner (two by two)           8 to 1\n"
        "Six line (two full rows)      5 to 1\n\n"
        "The betting table starts with 1 2 3, then 4 5 6, and so on.\n"
        "For example, 16 17 18 sit directly above 19 20 21.\n"
        "Zero can be bet straight or split with 1, 2, or 3."
    )

    def __init__(self, starting_balance=STARTING_BALANCE, wallet=None):
        if wallet is None:
            if type(starting_balance) is not int or starting_balance < 0:
                raise ValueError("Starting balance must be a nonnegative whole number.")
            wallet = Wallet(starting_balance)
        self.wallet = wallet
        self.wins = 0
        self.losses=0
        self._bets = self.build_bets()
        self._pending_bets = []

    @property
    def balance(self):
        return self.wallet.balance

    def pending_stake(self):
        total = 0
        for _, stake in self._pending_bets:
            total += stake
        return total

    def available_chips(self):
        return max(0, self.balance - self.pending_stake())

    def place_bet(self, name, stake):
        if type(stake) is not int:
            raise ValueError("Enter a whole-dollar bet")
        available = self.available_chips()
        if not 1 <= stake <= available:
            if available == 0:
                raise ValueError("No money available.")
            raise ValueError(f"Enter a bet from $1 to ${available}.")

        bet_name = self.bet_name(name)
        self._pending_bets.append((bet_name, stake))

    def bet_name(self, name):
        words = name.lower().split()
        if not words:
            raise ValueError("Enter a bet type.")
        bet_type = words[0]
        numbers = []
        try:
            for word in words[1:]:
                numbers.append(int(word))
        except ValueError:
            raise ValueError("Enter the bet's numbers as whole numbers.") from None
        if bet_type == "split":
            numbers.sort()

        name_parts = [bet_type]
        for number in numbers:
            name_parts.append(str(number))
        bet_name = " ".join(name_parts)
        if bet_name not in self._bets:
            raise ValueError("Those numbers do not make a valid bet.")
        return bet_name

    def clear_bets(self):
        self._pending_bets.clear()

    def spin(self):
        if not self._pending_bets:
            raise ValueError("Place at least one bet before spinning.")


        total_stake = self.pending_stake()
        if not self.wallet.can_afford(total_stake):
            raise InsufficientFunds(f"Balance is too low for the ${total_stake} on the table.")
        pocket = random.randrange(37)
        results = []
        total_return = 0
        for name, stake in self._pending_bets:
            winning_pockets, payout = self._bets[name]
            if pocket in winning_pockets:
                change = payout * stake
                total_return += stake + change
            else:
                change = -stake
            results.append((name, change))
        self.wallet.withdraw(total_stake)
        if total_return > 0:
            self.wallet.deposit(total_return)
        self.clear_bets()
        # based on profit or loss, says win or los
        net = total_return - total_stake
        if net>0:
            self.wins+=1
        elif net<0:
            self.losses+=1
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

    # def parse_bet(self, words):
    #     if len(words) < 1:
    #         raise ValueError(
    #             "Use 'bet <chips> <type> [numbers]'. Type 'help' for examples."
    #         )

    #     try:
    #         stake = int(words[1])
    #     except ValueError:
    #         raise ValueError("Enter the stake as a whole number of chips") from None
    #     return " ".join(words[2:]), stake

    def print_spin(self, pocket, results):
        if pocket == 0:
            color = "green"
        elif pocket in self.RED:
            color = "red"
        else:
            color = "black"
        print(f"\nThe ball landed on {pocket} ({color.upper()})!")
        for name, change in results:
            if change > 0:
                print(f"{name.title()}: You won ${change}!")
            else:
                print(f"{name.title()}: You lost ${abs(change)}.")
        print(f"Balance: ${self.balance}")

    def prompt_for_bet(self):
        print("\nChoose a bet type (q to go back).")
        for number, (label, _, _) in enumerate(self.BET_MENU, start=1):
            print(f"{number}. {label}")

        while True:
            choice = input("Select a bet type: ").strip().lower()
            if choice == "q":
                return
            try:
                number = int(choice)
            except ValueError:
                print("Invalid option.")
                continue
            if 1 <= number <= len(self.BET_MENU):
                label, bet_type, prompt = self.BET_MENU[number - 1]
                break
            print("Invalid option")

        while True:
            selection = input(prompt).strip().lower()
            if selection == "q":
                return
            if not bet_type and selection not in label.lower().split(" or "):
                print(f"Choose {label.lower()}.")
                continue
            try:
                name = self.bet_name(f"{bet_type} {selection}")
            except ValueError as error:
                print(error)
            else:
                break

        pockets, payout = self._bets[name]
        numbers = []
        for pocket in sorted(pockets):
            numbers.append(str(pocket))
        print(f"{name.title()} covers {', '.join(numbers)} and pays {payout} to 1.")
        while True:
            amount = (
                input(
                    f"Available: ${self.available_chips()}. Enter bet (q to go back): $"
                )
                .strip()
                .lower()
            )
            if amount == "q":
                return
            try:
                stake = int(amount.removeprefix("$"))
            except ValueError:
                print("Enter a whole-dollar bet.")
                continue
            try:
                self.place_bet(name, stake)
            except ValueError as error:
                print(error)
            else:
                return

    def play(self):
        while self.balance > 0:
            print("\n--- ROULETTE TABLE ---")
            available = self.available_chips()
            print(
                f"Available: ${available} | On the table: ${self.balance - available}"
            )
            for name, stake in self._pending_bets:
                print(f"{name.title()}: ${stake}")
            print("1. Place a Bet\n2. Spin\n3. Clear Bets\n4. Back")
            choice = input("Select an option: ").strip().lower()
            if choice == "1":
                if available == 0:
                    print("You have no money left to bet this round.")
                else:
                    self.prompt_for_bet()
            elif choice == "2":
                if not self._pending_bets:
                    print("Place at least one bet before spinning.")
                else:
                    try:
                        pocket, result = self.spin()
                    except InsufficientFunds as error:
                        print(error)
                        continue
                    self.print_spin(pocket, result)
            elif choice == "3":
                self.clear_bets()
                print("Bets cleared.")
            elif choice in ("4", "q"):
                self.clear_bets()
                return
            else:
                print("Invalid option.")

    def run(self):
        try:
            while self.balance > 0:
                print("\n--- ROULETTE ---")
                print(f"Balance: ${self.balance}")
                print("1. Play\n2. Rules & Payouts\n3. Quit")
                choice = input("Select an option: ").strip().lower()
                if choice == "1":
                    self.play()
                elif choice == "2":
                    print(self.HELP)
                elif choice in ("3", "q"):
                    break
                else:
                    print("Invalid option.")
        except (EOFError, KeyboardInterrupt):
            print()
        self.clear_bets()
        print("Thanks for playing!")
        return self.balance


if __name__ == "__main__":
    Roulette().run()