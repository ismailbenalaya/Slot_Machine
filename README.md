# Slot Machine Game

This is a Python-based slot machine game that simulates a simple casino experience. Players can deposit money, place bets, and spin the slot machine to win or lose money. The game also includes an **admin mode** for tracking statistics like total games played, machine balance, daily profit/loss, and win/loss ratios.

---

## Features

### **Player Mode**
1. **Deposit Money**:
   - Players can deposit an initial amount of money to start playing.
2. **Place Bets**:
   - Players can choose the number of lines to bet on (1-3) and the bet amount per line ($10-$500).
3. **Spin the Slot Machine**:
   - The slot machine generates random symbols, and players win if they match symbols across a line.
4. **Winning Logic**:
   - Different symbols have different values and multipliers.
   - Winnings are calculated based on the bet amount and symbol combinations.
5. **Game Over**:
   - The game ends if the player or the machine runs out of money.

### **Admin Mode**
1. **Password Protection**:
   - Admins must enter a password to access admin functions.
2. **Statistics**:
   - Admins can view:
     - Total games played.
     - Current machine balance.
     - Daily profit/loss.
     - Number of machine wins vs player wins.

### **Data Persistence**
1. **Machine Balance**:
   - The machine's balance is saved to a file (`machine_balance.txt`) and persists between game sessions.
2. **Game Logs**:
   - All game results are logged in a CSV file (`slot_machine_log.csv`) for tracking and analysis.

---

## How to Play

### **Player Mode**
1. Run the game.
2. Choose **player** mode when prompted.
3. Deposit an initial amount of money.
4. Place bets and spin the slot machine.
5. Continue playing until you decide to quit or run out of money.

### **Admin Mode**
1. Run the game.
2. Choose **admin** mode when prompted.
3. Enter the admin password (`admin123`).
4. Use the admin menu to view statistics:
   - Total games played.
   - Machine balance.
   - Daily profit/loss.
   - Machine wins vs player wins.

---

## Setup

### **Requirements**
- Python 3.x
- No external libraries are required.

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/slot-machine-game.git

### ***File Structure***
**-slot_machine.py**: The main Python script for the game.

**-slot_machine_log.csv**: Logs all game results for tracking and analysis.


## ***Code Overview*** 
### ***Key Functions***
***Player Functions:***

-deposit(): Handles player deposits.

-get_number_of_lines(): Allows players to choose the number of lines to bet on.

-get_bet(): Allows players to set the bet amount per line.

-spin(): Simulates a spin of the slot machine and calculates winnings.

***Admin Functions:***

-admin_menu(): Displays the admin menu and handles user input.

-total_games_played(): Calculates the total number of games played.

-daily_profit_loss(): Calculates the daily profit or loss.

-wins_statistics(): Calculates the number of machine wins vs player wins.

***Utility Functions:***

-save_machine_balance(): Saves the machine's balance to a file.

-load_machine_balance(): Loads the machine's balance from a file.

-log_to_csv(): Logs game results to a CSV file.

## ***Contributing***
Contributions are welcome! If you'd like to add new features, improve the code, or fix bugs, feel free to open a pull request.


## ***Acknowledgments***
**Inspired by classic casino slot machines**

**Built with Python for simplicity and fun.**

**Enjoy the game! 🎰**
