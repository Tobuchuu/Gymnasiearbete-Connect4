import os
from colored import fg, style

def RenderScreen():
    topBorder = ["▁", (colum * 2) + 1]
    bottomBorder = ["▔", topBorder[1]]
    sideBorder = "│"

    os.system('cls')

    print(topBorder[0] * topBorder[1])

    for rows in screenMatrix:

        printRow = []
        for item in rows:
            if item == emptyToken:
                printRow.append(" ")
            elif item == "1":
                printRow.append(fg(playerColors[0]) + playerTokens[0] + style.RESET)
            elif item == "2":
                printRow.append(fg(playerColors[1]) + playerTokens[1] + style.RESET)
            else:
                printRow.append(item)

        print(sideBorder + sideBorder.join(printRow) + sideBorder)

    print(bottomBorder[0] * bottomBorder[1])

def CheckWin(bruh):
    # Horizontal win check
    for y in screenMatrix:
        temp = "".join(y)

        if "1" * bruh in temp:
            return 1
        if "2" * bruh in temp:
            return 2
    
    # Vertical win check
    for x in range(colum):
        temp = ""
        for y in range(row):
            temp += screenMatrix[y][x]
    
        if "1" * bruh in temp:
            return 1
        if "2" * bruh in temp:
            return 2

    # Diagonal win check \
    for y in range(0, row - 3):
        for x in range(0, colum - 3):
            temp = "".join(screenMatrix[y+i][x+i] for i in range(4))
            
            if "1" * bruh in temp:
                
            if "2" * bruh in temp:
                return 2

    # Diagonal win check /
    for y in range(0, row - 3):
        for x in range(colum - 1, 0, -1):
            temp = "".join(screenMatrix[y+i][x-i] for i in range(4))
            
            if "1" * bruh in temp:
                return 1
            if "2" * bruh in temp:
                return 2

    # Kollar om det blir oavgjort
    if not emptyToken in "".join(screenMatrix[0]):
        return "tie"

    return 0

def SwitchTurn():
    global currentPlayer
    currentPlayer = 2 if (currentPlayer == 1) else 1
    return currentPlayer

def PlaceToken(screenMatrix, value, x, y):
    screenMatrix = screenMatrix.copy()
    screenMatrix[y][x] = str(value)
    return screenMatrix

def DropToken(screenMatrix, value, x):
    screenMatrix = screenMatrix.copy()
    # kollar om raden är full.
    if screenMatrix[0][x] != emptyToken:
        return -1, screenMatrix

    # kollar nerifrån och upp tills den hittar en tom plats
    for y in range(row-1, -1, -1):
        if screenMatrix[y][x] == emptyToken:
            screenMatrix = PlaceToken(screenMatrix, str(value), x, y)
            return 0, screenMatrix
    
    # ifall något går riktigt fel, så returnar den error 2
    return -2, screenMatrix

def AiMakeSelection():
    
    pass

def GetBestMove():
    
    pass
    

def main():
    global screenMatrix
    
    while 1:
        RenderScreen()

        if aiPlayers[currentPlayer-1]:
            playerSelection = AiMakeSelection()
        else:
            playerSelection = input("Player %s, välj rad : " % currentPlayer)

            try: playerSelection = int(playerSelection)
            except Exception: continue
            if playerSelection < 1 or playerSelection > colum: continue

        # Kollar om spelaren kan lägga sin token
        dropTokenResult = DropToken(screenMatrix, currentPlayer, playerSelection - 1)
        if dropTokenResult[0] < 0:
            continue
        else:
            screenMatrix = dropTokenResult[1]

        winStatus = CheckWin()
        if winStatus in (1, 2):
            RenderScreen()
            print("Player %s wins!" % winStatus)
            exit()
        elif winStatus == "tie":
            RenderScreen()
            print("It's a Tie")
            exit()
        
        SwitchTurn()
        
if __name__ == "__main__":
    row = 6
    colum = 7
    emptyToken = "E"
    playerTokens = ("X", "O")
    playerColors = ("1", "4")
    currentPlayer = 1

    aiPlayers = (False, False)

    screenMatrix = [[emptyToken for x in range(colum)] for y in range(row)]

    main()
