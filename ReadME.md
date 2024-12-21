2048 Game in Python
This is a Python implementation of the popular 2048 game using Pygame. The game allows players to combine tiles of the same value to create new tiles, aiming to create a tile with the value 2048. The game ends when there are no more valid moves left.

Features
Multiple Difficulty Levels: Easy, Medium, and Hard modes, with different grid sizes (3x3 for Easy, 4x4 for Medium, 5x5 for Hard).
you can change difficulty as per ur wish by pressing f1 you can play easy mode ,f2 for medium and f3 for hard mode.
Undo Move: A feature to undo the previous move.
Leaderboard: Tracks the top 5 scores in the game, stored in a file (leaderboard.txt).
Score Display: Displays the current score during gameplay.
Game Over: Displays a "Game Over" message along with the leaderboard when the game ends.
Requirements
Python 3.x
Pygame library (for graphics and game handling)
You can install the required dependencies by running:

bash
Copy code
pip install pygame
How to Play
Use the arrow keys to move the tiles.
Up arrow: Move tiles upwards.
Down arrow: Move tiles downwards.
Left arrow: Move tiles left.
Right arrow: Move tiles right.
The goal is to combine tiles of the same value to create a tile with the value of 2048.
You can also change the difficulty during the game:
F1: Set difficulty to Easy (3x3 grid).
F2: Set difficulty to Medium (4x4 grid).
F3: Set difficulty to Hard (5x5 grid).
The score will be updated as you merge tiles.
When no valid moves are available, the game will display "Game Over" along with the leaderboard.
Files
leaderboard.txt: Stores the top 5 highest scores.
game_2048.py: The main Python file containing the game logic.
Running the Game
Clone or download the repository.
Open a terminal/command prompt and navigate to the directory containing the game_2048.py file.
Run the game with the following command:
bash
Copy code
python game_2048.py
The game will start in Medium difficulty by default. You can change the difficulty during gameplay using the F1, F2, or F3 keys.

Screenshots

License
This project is licensed under the MIT License.









