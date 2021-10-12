row = 6
colum = 7
emptyToken = "E"
playerTokens = ("X", "O")
currentPlayer = 1


screenMatrix = [[emptyToken for x in range(colum)] for y in range(row)]


def renderScreen():
    topBorder = ["▁", (colum * 2) + 1]
    bottomBorder = ["▔", topBorder[1]]
    sideBorder = "│"

    print(topBorder[0] * topBorder[1])

    for rows in screenMatrix:

        printRow = []
        for item in rows:
            if item == emptyToken:
                printRow.append(" ")
            elif item == "1":
                printRow.append(playerTokens[0])
            elif item == "2":
                printRow.append(playerTokens[1])
            else:
                printRow.append(item)

        print(sideBorder + sideBorder.join(printRow) + sideBorder)

    print(bottomBorder[0] * bottomBorder[1])
    
def CheckWin():
    # Horizontal win check
    for y in screenMatrix:
        temp = "".join(y)

        if "1" * 4 in temp:
            print("1 win")
            return 1
        if "2" * 4 in temp:
            print("2 win")
            return 2
    
    # Vertical win check
    for x in range(colum):
        temp = ""
        for y in range(row):
            temp += screenMatrix[y][x]
    
        if "1" * 4 in temp:
            print("1 win")
            return 1
        if "2" * 4 in temp:
            print("2 win")
            return 2

    # Diagonal win check \
    for y in range(0, row - 3):
        for x in range(0, colum - 3):
            temp = "".join(screenMatrix[y+i][x+i] for i in range(4))
            
            if "1" * 4 in temp:
                print("1 win")
                return 1
            if "2" * 4 in temp:
                print("2 win")
                return 2

    # Diagonal win check /
    for y in range(0, row - 3):
        for x in range(colum - 1, 0, -1):
            temp = "".join(screenMatrix[y+i][x-i] for i in range(4))
            
            if "1" * 4 in temp:
                print("1 win")
                return 1
            if "2" * 4 in temp:
                print("2 win")
                return 2

def SwitchTurn():
    currentPlayer = 2 if (currentPlayer == 1) else 1
    return currentPlayer

def PlaceToken(value, x, y):
    screenMatrix[y][x] = value

def DropToken(value, x):
    # kollar om raden är full.
    if screenMatrix[0][x] != emptyToken:
        return -1

    # kollar nerifrån och upp tills den hittar en tom plats
    for y in range(row-1, -1, -1):
        if screenMatrix[y][x] == emptyToken:
            PlaceToken(value, x, y)
            return 0
    
    # ifall något går riktigt fel, så returnar den error 2
    return -2




PlaceToken("1", 3, 2)
PlaceToken("1", 2, 3)
PlaceToken("1", 1, 4)
PlaceToken("1", 0, 5)

# PlaceToken("1", 3, 1)
# PlaceToken("1", 4, 2)
# PlaceToken("1", 5, 3)
# PlaceToken("1", 6, 4)


CheckWin()

renderScreen()




