import random
import csv
from datetime import datetime
import os

# Constants
MAX_LINES = 3
MIN_BET = 10
MAX_BET = 500
ROWS = 3
COLS = 3
MACHINE_INITIAL_BALANCE = 10000  # Default initial balance
ADMIN_PASSWORD = "admin123"  # Admin password

# Symbol configurations
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

# Save machine balance to a file
def save_machine_balance(machine_balance):
    with open("machine_balance.txt", "w") as file:
        file.write(str(machine_balance))

# Load machine balance from a file
def load_machine_balance():
    try:
        with open("machine_balance.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return MACHINE_INITIAL_BALANCE

# Check for winnings
def check_winning(columns, lines, bet, symbol_value):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:  # All symbols match in this line
            winnings += symbol_value[symbol] * bet
            winning_lines.append(line + 1)  # Lines are 1-indexed
    return winnings, winning_lines

# Generate the slot machine columns
def get_slot_machine(rows, cols, symbols):
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)
    return columns

# Print the slot machine in a readable format
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        row_output = " | ".join(column[row] for column in columns)
        print(row_output)

# Get deposit amount
def deposit():
    while True:
        amount = input("What would you like to deposit ($): ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")

# Get the number of lines to bet on
def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number.")

# Get the bet amount for each line
def get_bet():
    while True:
        amount = input(f"Enter your bet per line (${MIN_BET}-${MAX_BET}): ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")

# Perform a spin
def spin(player_balance, machine_balance):
    while True:
        lines = get_number_of_lines()
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > player_balance:
            print(f"You do not have enough balance to bet that amount. Your current balance is ${player_balance}.")
            if player_balance < MIN_BET:
                print("You don't have enough money to place the minimum bet. Please add more money or quit.")
                return player_balance, machine_balance
            else:
                print("Please adjust your bet or the number of lines.")
        elif total_bet > machine_balance:
            print(f"The machine does not have enough balance to cover your bet. Machine balance is ${machine_balance}.")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet: ${total_bet}.")
    slots = get_slot_machine(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winning(slots, lines, bet, symbol_value)

    if winnings > 0:
        print(f"You won ${winnings}!")
        print("You won on lines:", ", ".join(map(str, winning_lines)))
        player_balance += winnings
        machine_balance -= winnings
        player_winnings = winnings
        machine_winnings = 0
    else:
        print("You didn't win anything. Try again!")
        player_balance -= total_bet
        machine_balance += total_bet
        player_winnings = 0
        machine_winnings = total_bet

    log_to_csv(player_winnings, machine_winnings, player_balance, machine_balance)
    return player_balance, machine_balance

# Log game results to CSV
def log_to_csv(player_winnings, machine_winnings, player_balance, machine_balance):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    winner = "Player" if player_winnings > 0 else "Machine"

    with open("slot_machine_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, time_str, winner, player_winnings, machine_winnings, player_balance, machine_balance])

# Initialize CSV file with headers if it doesn't exist
def initialize_csv():
    if not os.path.exists("slot_machine_log.csv"):
        with open("slot_machine_log.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Winner", "Player Winnings", "Machine Winnings", "Player Balance", "Machine Balance"])

# Admin functions
def admin_menu():
    print("\nAdmin Menu:")
    print("1. Total Games Played")
    print("2. Machine Balance")
    print("3. Daily Profit/Loss")
    print("4. Machine Wins vs Player Wins")
    print("5. Exit Admin Mode")

    choice = input("Enter your choice (1-5): ")
    return choice

# Calculate total games played
def total_games_played():
    try:
        with open("slot_machine_log.csv", "r") as file:
            reader = csv.reader(file)
            return sum(1 for row in reader) - 1  # Subtract header row
    except FileNotFoundError:
        return 0

# Calculate daily profit/loss
def daily_profit_loss():
    today = datetime.now().strftime("%Y-%m-%d")
    total_machine_winnings = 0
    total_player_winnings = 0

    try:
        with open("slot_machine_log.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == today:
                    total_machine_winnings += int(row[4])
                    total_player_winnings += int(row[3])
        return total_machine_winnings - total_player_winnings
    except FileNotFoundError:
        return 0

# Calculate machine wins vs player wins
def wins_statistics():
    machine_wins = 0
    player_wins = 0

    try:
        with open("slot_machine_log.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[2] == "Machine":
                    machine_wins += 1
                elif row[2] == "Player":
                    player_wins += 1
        return machine_wins, player_wins
    except FileNotFoundError:
        return 0, 0

# Admin mode
def admin_mode():
    password = input("Enter admin password: ")
    if password != ADMIN_PASSWORD:
        print("Incorrect password. Access denied.")
        return

    while True:
        choice = admin_menu()
        if choice == "1":
            total_games = total_games_played()
            print(f"Total games played: {total_games}")
        elif choice == "2":
            machine_balance = load_machine_balance()
            print(f"Machine balance: ${machine_balance}")
        elif choice == "3":
            profit_loss = daily_profit_loss()
            print(f"Daily profit/loss: ${profit_loss}")
        elif choice == "4":
            machine_wins, player_wins = wins_statistics()
            print(f"Machine wins: {machine_wins}, Player wins: {player_wins}")
        elif choice == "5":
            print("Exiting admin mode.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main game loop
def main():
    # Initialize CSV file (only if it doesn't exist)
    initialize_csv()

    # Ask if the user is a player or admin
    user_type = input("Are you a player or admin? (player/admin): ").lower()
    if user_type == "admin":
        admin_mode()
        return  # Exit after admin mode

    # Load the machine balance from the file or use the initial balance
    machine_balance = load_machine_balance()
    player_balance = deposit()

    while True:
        print(f"Player balance: ${player_balance}")
        print(f"Machine balance: ${machine_balance}")
        if player_balance < MIN_BET:
            print("You don't have enough money to place the minimum bet. Please add more money or quit.")
            answer = input("Would you like to add more money? (y/n): ").lower()
            if answer == "y":
                additional_deposit = deposit()
                player_balance += additional_deposit
            else:
                save_machine_balance(machine_balance)  # Save machine balance before quitting
                break
        else:
            answer = input("Press Enter to spin (q to quit): ").lower()
            if answer == "q":
                save_machine_balance(machine_balance)  # Save machine balance before quitting
                break

        if player_balance <= 0:
            print("You ran out of money! Game over.")
            save_machine_balance(machine_balance)  # Save machine balance when game ends
            break
        if machine_balance <= 0:
            print("The machine ran out of money! Game over.")
            save_machine_balance(machine_balance)  # Save machine balance when game ends
            break

        player_balance, machine_balance = spin(player_balance, machine_balance)

    print(f"Game over! Final player balance: ${player_balance}, Final machine balance: ${machine_balance}.")

if __name__ == "__main__":
    main()