from collections import deque
from funcasino.deck import Deck
from funcasino.wallet import Wallet

RANK_ORDER = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

class War:
    def __init__(self, wallet=None, hand_size=10, max_battles=30):
        self.wallet = wallet or Wallet()
        self.hand_size = hand_size
        self.max_battles = max_battles

    def card_value(self, card):
        return RANK_ORDER.index(card.rank)