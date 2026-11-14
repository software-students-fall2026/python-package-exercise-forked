from collections import deque
from funcasino.deck import Deck
from funcasino.wallet import Wallet
from funcasino.card_art import render_battle, render_cards
import sys
import time

RANK_ORDER = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
FRAME_HEIGHT = 9

class War:
    def __init__(self, wallet=None, hand_size=10, max_battles=20):
        self.wallet = wallet or Wallet()
        self.hand_size = hand_size
        self.max_battles = max_battles
        self.player_hand = deque()
        self.dealer_hand = deque()
        self.delay = 1.0
        self.drawn = False

    def card_value(self, card):
        return RANK_ORDER.index(card.rank)

    def deal_hands(self):
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.drawn = False

        self.deck = Deck()
        self.deck.shuffle()

        for _ in range(self.hand_size):
            self.player_hand.append(self.deck.deal())
            self.dealer_hand.append(self.deck.deal())

    def show(self, pc, dc, message):
        if self.drawn:
            sys.stdout.write(f"\033[{FRAME_HEIGHT}A")
        print(render_battle(pc, dc))
        print(f"\033[K{message}")
        self.drawn = True
        time.sleep(self.delay)

    def battle(self, verbose=False):
        p, d = self.player_hand, self.dealer_hand
        pot = []
        # game only ends if someone runs out of cards
        # person who has no cards left is the loser
        while p and d:
            pc, dc = p.popleft(), d.popleft()
            pot += [pc, dc]
            pv, dv = self.card_value(pc), self.card_value(dc)

            if pv != dv:
                winner = p if pv > dv else d
                # add won cards to player's hand
                winner.extend(pot)
                name = "Player" if pv > dv else "Dealer"
                if verbose:
                    self.show(pc, dc, f"{name} takes {len(pot)} cards  (Player: {len(p)} | Dealer: {len(d)})")
                return name.lower()

            if verbose:
                self.show(pc, dc, "WAR! Each side burns 3 cards...")
            for _ in range(3):
                if len(p) > 1: pot.append(p.popleft())
                if len(d) > 1: pot.append(d.popleft())

        if p or d:
            (p if p else d).extend(pot)
        return None

    def simulate(self, verbose=False):
        self.deal_hands()
        for _ in range(self.max_battles):
            if not self.player_hand or not self.dealer_hand:
                break
            self.battle(verbose)

        p, d = len(self.player_hand), len(self.dealer_hand)
        if p > d:
            return "player"
        if d > p:
            return "dealer"
        return "tie"

    PAYOUTS = {"player": 1, "dealer":1, "tie":8}

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"Balance: ${self.wallet.balance}. Enter bet: $"))
                if self.wallet.can_afford(bet):
                    self.wallet.withdraw(bet)
                    return bet
                print("Invalid bet amount.")
            except ValueError:
                print("Please enter a valid number.")

    def choose_side(self):
        choice = input("Bet on (player / dealer / tie): ").lower()
        while choice not in self.PAYOUTS:
            choice = input("Please enter player, dealer, or tie: ").lower()
        return choice

    def payout(self, choice, result, bet):
        if choice != result:
            return 0
        return bet + bet * self.PAYOUTS[choice]

    def play_round(self):
        bet = self.place_bet()
        choice = self.choose_side()

        print()
        result = self.simulate(verbose=True)

        print(f"\nFinal count - Player: {len(self.player_hand)} | Dealer: {len(self.dealer_hand)}")
        print(f"Result: {result.upper()}")

        winnings = self.payout(choice, result, bet)
        self.wallet.deposit(winnings)
        if winnings:
            print(f"You won ${winnings - bet}!")
        else:
            print(f"You lost ${bet}.")