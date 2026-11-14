from collections import deque
from funcasino.deck import Deck
from funcasino.wallet import Wallet
from funcasino.card_art import render_battle, render_cards
import sys
import time

RANK_ORDER = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
FRAME_HEIGHT = 9

class War:
    def __init__(self, wallet=None, hand_size=10, max_battles=30):
        self.wallet = wallet or Wallet()
        self.hand_size = hand_size
        self.max_battles = max_battles
        self.player_hand = deque()
        self.dealer_hand = deque()
        self.delay = 0.6
        self.drawn = False

    def card_value(self, card):
        return RANK_ORDER.index(card.rank)

    def deal_hands(self):
        self.deck = Deck()
        self.deck.shuffle()
        for _ in range(self.hand_size):
            self.player_hand.append(self.deck.deal())
            self.dealer_hand.append(self.deck.deal())

    def show(self, pc, dc, message):
        ...
    def battle(self, p, d):
        ...