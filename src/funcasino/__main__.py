from funcasino.wallet import Wallet
from funcasino.slots import Slots
from funcasino.cointoss import CoinToss
from funcasino.craps import Craps
# from funcasino.blackjack import Blackjack

LINE = " " + "─" * 39

def show_menu(balance):
    print()
    print(" ♠ ♥ ♦ ♣   F U N   C A S I N O   ♣ ♦ ♥ ♠")
    print(LINE)
    print(f"   Balance: ${balance}")
    print()
    print("   1 ▸ Slots          2 ▸ Coin Toss")
    print("   3 ▸ Craps          4 ▸ Blackjack")
    print("                      Q ▸ Quit")
    print(LINE)

def main():
    wallet = Wallet(100)
    games = {
        "1": lambda : Slots(wallet).play(),
        "2": lambda: CoinToss(wallet).play(),
        "3": lambda: Craps(wallet).play(),
        # "4": lambda: Blackjack(wallet).play(),
    }

    while wallet.balance > 0:
        show_menu(wallet.balance)
        choice = input("   Choose a game: ").lower()
        if choice == "q":
            break
        if choice in games:
            games[choice]()
        else:
            print("   Please enter a valid option.")

    if wallet.balance <= 0:
        print("Thank you for your generous donation to the house!")

if __name__ == "__main__":
    main()