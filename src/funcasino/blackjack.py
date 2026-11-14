from funcasino.wallet import Wallet
from funcasino.deck import Deck
import time
import os

class Blackjack:
    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.max_hands = 4

    def hand_value(self, hand):
        total = sum(card.blackjack_value() for card in hand)
        aces = sum(card.rank == "A" for card in hand)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def display_table(self, dealer_hand, hands, active_index=None, reveal_dealer=False):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n--- Dealer ---")

        if reveal_dealer:
            for card in dealer_hand:
                print(card)
            print("Dealer Value:", self.hand_value(dealer_hand))
        else:
            print(dealer_hand[0])
            print("Unknown")
        
        for index, hand in enumerate(hands):
            mark = ""
            if index == active_index:
                mark = "(Current hand)"

            print(f"\n--- Player Hand {index + 1}{mark} ---")
            for card in hand["cards"]:
                print(card)
            
            print("Player Value:", self.hand_value(hand["cards"]))
            print(f"Bet: ${hand['bet']}")
            print("Status:", hand["status"])

    def get_bet(self):
        while True:
            bet = input(f"Current Balance: ${self.wallet.balance}. Enter your bet: $")

            if not bet.isdigit():
                print("Invalid bet.")
                continue
            bet = int(bet)

            if bet <= 0 or not self.wallet.can_afford(bet):
                print("Invalid bet.")
                continue

            self.wallet.withdraw(bet)
            break
        
        return bet

    def can_split(self, hand, hands):
        cards = hand["cards"]
        status = hand["status"]
        bet = hand["bet"]

        return (
            status == "Playing"
            and len(cards) == 2
            and cards[0].blackjack_value() == cards[1].blackjack_value()
            and len(hands) < self.max_hands
            and self.wallet.can_afford(bet)
        )
    
    def split_hand(self, hands, index, deck):
        hand = hands[index]
        first_card = hand["cards"][0]
        second_card = hand["cards"][1]
        bet = hand["bet"]

        self.wallet.withdraw(bet)

        status = ""
        if first_card.rank == "A":
            status = "Standing"
        else:
            status = "Playing"

        hands[index] = {
            "cards": [first_card, deck.deal()],
            "bet": bet,
            "status": status
        }

        hands.insert(index + 1, {
            "cards": [second_card, deck.deal()],
            "bet": bet,
            "status": status
        })

        print(f"\n Player Hand {index + 1} split. The additional bet is ${bet}.")
    
    def check_for_blackjack(self, dealer_hand, hands):
        hand = hands[0]
        player_blackjack = self.hand_value(hand["cards"]) == 21
        dealer_blackjack = self.hand_value(dealer_hand) == 21

        if not player_blackjack and not dealer_blackjack:
            return False
        else: 
            self.display_table(dealer_hand, hands, reveal_dealer=True)

        if player_blackjack and dealer_blackjack:
            print("\nBoth player and dealer have blackjack. Push.")
            self.pushes += 1
            self.wallet.deposit(hand["bet"])
        elif player_blackjack:
            print("\nBlackjack! You win.")
            self.wins += 1
            self.wallet.deposit(hand["bet"] * 2.5)
        else:
            print("\nDealer has blackjack. You lose!")
            self.losses += 1

        return True
    
    def play_player_hands(self, dealer_hand, hands, deck):
        index = 0

        while index < len(hands):
            hand = hands[index]

            if hand["status"] != "Playing":
                index += 1
                continue
                
            value = self.hand_value(hand["cards"])

            if value >= 21:
                hand["status"] = "Bust" if value > 21 else "Standing"
                self.display_table(dealer_hand, hands, index)
                index += 1
                continue

            self.display_table(dealer_hand, hands, index)

            print("\nWhat do you choose to do?")
            print("1. Hit")
            print("2. Stand")
            if self.can_split(hand, hands):
                print("3. Split")
    
            choice = input("Select an option: ")
            if choice == "1":
                hand["cards"].append(deck.deal())
            elif choice == "2":
                hand["status"] = "Standing"
                index += 1
            elif choice == "3" and self.can_split(hand, hands):
                self.split_hand(hands, index, deck)
            else:
                print("Invalid option.")
            
    def play_dealer_hand(self, dealer_hand, hands, deck):
        if all(self.hand_value(hand["cards"]) > 21 for hand in hands):
            self.display_table(dealer_hand, hands, reveal_dealer=True)
            return
        
        while True:
            self.display_table(dealer_hand, hands, reveal_dealer=True)
            time.sleep(1.5)

            value = self.hand_value(dealer_hand)
            if value > 21:
                print("\nDealer busts!")
                return
            if value >= 17:
                print("\nDealer stands.")
                return
            print("\nDealer hits.")
            time.sleep(1)
            dealer_hand.append(deck.deal())

    def settle_all_hands(self, dealer_hand, hands):
        dealer_value = self.hand_value(dealer_hand)

        for index, hand in enumerate(hands):
            value = self.hand_value(hand["cards"])
            bet = hand["bet"]
            print(f"\nPlayer Hand {index + 1} ({value}):")

            if value > 21:
                print("Bust! You lose.")
                self.losses += 1
                hand["status"] = "Lost"
            elif dealer_value > 21 or value > dealer_value:
                print("You win.")
                self.wins += 1
                self.wallet.deposit(bet * 2)
                hand["status"] = "Won"
            elif value < dealer_value:
                print("Dealer wins.")
                self.losses += 1
                hand["status"] = "Lost"
            else:
                print("Both hands equal. Push.")
                self.pushes += 1
                self.wallet.deposit(bet)
                hand["status"] = "Push"

    def play_round(self):
        bet = self.get_bet()

        deck = Deck(8)
        deck.shuffle()

        dealer_hand = [deck.deal(), deck.deal()]
        hands = [{
            "cards": [deck.deal(), deck.deal()],
            "bet": bet,
            "status": "Playing"
        }]

        if self.check_for_blackjack(dealer_hand, hands):
            return

        self.play_player_hands(dealer_hand, hands, deck)
        self.play_dealer_hand(dealer_hand, hands, deck)
        self.settle_all_hands(dealer_hand, hands)

    def show_stats(self):
        total = self.wins + self.losses + self.pushes
        win_rate = (self.wins / total * 100) if total else 0

        print(f"\nWins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Pushes: {self.pushes}")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Balance: ${self.wallet.balance}")

    def play(self):
        while self.wallet.balance > 0:
            print("\n--- BLACKJACK ---")
            print("1. Play")
            print("2. View Stats")
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
        
        print("\nYou ran out of money. Thanks for playing!")
        print("Here are your final stats!")
        self.show_stats()

if __name__ == "__main__":
    Blackjack().play()