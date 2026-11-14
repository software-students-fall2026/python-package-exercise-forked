[![CI](https://github.com/software-students-fall2026/python-package-exercise-forked/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-forked/actions/workflows/ci.yml)

# Fun Casino

FunCasino is a Python package that simulates some of the most popular casino games, including blackjack, roulette, and slots, for educational purposes.

[PyPI Link](https://pypi.org/project/funcasino/)

## Team Members
- [Shuo Cao](https://github.com/ShuoWu6529)
- [Jack Jiang](https://github.com/jack-k-jiang)
- [Ronald Szeto](https://github.com/ronaldszeto)
- [Eric Wu](https://github.com/ew2725)
- [Ruikun Xu](https://github.com/xuruikun)

## Installation & Contribution

### 0. Prerequisites

- Python 3.15

### 1. Clone repository

Clone a copy of this repository to your local machine from GitHub and open the repository directory.

### 2. Install dependencies and set up virtual environment

After cloning this repository, run `pipenv install --dev` from the main project directory. This creates the project's virtual environment and installs everything listed in the `Pipfile`:

- `[packages]` - what the package itself needs to run. Here, that's just the package itself, installed in "_editable_" mode.
- `[dev-packages]` - tools needed only while developing the package, such as `pytest`, `coverage`, [build](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives), and [twine](https://packaging.python.org/en/latest/key_projects/#twine). The `--dev` flag installs these too.

### 3. Run the program

FunCasino could be run as a program through `pipenv run python -m funcasino`. Each game is also an importable module that can be used in any file after downloading the package.

### 4. Running tests

Simple example unit tests are included within the `tests` directory. To run these tests...

1. Activate the virtual environment, if not yet done, e.g. `pipenv shell`.
2. Install all the project's dependencies, including dev dependencies like `pytest`, into the virtual environment, e.g. `pipenv install --dev`.
3. Run the tests from the main project directory: `python3 -m pytest`.
4. Tests should never fail. Any failed tests indicate that the production code is behaving differently from the behavior the tests expect.

### 5. Build the Package

From the main project directory, run:

```bash
pipenv run python -m build
```

### Contribute

Contributions are always welcome! If there are any bugs or feature suggestions, feel free to open an issue describing it.

To contribute to issues:

1. Fork this repository and clone your fork to your local machine.
2. Follow the installation & setup instructions.
3. Make your changes by fixing an issue or adding a feature (make sure to add or update tests if necessary).
4. Run the tests: `pipenv run python -m pytest`.
5. Build the package: `pipenv run python -m build.`
6. Commit the changes, push them to the forked repository, and open a pull request explaining your changes.

## Documentation

### Blackjack
CLI implementation of blackjack for the `funcasino` package.

#### How It Works

* Place a bet (must be more than $0 and no more than your balance)
* Try to hit 21 or as close to 21 without hitting over as well as having a higher value than the dealer, who will always hit until getting at least 17 in value.
* Each game is played with a set of 8 decks so card counting is very difficult.
* If you have a starting hand with the same card ranks, you could split your hand and bet more money against the dealer with the same hand!
* The game keeps going until you quit or your balance hits $0. Your wins, losses, pushes, and overall win statistics are tracked.

#### Function Descriptions

* `hand_value(hand)`: Returns the card values associated with each card rank
* `display_table(dealer_hand, hands, active_index=None, reveal_dealer=False)`: Displays the table for both the dealer and the player. The dealer will have their second card hidden until it is their turn to play
* `get_bet()`: Returns the bet amount that the player inputs
* `can_split(hand, hands)`: Returns a boolean conditioned on whether a player has all the requirements to split a hand or not
* `split_hand(hands, index, deck)`: Splits a hand by mutating their current hand array
* `check_for_blackjack(dealer_hand, hands)`: Checks both the dealer and player for blackjack to resolve game status early
* `play_player_hands(dealer_hand, hands, deck)`: Plays the player turn in blackjack, asking for inputs for their decisions
* `play_dealer_hand(dealer_hand, hands, deck)`: Plays the dealer turn in blackjack after the player turn
* `settle_all_hands(dealer_hand, hands)`: Settles all the player hands after both the player and dealer have finished playing their hands
* `play_round()`: Creates a hand for both the dealer and player, and starts the game
* `show_stats()`: Prints the wins, losses, pushes, and winrate for the game
* `play()`: Main menu loop

#### Usage

```python
from funcasino.blackjack import Blackjack
from funcasino.wallet import Wallet

game = Blackjack(Wallet(200))
game.play()
```

#### Example Output

```text
--- BLACKJACK ---
1. Play
2. View Stats
3. Quit
Select an option: 1
Current Balance: $100. Enter your bet: $50

--- Dealer ---
Q of Spades
6 of Spades
Dealer Value: 16

--- Player Hand 1 ---
8 of Diamonds
2 of Clubs
3 of Clubs
10 of Hearts
Player Value: 23
Bet: $50
Status: Bust

Player Hand 1 (23):
Bust! You lose.
```

### Coin Toss
CLI implementation of a coin toss game for the `funcasino` package.

#### How It Works

* Place a bet (must be more than $0 and no more than your balance), then call heads or tails.
* Guess correctly and you win your bet (1:1 payout). Guess wrong and you lose your bet.
* The game keeps going until you quit or your balance hits $0. Your wins, losses, and the history of each round are tracked.

#### Function Descriptions

* `CoinToss(wallet=None)`: Creates a new game. Pass in a shared `Wallet` to use the same balance across games, or leave it empty to start with $100.
* `flip_coin()`: Randomly returns `"heads"` or `"tails"`.
* `animate_flip(result)`: Plays a short flipping animation in the terminal that lands on `result`.
* `place_bet()`: Asks for a bet and keeps asking until it's a valid amount.
* `play_round()`: Runs one round: bet, call heads or tails, flip, then update the balance, wins/losses, and `history`.
* `show_stats()`: Prints wins, losses, win rate, and current balance.
* `play()`: Main menu loop (Play / View Stats / Quit).

#### Usage

```python
from funcasino.cointoss import CoinToss
from funcasino.wallet import Wallet

game = CoinToss(Wallet(200))
game.play()
```

#### Example Output

```text
--- COIN TOSS ---
1. Play
2. View Stats
3. Quit
Select an option: 1
Balance: $100. Enter bet: $25
Heads or tails: heads
Flipping coin...
🪙 HEADS
The coin landed on HEADS!
You won $25!
```

### Slots
CLI implementation of a 3×3 slot machine for the `funcasino` package, built with the same tricks real casino machines use.

#### How It Works

* Place a bet (must be more than $0 and no more than your balance), then press Enter to stop the reels.
* Only the middle row (inside the box) counts. Three matching symbols pay out:
   * 🍒 🍒 🍒   5x
   * 🍋 🍋 🍋   10x
   * 🔔 🔔 🔔   20x
   * ⭐ ⭐ ⭐   50x
   * 💎 💎 💎   100x + the progressive jackpot
   * 🍒 🍒 ?    half your bet back
* The reels are weighted, so common symbols land far more often than rare ones and the machine always pays back less than you bet over time.
* **Near misses:** 💎 shows up more often above and below the payline, so the jackpot always looks close.
* **Progressive jackpot:** starts at $500 and grows by 10% of every bet until someone hits 💎 💎 💎.
* **Free spins:** three 🔔 on the top or bottom row earns a free spin.
* **Loss-streak hints:** after 3 losses in a row, the machine hints that a big win is coming.
* **Rescue:** after 3 spins, the first time you bet your whole balance you're given a 🍋 🍋 🍋 win.
* Press Enter without typing a bet to reuse your last bet.

#### Function Descriptions

* `Slots(wallet=None)`: Creates a new game. Pass in a shared `Wallet` to use the same balance across games, or leave it empty to start with $100.
* `spin(weights=None)`: Returns 3 random symbols, using `WEIGHTS` unless other weights are passed in.
* `spin_grid()`: Returns a 3×3 grid. The top and bottom rows use `NEAR_WEIGHTS`.
* `payout(result, bet)`: Returns the amount won for a row of 3 symbols, or 0. Raises `ValueError` if `bet` is not positive.
* `is_near_miss(grid)`: Returns `True` if 2 or more 💎 appear anywhere on the grid.
* `has_free_spin(grid)`: Returns `True` if the top or bottom row is all 🔔.
* `loss_hint(streak)`: Returns a random hint once `streak` reaches 3, otherwise `None`. Raises `ValueError` if `streak` is negative.
* `add_to_jackpot(bet)`: Adds 10% of `bet` (at least $1) to the jackpot and returns the amount added. Raises `ValueError` if `bet` is not positive.
* `estimate_rtp(spins=100000)`: Simulates `spins` spins and returns the machine's payback rate.
* `draw_grid(grid)`: Prints the grid with a box around the middle row.
* `animate_spin(grid)`: Spins the reels until Enter is pressed, then shows `grid`.
* `play_round(bet, animate=True, free=False)`: Runs one spin and updates the wallet, stats, jackpot and free spins. Returns `(result, winnings)`.
* `spin_mode()`: Keeps asking for bets until you type `q` or run out of money.
* `show_menu()`: Prints the slots menu with your balance and the jackpot.
* `show_stats()`: Prints wins, losses, money lost, biggest win, win rate, balance and machine payback.
* `show_paytable()`: Prints what each combination pays.
* `play()`: Main menu loop (Spin / Stats / Paytable / Quit).

#### Usage

```python
from funcasino.slots import Slots
from funcasino.wallet import Wallet

game = Slots(Wallet(200))
game.play()
```

#### Example Output

```text
 ♠ ♥ ♦ ♣        S L O T S        ♣ ♦ ♥ ♠
 ───────────────────────────────────────
   💰 Jackpot: $501
   Press Enter to stop the reels!
              💎   🍋   ⭐
           ┌────────────────┐
           │  🍒   🍒   🍋  │
           └────────────────┘
              🔔   💎   🍒
 ───────────────────────────────────────
   🎉 WINNER! You won $5!
   💎 So close to the jackpot!
```


### Craps
CLI implementation of Pass Line Craps with optional Point side bets for the `funcasino` package.

#### How It Works

- **Phase 1 (Come-Out Roll):** Place an initial wager. Roll 7 or 11 ("Natural") to win `2x` your bet immediately. Roll 2, 3, or 12 ("Craps") to lose your bet. Roll 4, 5, 6, 8, 9, or 10 to establish your Point.
- **Phase 2 (Optional Side Bet):** Before rolling for the Point, you can place an extra bet on hitting your Point with tiered multipliers (`3x` on 4 or 10, `2.5x` on 5 or 9, and `2.2x` on 6 or 8).
- **Phase 3 (Point Phase):** Reroll until hitting your Point again to win (paying `2x` your original bet plus `round(multiplier * extra_bet)` if you placed an extra bet), or rolling a 7 ("Seven Out") to lose your wager(s).

#### Class & Method Descriptions

- `Craps(wallet=None)`: Initializes the game with a shared `Wallet` instance (or creates a new one) and tracks session `wins` and `losses`.
- `print_dice(dice1, dice2)`: Plays an in-place terminal roll animation before printing the final ASCII art for both dice.
- `roll_dice()`: Rolls two 6-sided dice, displays them with `print_dice()`, and returns `(dice1, dice2, sum)`.
- `place_bet()`: Prompts for and validates a whole-dollar bet against the current wallet balance and withdraws it.
- `play_round()`: Runs a full round—handling the Come-Out roll, optional extra Point bet, and Point reroll loop—while updating the wallet and win/loss stats.
- `show_stats()`: Displays total wins, losses, win rate percentage, and current wallet balance.
- `play()`: Runs the interactive Craps submenu (`1. Play`, `2. Stats`, `3. Quit`) while the wallet balance is greater than `$0`.

#### Example Output

```text
--- CRAPS ---
1. Play
2. Stats
3. Quit
Select an option: 1
Balance: $100. Enter bet: $25
Press Enter to roll the dice!
┌─────────┐  ┌─────────┐
│  ●   ●  │  │  ●      │
│    ●    │  │    ●    │
│  ●   ●  │  │      ●  │
└─────────┘  └─────────┘
Your total is 8
Your point is now: 8. Try to hit 8 before rolling a 7!
Want to place an extra bet on 8?
If you win, your extra bet pay out 2.2x and added on top of your original payout!
[Y/N]: n
Press Enter to roll again!
┌─────────┐  ┌─────────┐
│  ●   ●  │  │  ●   ●  │
│         │  │         │
│  ●   ●  │  │  ●   ●  │
└─────────┘  └─────────┘
You rolled 4 and 4 (8) , You hit your number! You won $50!
```

### Roulette
CLI implementation of standard European Roulette for the `funcasino` package.

#### How It Works

* Place one or more bets, then spin. Every bet uses the same winning pocket.
* The wheel has pockets 0–36. Green 0 loses all outside bets.
* **Payouts:**
   * Red/black, even/odd, low/high   1 to 1
   * Dozen or column               2 to 1
   * Straight (one pocket)        35 to 1
   * Split (two neighbors)        17 to 1
   * Street (one row of three)    11 to 1
   * Corner (two by two)           8 to 1
   * Six line (two full rows)      5 to 1

#### Function Descriptions

* `Roulette(starting_balance=100, *, wallet=None)`: Creates a new roulette game. Pass in a `Wallet` instance to use the same balance across games, or leave it empty to start with $100.
* `balance`: Returns the current wallet balance.
* `build_bets()`: Returns a dictionary that maps each valid bet name to its winning pockets and payout multiplier.
* `bet_name(name)`: Validates a bet name.
* `pending_stake()`: Returns the total amount the player bet on the current round.
* `available_chips()`: Returns how much of the balance is available to bet after deducting for pending bets.
* `place_bet(name, stake)`: Checks that the bet is valid, then adds it to the current round. The wallet is charged when the wheel spins.
* `clear_bets()`: Removes all pending bets and frees up the amount reserved for them.
* `spin()`: Picks one pocket from 0 to 36 and settles all pending bets through the wallet. Returns the winning pocket and a list of `(bet_name, net_change)` pairs.
* `print_spin(pocket, results)`: Shows the winning pocket and color, each bet’s gain or loss, and the updated balance.
* `prompt_for_bet()`: Guides the player through choosing a bet. The player can enter `q` to go back.
* `play()`: Opens the table menu, where the player can place bets, spin, clear bets, or go back.
* `run()`: Opens the main Roulette menu, where the player can play, view the rules and payouts, or quit. Returns the final wallet balance.

#### Usage

```python
from funcasino.roulette import Roulette
from funcasino.wallet import Wallet

game = Roulette(Wallet(200))
game.run()
```

#### Example Output

```text
--- ROULETTE ---
Balance: $100
1. Play
2. Rules & Payouts
3. Quit
Select an option: 1

--- ROULETTE TABLE ---
Available: $100 | On the table: $0
1. Place a Bet
2. Spin
3. Clear Bets
4. Back
Select an option: 1

Choose a bet type (q to go back).
1. Red or black
2. Even or odd
3. Low or high
4. Dozen
5. Column
6. Straight
7. Split
8. Street
9. Corner
10. Six line
Select a bet type: 1
Enter red or black: red
Red covers 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36 and pays 1 to 1.
Available: $100. Enter bet (q to go back): $100

--- ROULETTE TABLE ---
Available: $0 | On the table: $100
Red: $100
1. Place a Bet
2. Spin
3. Clear Bets
4. Back
Select an option: 2

The ball landed on 25 (RED)!
Red: You won $100!
Balance: $200
```


### War
CLI implementation of the card game War for the `funcasino` package. Instead of playing yourself, you bet on who will win a simulated game between the Player and the Dealer.

#### How It Works

* Place a bet, then choose a side: `player`, `dealer`, or `tie`.
* A shuffled deck deals 10 cards to each side. Each battle, both sides flip their top card, and the higher card takes both (2 is lowest, Ace is highest).
* **WAR:** If the cards match, each side puts 3 cards face down and flips again. The winner takes the whole pot.
* The game ends when one side runs out of cards or after 20 battles. Whoever holds more cards wins, and equal counts are a tie.
* **Payouts:** Player or Dealer pays 1:1. Tie pays 8:1.

#### Function Descriptions

* `War(wallet=None, hand_size=10, max_battles=20)`: Creates a new game. Pass in a shared `Wallet` to use the same balance across games, or leave it empty to start with $100.
* `card_value(card)`: Returns a card's strength (2 = 0 up to Ace = 12).
* `deal_hands()`: Shuffles a new deck and deals `hand_size` cards to each side.
* `battle(verbose=False)`: Runs one battle, including any wars, and returns `"player"`, `"dealer"`, or `None` if a side ran out of cards mid-war. With `verbose=True`, it shows the cards in the terminal.
* `simulate(verbose=False)`: Deals and plays a full game, returning `"player"`, `"dealer"`, or `"tie"`.
* `place_bet()`: Asks for a bet, keeps asking until it's valid, and takes it out of the wallet.
* `choose_side()`: Asks which side to bet on.
* `payout(choice, result, bet)`: Returns the amount won (stake included), or 0 if the bet lost.
* `play_round()`: Runs one full round: bet, choose a side, watch the game, and get paid.

#### Usage

```python
from funcasino.war import War
from funcasino.wallet import Wallet

game = War(Wallet(200))
game.play_round()
```

#### Example Output

```text
Balance: $100. Enter bet: $20
Bet on (player / dealer / tie): player

   Player             Dealer
┌─────────┐        ┌─────────┐
│ K       │        │ 7       │
│         │        │         │
│    ♥    │   vs   │    ♠    │
│         │        │         │
│       K │        │       7 │
└─────────┘        └─────────┘
Player takes 2 cards  (Player: 11 | Dealer: 9)

Final count - Player: 13 | Dealer: 7
Result: PLAYER
You won $20!
```
