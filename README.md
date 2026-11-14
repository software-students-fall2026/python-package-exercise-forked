[![CI](https://github.com/software-students-fall2026/python-package-exercise-forked/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-forked/actions/workflows/ci.yml)

# Fun Casino

FunCasino is a Python package that simulates some of the most popular casino games, including blackjack, roulette, and slots, for educational purposes.

<!-- [PyPI Link](https://www.google.com/) -->

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


### Craps
CLI implementation of standard Pass Line Craps for the `funcasino` package.

#### How It Works

* **Phase 1 (Come-Out Roll):** Win on 7 or 11. Lose on 2, 3, or 12 ("Craps"). Roll 4, 5, 6, 8, 9, or 10 to set the target Point.
* **Phase 2 (Point Phase):** Reroll until hitting your Point number again to win, or rolling a 7 to lose ("Seven Out").

#### Function Descriptions

* `print_dice(dice1, dice2)`: Takes two die and prints an ASCII art representation in the terminal.
* `play_craps(player)`: Main game controller function. Validates bets, runs Come-Out and Point roll loops, displays dice art, and updates the global `Player` object 

#### Example Output

```text
------ Welcome to CRAPS ------
Current Balance: $100
Enter your Pass Line bet: $25
Press Enter to roll the dice!

┌─────────┐  ┌─────────┐
│  ●   ●  │  │  ●      │
│    ●    │  │    ●    │
│  ●   ●  │  │      ●  │
└─────────┘  └─────────┘

Your Point is now: 8. Try to hit 8 before rolling a 7!
Press Enter to roll again...

┌─────────┐  ┌─────────┐
│  ●   ●  │  │  ●   ●  │
│         │  │         │
│  ●   ●  │  │  ●   ●  │
└─────────┘  └─────────┘

You hit your point (8)! You WIN $25! New Balance: $125
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
