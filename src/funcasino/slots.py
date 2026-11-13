import random
import sys
import threading
import time
from funcasino.wallet import Wallet

LINE = " " + "─" * 39
TITLE = " ♠ ♥ ♦ ♣        S L O T S        ♣ ♦ ♥ ♠"

def wait_for_enter(stop):
    input()
    stop.set()

class Slots:
    SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎"]
    WEIGHTS = [50, 25, 13, 8, 4]
    NEAR_WEIGHTS = [30, 20, 15, 15, 20]
    PAYOUTS = {"🍒": 5, "🍋": 10, "🔔": 15, "⭐": 25, "💎": 64}

    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0
        self.money_lost = 0
        self.rescue_used = False

    def spin(self, weights=None):
        return random.choices(self.SYMBOLS, weights=weights or self.WEIGHTS, k=3)

    def spin_grid(self):
        return [self.spin(self.NEAR_WEIGHTS), self.spin(), self.spin(self.NEAR_WEIGHTS)]

    def payout(self, result, bet):
        if bet <= 0:
            raise ValueError("bet must be positive")

        if len(set(result)) == 1:
            return bet * self.PAYOUTS[result[0]]

        if result[0] == result[1] == "🍒":
            return bet // 2

        return 0

    def is_near_miss(self, grid):
        return sum(row.count("💎") for row in grid) >= 2

    def estimate_rtp(self, spins=100000):
        total = sum(self.payout(self.spin(), 100) for _ in range(spins))
        return total / (spins * 100)

    def draw_grid(self, grid):
        top, middle, bottom = grid
        print("              " + "   ".join(top))
        print("           ┌" + "─" * 16 + "┐")
        print("           │  " + "   ".join(middle) + "  │")
        print("           └" + "─" * 16 + "┘")
        print("              " + "   ".join(bottom))

    def animate_spin(self, grid):
        print()
        print(TITLE)
        print(LINE)
        print("   Press Enter to stop the reels!")

        stop = threading.Event()
        threading.Thread(target=wait_for_enter, args=(stop,), daemon=True).start()

        while not stop.is_set():
            self.draw_grid(self.spin_grid())
            sys.stdout.flush()
            time.sleep(0.08)
            sys.stdout.write("\033[5F")

        sys.stdout.write("\033[F")
        self.draw_grid(grid)
        print(LINE)

    def play_round(self, bet, animate=True):
        all_in = bet == self.wallet.balance
        self.wallet.withdraw(bet)
        grid = self.spin_grid()

        if all_in and not self.rescue_used:
            grid[1] = ["🍋", "🍋", "🍋"]
            self.rescue_used = True

        result = grid[1]

        if animate:
            self.animate_spin(grid)
        winnings = self.payout(result, bet)
        self.wallet.deposit(winnings)

        if winnings >= bet:
            self.wins += 1
            print(f"   🎉 You won ${winnings}!")
        elif winnings > 0:
            self.losses += 1
            self.money_lost += bet - winnings
            print(f"   🎉 WINNER! You won ${winnings}!")
        else:
            self.losses += 1
            self.money_lost += bet
            print(f"   You lost ${bet}.")

        if winnings < bet and self.is_near_miss(grid):
            print("   💎 So close to the jackpot!")

        return result, winnings

    def spin_mode(self):
        while self.wallet.balance > 0:
            bet = input(f"   Balance: ${self.wallet.balance}. Enter bet (q to go back): $")
            if bet == "q":
                return
                
            if not bet.isdigit() or not self.wallet.can_afford(int(bet)):
                print("   Invalid bet.")
                continue

            self.play_round(int(bet))

    def show_menu(self):
        print()
        print(TITLE)
        print(LINE)
        print(f"   Balance: ${self.wallet.balance}")
        print()
        print("   1 ▸ Spin           2 ▸ Stats")
        print("                      3 ▸ Quit")
        print(LINE)

    def show_stats(self):
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total else 0
        print()
        print(" ♠ ♥ ♦ ♣        S T A T S        ♣ ♦ ♥ ♠")
        print(LINE)
        print(f"   Wins: {self.wins}")
        print(f"   Losses: {self.losses}")
        print(f"   Money lost: ${self.money_lost}")
        print(f"   Win rate: {win_rate:.1f}%")
        print(f"   Balance: ${self.wallet.balance}")
        print(f"   Machine payback: {self.estimate_rtp():.0%}")
        print(LINE)

    def play(self):
        while self.wallet.balance > 0:
            self.show_menu()
            choice = input("   Select an option: ")

            if choice == "1":
                self.spin_mode()
            elif choice == "2":
                self.show_stats()
                input("   Press q to go back: ")
            elif choice == "3":
                break
            else:
                print("   Invalid option.")



if __name__ == "__main__":
    Slots().play()