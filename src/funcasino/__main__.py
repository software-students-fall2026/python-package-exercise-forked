from funcasino.wallet import Wallet
from funcasino.slots import Slots
from funcasino.cointoss import CoinToss
from funcasino.craps import Craps
from funcasino.blackjack import Blackjack
from funcasino.war import War
from funcasino.roulette import Roulette
from funcasino.stats import show_stats

LINE = " " + "─" * 39

def show_menu(balance):
    print()
    print(" ♠ ♥ ♦ ♣   F U N   C A S I N O   ♣ ♦ ♥ ♠")
    print(LINE)
    print(f"   Balance: ${balance}")
    print()
    print("   1 ▸ Slots          2 ▸ Coin Toss")
    print("   3 ▸ Craps          4 ▸ Blackjack")
    print("   5 ▸ War           6 ▸ Roulette")
    print("   7▸ Stats          Q ▸ Quit")
    print(LINE)

def main():
    wallet = Wallet(100)
    slots = Slots(wallet)
    cointoss = CoinToss(wallet)
    craps = Craps(wallet)
    blackjack = Blackjack(wallet)
    war = war(wallet)
    #roulette = Roulette(wallet)

    games = {
        "1": slots.play,
        "2": cointoss.play,
        "3": craps.play,
        "4": blackjack.play,
        "5": War.play_round,
        #"5": roulette.play,
    }

    game_stats = {
    "Slots": slots,
    "Coin Toss": cointoss,
    "Craps": craps,
    "Blackjack": blackjack,
    "War": war,
    #"Roulette": roulette,
    }

    while wallet.balance > 0:
        show_menu(wallet.balance)
        choice = input("   Choose a game: ").lower()
        if choice == "q":
            break
        if choice in games:
            games[choice]()
        elif choice == "6":
            show_stats(game_stats, wallet)
            input("   Press Enter to continue: ")
        else:
            print("   Please enter a valid option.")

    show_stats(game_stats, wallet)
    if wallet.balance <= 0:
        print("Thank you for your generous donation to the house!")

if __name__ == "__main__":
    main()