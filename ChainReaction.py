#====== Board Object ======
class Gameboard():
    def __init__(self, n: int, boom: int) -> None:
        self.n = n
        self.boom = boom
        self.grid = [[[symbol(None), 0] for _ in range(n)] for __ in range(n)]
        self.red_count = 0
        self.blue_count = 0

    def __str__(self) -> str:
        x = f"{symbol(True)} {int(getScore(self, True))} {symbol(False)} {int(getScore(self, False))}"
        x += "\n       " + "      ".join(str(i) for i in range(self.n))

        for i in range(self.n):
            y = "".join([f" | {self.grid[i][j][0]} {self.grid[i][j][1]}" for j in range(self.n)])
            x += f"\n {i} {y}"
        
        return x

    def add(self, isBlue: bool, coord: tuple) -> bool:
        if coord[0] not in range(0, self.n) or coord[1] not in range(0, self.n):
            return False
        
        target = self.grid[coord[0]][coord[1]]

        if getScore(self, isBlue) == 0 and getScore(self, not isBlue) <= 1 and target[0] != symbol(not isBlue):
            self.grid[coord[0]][coord[1]] = [symbol(isBlue), 1]
            self.modifyScore(isBlue, 1)
            return True

        elif target[0] != symbol(isBlue):
            print("Invalid input")
            return False
    
        else:
            self.grid[coord[0]][coord[1]] = [target[0], target[1] + 1]
            return True

    def remove(self, coord: tuple) -> None:
        if self.grid[coord[0]][coord[1]][0] == symbol(True):
            self.modifyScore(True, -1)
        elif self.grid[coord[0]][coord[1]][0] == symbol(False):
            self.modifyScore(False, -1)
        self.grid[coord[0]][coord[1]] = [symbol(None), 0]
        

    def conquer(self, coord: tuple, isBlue: bool) -> None:
        if self.grid[coord[0]][coord[1]][0] == symbol(not isBlue):
            self.modifyScore(not isBlue, -1)

        if self.grid[coord[0]][coord[1]][0] != symbol(isBlue):
            self.modifyScore(isBlue, 1)

        self.grid[coord[0]][coord[1]] = [symbol(isBlue), min(self.grid[coord[0]][coord[1]][1] + 1, self.boom)]

    def modifyScore(self, isBlue: bool, counts: int) -> None:
        if isBlue:
            self.blue_count += counts
        else:
            self.red_count += counts

#====== Tool Funcs ======
    
def symbol(isBlue: bool) -> str:
    return "⚪" if isBlue is None else "🔵" if isBlue else "🔴"

def getScore(obj: Gameboard, isBlue: bool) -> int:
    return obj.blue_count if isBlue else obj.red_count

def checkBoom(obj: Gameboard, isBlue: bool) -> list[tuple]:
    return [(i, j) for i in range(obj.n) for j in range(obj.n) if obj.grid[i][j] == [symbol(isBlue), obj.boom]]
    
def findAdjacent(obj: Gameboard, coord: tuple) -> list[tuple]:
    coords = [(coord[0]-1, coord[1]), (coord[0]+1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1)]
    booleans = [coord[0] == 0, coord[0] == obj.n-1, coord[1] == 0, coord[1] == obj.n-1]
    return [coords[i] for i in range(4) if not booleans[i]]

#====== Game UI ====== 

def updatePlayer(obj: Gameboard, isBlue: bool, round: int) -> None:
    print("=" * 20)
    x = "Blue" if isBlue else "Red"
    print(f"{x}'s Turn: ", end="")
    print(f"Round {round}")
    print(obj)

def checkEnd(obj: Gameboard, round: int) -> bool:
    if not getScore(obj, True) and getScore(obj, False) > 1:
        print(f"Round {round}: Red Wins!")
        return True
    elif not getScore(obj, False) and getScore(obj, True) > 1:
        print(f"Round {round}: Blue Wins!")
        return True
    return False

#====== Main ======

blue = True
board = Gameboard(5, 4)
round = 1
while True:
    updatePlayer(board, blue, round)

    if checkEnd(board, round):
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
        if temp == True:
            round += 1
    else:
        continue

    while checkBoom(board, blue):
        checked = True
        for x in checkBoom(board, blue):
            board.remove(x)
            for y in findAdjacent(board, x):
                board.conquer(y, blue)
                
        if not checkBoom(board, blue):
            break
        elif checkEnd(board):
            break
        else:
            print(board)

    blue = temp
