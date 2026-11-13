from funcasino.wallet import Wallet
from funcasino.deck import Deck
import time

class Blackjack:
    def __init__(self, wallet=None):
        self.wallet = wallet or Wallet()
        self.wins = 0
        self.losses = 0

    def hand_value(self, hand):
        total = sum(card.blackjack_value() for card in hand)
        aces = sum(card.rank == "A" for card in hand)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def play_round(self):
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

        deck = Deck(8)
        deck.shuffle()
        dealer_hand = [deck.deal(), deck.deal()]
        player_hand = [deck.deal(), deck.deal()]
        dealer_card_value = 0
        player_card_value = 0
        player_turn = True
        dealer_turn = False

        while player_turn:
            player_card_value = self.hand_value(player_hand)

            print("\nDealer's hand:")
            print(dealer_hand[0])
            print("Unknown")

            print("\nPlayer's hand:")
            for card in player_hand:
                print(card)
            print("Player card value:", player_card_value)

            if player_card_value == 21:
                player_turn = False
                dealer_turn = True
            elif player_card_value > 21:
                self.losses += 1
                print("You bust!")
                break
            else:
                print("\nWhat do you choose to do?")
                print("1. Hit")
                print("2. Stand")
                choice = input("Select an option: ")
                if choice == "1":
                    player_hand.append(deck.deal())
                elif choice == "2":
                    player_turn = False
                    dealer_turn = True
                else:
                    print("Invalid option.")
        
        while dealer_turn:
            dealer_card_value = self.hand_value(dealer_hand)

            print("\nDealer's hand:")
            for card in dealer_hand:
                print(card)
            print("Dealer card value:", dealer_card_value)

            print("\nPlayer's hand:")
            for card in player_hand:
                print(card)
            print("Player card value:", player_card_value)

            time.sleep(1.5)
            
            if dealer_card_value < 17:
                print("\nDealer hits...")
                time.sleep(1)
                dealer_hand.append(deck.deal())
            else:
                dealer_turn = False
                
                if dealer_card_value > 21:
                    print("\nDealer busts! You win!")
                    self.wins += 1
                    self.wallet.deposit(bet * 2)
                elif player_card_value > dealer_card_value:
                    print("\nYou win!")
                    self.wins += 1
                    if player_card_value == 21:
                        self.wallet.deposit(bet * 2.5)
                    else:
                        self.wallet.deposit(bet * 2)
                elif player_card_value < dealer_card_value:
                    print("\nDealer wins!")
                    self.losses += 1
                else:
                    print("\nPush! Your bet is returned.")
                    self.wallet.deposit(bet)

    def show_stats(self):
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total else 0

        print(f"\nWins: {self.wins}")
        print(f"Losses: {self.losses}")
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