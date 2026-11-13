import random
from funcasino.wallet import Wallet
import sys
import time

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"),
    2: ("┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"),
    3: ("┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"),
    4: ("┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"),
    5: ("┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"),
    6: ("┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘")
}


class Craps:
    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0

    def print_dice(self, dice1, dice2):
        # these are all for the animation
        for i in range(5):
            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            for line in range(5):
                print(dice_art[d1][line] + "  " + dice_art[d2][line])
            sys.stdout.write("\033[5A")         # moves the cursor back up 5 lines each time so the dice animate in place
            time.sleep(0.1 + i * 0.01)

        #prints the actual result
        for line in range(5):
            print(dice_art[dice1][line] + "  " + dice_art[dice2][line])
            
    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.print_dice(dice1, dice2)
        return dice1, dice2, dice1 + dice2

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"Balance: ${self.wallet.balance}. Enter bet: $"))

                if 0 < bet <= self.wallet.balance:
                    self.wallet.withdraw(bet)
                    return bet

                print("Invalid bet amount.")

            except ValueError:
                print("Please enter a valid number.")

    def play_round(self):
        bet = self.place_bet()

        input("Press Enter to roll the dice!")
        dice1, dice2, sum1 = self.roll_dice()
        print(f"Your total is {sum1}")

        #first round, either 2x, 0x, or advances
        if sum1 in (7, 11):
            self.wallet.deposit(2*bet)
            self.wins+=1
            print(f"Natural {sum1}! You won ${2*bet}!")
            return
        elif sum1 in (2, 3, 12):
            self.losses+=1
            print(f"Craps ({sum1})! You lost ${bet}!")
            return

        point = sum1
        print(f"Your point is now: {point}. Try to hit {point} before rolling a 7!")

        #second round, multipliers based on how hard it is to get your number
        if sum1 in (4,10):
            multiplier = 3 
        elif sum1 in (5,9):
            multiplier = 2.5
        else:
            multiplier = 2.2
        
        print(f"Want to place an extra bet on {point}?")
        print(f"If you win, your extra bet pay out {multiplier}x and added on top of your original payout!")
        decision = input("[Y/N]: ")
        decision = decision.strip().lower()

        while decision not in ["y", "n"]:
            decision = input("Please enter 'y' or 'n' to make your decision: ")
            decision = decision.strip().lower()

        if decision == "y":
            if self.wallet.balance == 0:
                print ("You have no money to add!")
                extra = False
            else:
                extra = True
                extra_bet = self.place_bet()
        else:
            extra = False

        while True:
            input("Press Enter to roll again!")
            dice1, dice2, sum2 = self.roll_dice()

            if sum2 == point:
                self.wins+=1
                if extra == True:
                    payout = round(2*bet+multiplier*extra_bet)
                    self.wallet.deposit(payout)
                    print(f"You rolled {dice1} and {dice2} ({sum2}) , Since you bet extra and you hit your number! You won ${payout}!")
                else:
                    self.wallet.deposit(2*bet)
                    print(f"You rolled {dice1} and {dice2} ({sum2}) , You hit your number! You won ${2*bet}!")
                return

            if sum2 == 7:
                self.losses+=1
                if extra == True:
                    print(f"You rolled {dice1} and {dice2} (7) , You sevened out unfortunately. You lost ${bet+extra_bet}!")
                else:
                    print(f"You rolled {dice1} and {dice2} (7) , You sevened out unfortunately. You lost ${bet}!")
                return

            print(f"You rolled {sum2} ({dice1} and {dice2}), not {point} or 7. Rerolling...")
    
    def show_stats(self):
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total else 0
        print("\n--- CRAPS STATS ---")
        print(f"Wins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Balance: ${self.wallet.balance}")
        input("Press Enter to exit: ")

    def play(self):
        while self.wallet.balance > 0:
            print("\n--- CRAPS ---")
            print("1. Play")
            print("2. Stats")
            print("3. Quit")
            choice = input("Select an option: ")

            if choice == "1":
                self.play_round()
            elif choice == "2":
                self.show_stats()
            elif choice == "3":
                break
            else:
                print("Invalid option.")

        print("Thanks for playing! Here are your final stats:")
        self.show_stats()


if __name__ == "__main__":
    game = Craps()
    game.play()