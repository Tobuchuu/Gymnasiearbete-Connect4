import os
import re
from colored import fg, style
import random



def RenderScreen(screenMatrix):
    topBorder = ["▁", (colum * 2) + 1]
    bottomBorder = ["▔", topBorder[1]]
    sideBorder = "│"

    os.system('cls')

    print(topBorder[0] * topBorder[1])

    for rows in screenMatrix:

        printRow = []
        for item in rows:
            item = item[0]

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

def PlaceToken(screenMatrix, value, x, y):
    tempScreenMatrix = screenMatrix.copy()
    tempScreenMatrix[y][x] = str(value)
    return tempScreenMatrix

def DropToken(screenMatrix, value, x):
    tempScreenMatrix = screenMatrix.copy()
    

    # kollar om raden är full.
    if tempScreenMatrix[0][x] != emptyToken:
        return -1, tempScreenMatrix

    # kollar nerifrån och upp tills den hittar en tom plats
    for y in range(row-1, -1, -1):
        if tempScreenMatrix[y][x] == emptyToken:
            tempScreenMatrix = PlaceToken(tempScreenMatrix, str(value), x, y)
            return 0, tempScreenMatrix
    
    # ifall något går riktigt fel, så returnar den error 2
    return -2, tempScreenMatrix

# def CheckTokenAt(screenMatrix, x, y):
#     if y < 0 or y >= len(screenMatrix): return False
#     if x < 0 or x >= len(screenMatrix[0]): return False

#     try:
#         return screenMatrix[y][x]
#     except:
#         return False

# def SearchForPattern(screenMatrix, pattern, find_exact=True):
#     matches = []

#     if find_exact:
#         pattern = f'((?<=E)|(?<=^)){pattern}(?=E|$)'

#     # check for - matches
#     for row in screenMatrix:
#         line = row
    
#         search = re.search(pattern, "".join(i[0] for i in line))
#         if search:
#             span = search.span()
#             matches.append({
#                 "string": search.group(),
#                 "type": "-",
#                 "coords": (
#                     line[span[0]][1],
#                     line[span[1] - 1][1]
#                 )
#             })
    
#     # check for | matches
#     for column_index in range(len(screenMatrix[0])):
#         line = [x[column_index] for x in screenMatrix]

#         search = re.search(pattern, "".join(i[0] for i in line))
#         if search:
#             span = search.span()
#             matches.append({
#                 "string": search.group(),
#                 "type": "|",
#                 "coords": (
#                     line[span[0]][1],
#                     line[span[1] - 1][1]
#                 )
#             })
        
#     # check for / matches
#     for column_index in range((len(screenMatrix[0]) - 1) * -1, len(screenMatrix[0]) -1):
#         line = []

#         for row_index_difference in range(len(screenMatrix) + 1):

#             r = CheckTokenAt(screenMatrix, column_index + row_index_difference, len(screenMatrix) - row_index_difference)
#             if r:
#                 line.append(r)

#         search = re.search(pattern, "".join(i[0] for i in line))
#         if search:
#             span = search.span()
#             matches.append({
#                 "string": search.group(),
#                 "type": "/",
#                 "coords": (
#                     line[span[0]][1],
#                     line[span[1] - 1][1]
#                 )
#             })
        
#     # check for \ matches
#     for column_index in range((len(screenMatrix) * 2), 0, -1):
#         line = []

#         for row_index_difference in range(len(screenMatrix) + 1):
            
#             r = CheckTokenAt(screenMatrix, column_index - row_index_difference, len(screenMatrix) - row_index_difference)
#             if r:
#                 line.append(r)
        
#         search = re.search(pattern, "".join(i[0] for i in line))
#         if search:
#             span = search.span()
#             matches.append({
#                 "string": search.group(),
#                 "type": "\\",
#                 "coords": (
#                     line[span[1] - 1][1],
#                     line[span[0]][1]
#                 )
#             })

#     return matches

# def CheckIfPatternIsValid(screenMatrix, found_pattern):
#     """
#     Returns how many open slots a found pattern has next to it\n
#     \n
#     E X X X E -> 2\n
#     E X X X O -> 1\n
#     O X X X O -> 0\n

#     """
#     if found_pattern['type'] == "-":
#         before = CheckTokenAt(screenMatrix, found_pattern['coords'][0][0] - 1, found_pattern['coords'][0][1])
#         after  = CheckTokenAt(screenMatrix, found_pattern['coords'][1][0] + 1, found_pattern['coords'][1][1])
#     if found_pattern['type'] == "|":
#         before = CheckTokenAt(screenMatrix, found_pattern['coords'][0][0], found_pattern['coords'][0][1] - 1)
#         after  = CheckTokenAt(screenMatrix, found_pattern['coords'][1][0], found_pattern['coords'][1][1] + 1)
#     if found_pattern['type'] == "/":
#         before = CheckTokenAt(screenMatrix, found_pattern['coords'][0][0] - 1, found_pattern['coords'][0][1] - 1)
#         after  = CheckTokenAt(screenMatrix, found_pattern['coords'][1][0] + 1, found_pattern['coords'][1][1] - 1)
#     if found_pattern['type'] == "\\":
#         before = CheckTokenAt(screenMatrix, found_pattern['coords'][0][0] - 1, found_pattern['coords'][0][1] - 1)
#         after  = CheckTokenAt(screenMatrix, found_pattern['coords'][1][0] + 1, found_pattern['coords'][1][1] + 1)
    
#     if before and after:
#         return 2
#     if (before and not after) or (not before and after):
#         return 1
#     if not before and not after:
#         return 0

def StaticEvaluation(screenMatrix, playerToken):
    score = 0
    for r in range(row):
        rowArray = [i for i in screenMatrix[r]]
        for c in range(colum - 3):
            window = rowArray[c:c + windowLength]

            if window.count(playerToken) == windowLength:
                score += 100
            elif window.count(playerToken) == windowLength - 1 and window.count(emptyToken) == 1:
                score += 75
    return score

def ValidDropPosition(screenMatrix):
    validPositions = []
    for c in range(colum):
        tempScreenMatrix = screenMatrix.copy()
        if DropToken(tempScreenMatrix, currentPlayer, c)[0] == 0:
            validPositions.append(c)
    return validPositions

def PickBestMove(screenMatrix, playerToken):
    print(screenMatrix)
    validPositions = ValidDropPosition(screenMatrix.copy())
    print(screenMatrix)
    exit()
    bestScore = 0
    bestColum = random.choice(validPositions)

    for c in validPositions:
        r = NextOpenRow(screenMatrix, c)
        tempScreenMatrix = screenMatrix.copy()
        tempScreenMatrix = DropToken(tempScreenMatrix, currentPlayer, c)[1]
        
        score = StaticEvaluation(tempScreenMatrix, playerToken)
        if score > bestScore:
            bestScore = score
            bestColum = c

    return bestColum


def NextOpenRow(screenMatrix, c):
    for r in range(row):
        if screenMatrix[r][c] == emptyToken:
            return r


# def GetChildOf(screenMatrix, value):
#     toReturn = []
#     for x in range(len(screenMatrix[0])):
#         thing = DropToken(screenMatrix.copy(), value, x)
#         if thing[0] == 0:
#             toReturn.append(thing[1].copy())
#     return toReturn


# def minimax(screenMatrix, depth, maximiizingPlayer):
    # if depth == 0:
    #     return StaticEvaluation
    
    # if maximiizingPlayer:
    #     maxEval = float(-inf)
    #     for x in GetChildOf(globalScreenMatrix, currentPlayer):
    #         eval = minimax(child, depth - 1, False)
    #         maxEval = max(maxEval, eval)
    #     return maxEval
    # else:
    #     miniEval = float(inf)
    #     for x in GetChildOf(globalScreenMatrix, currentPlayer):
    #         eval = minimax(child, depth - 1, True)
    #         minEval = min(minEval, eval)
    #     return minEval

def MakeAiSelection():
    c = PickBestMove(globalScreenMatrix, playerTokens[currentPlayer - 1])
    # DropToken(globalScreenMatrix, currentPlayer, c)
    return c




def main():
    global globalScreenMatrix
    global currentPlayer

    while 1:
        # fitta = globalScreenMatrix.copy()
        # RenderScreen(GetChildOf(fitta, currentPlayer)[0])

        # for x in ("1", "11", "111", "1111"):
        #     print(x, [CheckIfPatternIsValid(globalScreenMatrix, p) for p in SearchForPattern(globalScreenMatrix, x)])

        RenderScreen(globalScreenMatrix)

        if aiPlayers[currentPlayer-1]:
            playerSelection = MakeAiSelection()
        else:
            playerSelection = input("Player %s, välj rad : " % currentPlayer)

            try: playerSelection = int(playerSelection)
            except Exception: continue
            if playerSelection < 1 or playerSelection > colum: continue

        # Kollar om spelaren kan lägga sin token
        dropTokenResult = DropToken(globalScreenMatrix, currentPlayer, playerSelection - 1)
        globalScreenMatrix = dropTokenResult[1]
        # if dropTokenResult[0] < 0:
        #     continue
        # else:
        #     globalScreenMatrix = dropTokenResult[1]

        # winStatus = SearchForPattern(globalScreenMatrix, "(1111|2222)")
        # if len(winStatus) > 0:
        #     winner = int(winStatus[0]['string'][0])
        #     RenderScreen(globalScreenMatrix)
        #     print("Player %s wins!" % winner)
        #     exit()
        
        currentPlayer = 1 if currentPlayer == 2 else 2
        




if __name__ == "__main__":
    row = 6
    colum = 7
    emptyToken = "E"
    playerTokens = ("X", "O")
    playerColors = ("1", "4")
    currentPlayer = 1

    aiPlayers = (False, True)
    windowLength = 4

    globalScreenMatrix = [[emptyToken for x in range(colum)] for y in range(row)]

    # /
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 3, 0)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 2, 1)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 1, 2)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 3)

    # \
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 3, 3)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 2, 2)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 1, 1)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 0)

    # |
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 1)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 2)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 3)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 4)

    # -
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 0, 0)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 1, 0)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 2, 0)
    # globalScreenMatrix = PlaceToken(globalScreenMatrix, "X", 3, 0)




    # RenderScreen(globalScreenMatrix)

    # scan = SearchForPattern(globalScreenMatrix, "XXXX")

    # for x in scan:
    #     print(x, "\n")

    #     print(CheckIfPatternIsValid(globalScreenMatrix, x))

    main()