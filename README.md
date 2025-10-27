# Backgammon Game

### Alumno: Nahuel Quiroga - 64048

## Prerequisites

1. Install Python 3.11+
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Start Redis server

```bash
docker-compose up -d
```

### Run the application

```bash
python main.py --gui
```

And choice the option do you want

### Pygame Usage

- **SPACE**: Roll dice
- **R**: Reset game
- **ESC**: Exit

### CLI Usage

The CLI interface provides a text-based way to play Backgammon. Here are the available commands:

- **help (h)**: Show help menu with all available commands
- **board (b)**: Display the current board state with all pieces
- **turn (t)**: Show which player's turn it is
- **roll (r)**: Roll dice for the current player
- **status (s)**: Show the last dice roll and remaining moves
- **moves**: Show possible moves from a specific point (interactive)
- **move**: Make a move from one point to another (interactive prompts)
- **enter**: Enter a piece from the bar using a specific die value
- **bearoff**: Bear off a checker from the board (if allowed)
- **end (e)**: End the current player's turn and switch to the next player
- **quit (q)**: Exit the game

#### How to Play on CLI:

1. Start the game with `python main.py`
2. Use `roll` to roll the dice
3. Use `moves` to see possible moves from a point
4. Use `move` to execute a move (you'll be prompted for source and destination)
5. Use `bearoff` when all pieces are in your home board
6. Use `end` to finish your turn

### Pygame Usage

The Pygame interface provides a visual representation of the Backgammon board with mouse and keyboard controls.

#### Controls:

- **SPACE**: Roll dice
- **R**: Reset game
- **ESC**: Exit game
- **Mouse Click**: Select pieces and make moves

#### How to Play on Pygame:

1. Start the game with `python main.py --gui`
2. Click on a piece to select it (highlighted in green)
3. Click on a valid destination to move the piece
4. Use SPACE to roll dice when it's your turn
5. The game will automatically switch turns when no moves are available
6. Win by bearing off all your pieces first

#### Visual Indicators:

- **Green highlight**: Selected piece
- **Blue highlight**: Valid destinations for selected piece
- **Dice display**: Shows current roll and remaining moves
- **Turn indicator**: Shows whose turn it is
- **Win message**: Displays when a player wins
