SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠",
}

CARD_BACK = (
    "┌─────────┐",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "└─────────┘",
)


def card_lines(card):
    """Return the ASCII art for a card as a tuple of 7 strings, all the same width."""
    suit = SUIT_SYMBOLS[card.suit]
    rank = card.rank  # "10" is 2 characters wide, so pad it with ljust/rjust
    return (
        "┌─────────┐",
        f"│ {rank.ljust(2)}      │",
        "│         │",
        f"│    {suit}    │",
        "│         │",
        f"│      {rank.rjust(2)} │",
        "└─────────┘",
    )


def render_cards(*cards, gap="  "):
    """Return several cards side by side as one string.
    Pass None for a card to draw it face down."""
    arts = [CARD_BACK if card is None else card_lines(card) for card in cards]
    return "\n".join(gap.join(art[row] for art in arts) for row in range(len(CARD_BACK)))


def render_battle(player_card, dealer_card):
    """Return the player's card vs the dealer's card, with labels above them."""
    width = len(CARD_BACK[0])
    left, right = card_lines(player_card), card_lines(dealer_card)
    middle = len(left) // 2
    rows = ["Player".center(width) + "        " + "Dealer".center(width)]
    for i in range(len(left)):
        gap = "   vs   " if i == middle else "        "
        rows.append(left[i] + gap + right[i])
    return "\n".join(rows)
