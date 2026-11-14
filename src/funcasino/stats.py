LINE = " " + "─" * 39


def show_stats(games, wallet, starting_balance=100):
    total_wins = 0
    total_losses = 0
    total_ties = 0

    print()
    print(" ♠ ♥ ♦ ♣   C A S I N O   S T A T S   ♣ ♦ ♥ ♠")
    print(LINE)

    for name, game in games.items():
        wins = getattr(game, "wins", 0)
        losses = getattr(game, "losses", 0)
        ties = getattr(game, "ties", getattr(game, "pushes", 0))
        total_wins += wins
        total_losses += losses
        total_ties += ties

        record = f"{wins}W / {losses}L"
        if ties:
            record += f" / {ties}T"
        print(f"   {name:<12} {record}")

    total_games = total_wins + total_losses + total_ties
    win_rate = (total_wins / total_games * 100) if total_games else 0
    net = wallet.balance - starting_balance

    print(LINE)
    print(f"   Total Wins:   {total_wins}")
    print(f"   Total Losses: {total_losses}")
    if total_ties:
        print(f"   Total Ties:   {total_ties}")
    print(f"   Win Rate:     {win_rate:.1f}%")
    print(f"   Net Profit:   ${net:+}")
    print(f"   Balance:      ${wallet.balance}")
    print(LINE)