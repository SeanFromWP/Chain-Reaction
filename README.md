# Chain-Reaction
My classmates are playing this game, so I decided to write a Python version.

## How To Play
Copy the code or save it locally, then run it using Python.

## Game Rules
### Basic
* There are 2 players: Blue and Red. Blue goes first.
* The game board is an **n x n** grid (default: 5 x 5).
* If you don't have any circles on the board yet, you can place one in any empty cell.
* Otherwise, you can only click on a circle that you already control to increase its value by 1.
* (See "Boom" below.)
* After your turn ends, it's your opponent's turn.
* If one player completely eliminates the other from the board, they win.

### Boom
* There is a **Boom value** (default: 4).
* If one of your circles reaches the Boom value, it explodes:
  * Each of its adjacent (up, down, left, right) cells increases by 1 and changes to your color.
* This process repeats until no circle has the Boom value.
* After the chain reaction ends, your turn is over.

## Customize
* You can customize the board size and Boom value via the `Gameboard(n, boom)` constructor.
