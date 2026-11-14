import random

SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9",
         "10", "J", "Q", "K", "A")

class Card:
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError(f"Invalid rank: {rank!r}")
        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit!r}")
        self.rank = rank
        self.suit = suit

    def blackjack_value(self):
        if self.rank == "A":
            return 11
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, num_decks=1):
        if not isinstance(num_decks, int):
            raise TypeError("Number of decks must be an integer.")
        if num_decks < 1:
            raise ValueError("Number of decks must be at least 1.")
        self.cards = []
        self.num_decks = num_decks
        for i in range(num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit))
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError("The deck is empty.")
        return self.cards.pop()
    
    def size(self):
        return len(self.cards)