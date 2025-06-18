#====== Board Object ======
class Gameboard():
    def __init__(self, n: int, boom: int) -> None:
        self.n = n
        self.boom = boom
        self.grid = [[[symbol(None), 0] for _ in range(n)] for __ in range(n)]

    def __str__(self) -> str:
        x = f"{symbol(True)} {int(count(self, True))} {symbol(False)} {int(count(self, False))}"
        x += "\n       " + "      ".join(str(i) for i in range(self.n))

        for i in range(self.n):
            y = "".join([f" | {self.grid[i][j][0]} {self.grid[i][j][1]}" for j in range(self.n)])
            x += f"\n {i} {y}"
        
        return x

    def add(self, isBlue: bool, coord: tuple) -> bool:
        if coord[0] not in range(0, self.n) or coord[1] not in range(0, self.n):
            return False
        
        target = self.grid[coord[0]][coord[1]]

        if count(self, isBlue) == 0 and count(self, not isBlue) <= 1 and target[0] != symbol(not isBlue):
            self.grid[coord[0]][coord[1]] = [symbol(isBlue), 1]
            return True

        elif target[0] != symbol(isBlue):
            print("Invalid input")
            return False
    
        else:
            self.grid[coord[0]][coord[1]] = [target[0], target[1] + 1]
            return True

    def remove(self, coord: tuple) -> None:
        self.grid[coord[0]][coord[1]] = [symbol(None), 0]

    def conquer(self, coord: tuple, isBlue: bool) -> None:
        self.grid[coord[0]][coord[1]] = [symbol(isBlue), self.grid[coord[0]][coord[1]][1] + 1]

#====== Tool Funcs ======
    
def symbol(isBlue: bool) -> str:
    return "⚪" if isBlue is None else "🔵" if isBlue else "🔴"

def count(obj: Gameboard, isBlue: bool) -> int:
    return sum(1 for x in obj.grid for y in x if y[0] == symbol(isBlue))

def checkBoom(obj: Gameboard, isBlue: bool) -> list[tuple]:
    return [(i, j) for i in range(obj.n) for j in range(obj.n) if obj.grid[i][j] == [symbol(isBlue), obj.boom]]
    
def findAdjacant(obj: Gameboard, coord: tuple) -> list[tuple]:
    coords = [(coord[0]-1, coord[1]), (coord[0]+1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1)]
    booleans = [coord[0] == 0, coord[0] == obj.n-1, coord[1] == 0, coord[1] == obj.n-1]
    return [coords[i] for i in range(4) if not booleans[i]]

#====== Game UI ====== 

def updatePlayer(obj: Gameboard, isBlue: bool) -> None:
    print("=" * 20) 
    print("Blue's Turn") if isBlue else print("Red's Turn")
    print(obj)

def checkEnd(obj: Gameboard) -> bool:
    if not count(obj, True) and count(obj, False) > 1:
        print("Red Wins!")
        return True
    elif not count(obj, False) and count(obj, True) > 1:
        print("Blue Wins!")
        return True
    return False

#====== Main ======

blue = True
board = Gameboard(5, 4)

while True:
    updatePlayer(board, blue)

    if checkEnd(board):
        break

    temp = blue
    checked = False

    try:
        coord = list(map(int, input("Place your circle: ").split()))
        if len(coord) != 2:
            raise ValueError
    except:
        print("Invalid input")
        continue

    if board.add(blue, coord):
        temp = not blue
    else:
        continue

    while checkBoom(board, blue):
        checked = True
        for x in checkBoom(board, blue):
            board.remove(x)
            for y in findAdjacant(board, x):
                board.conquer(y, blue)
                
        if not checkBoom(board, blue):
            break
        elif checkEnd(board):
            break
        else:
            print(board)

    blue = temp
