import os
import random

availableSlots = []

def StartScreen():
    print("\n")
    print("Trabalho da disciplina de Inteligência Artificial - Jogo da Velha 6x6")
    print("\n")
    print("Regras: O jogador disputa contra a máquina para ver quem junta 4", 
          "símbolos na horizontal, vertical ou diagonal primeiro.")
    print("\n")
    input("Aperte enter para começar.")


def BuildBoard():
    board = []

    for i in range(6):
        row = []
        for j in range(6):
            row.append(" ")
            availableSlots.append((i, j))
        board.append(row)
            
    return board

def ChooseSymbol():
    playerSymbol = ""
    while playerSymbol != "X" and playerSymbol != "O":
        playerSymbol = input("Escolha um símbolo entre X e O (símbolo O joga primeiro): ")
    
    aiSymbol = "X" if playerSymbol == "O" else "O"
    print("\n")
    return (playerSymbol, aiSymbol)

def MiniMax(board, depth, isMaximizing, alpha, beta):
    if depth == 3:
        return 0

    winner = CheckWinner()
    if winner != None:
        return scores[winner]
    
    if isMaximizing:
        bestScore = -1000
        for i in range(6):
            for j in range(6):
                if board[i][j] == " ":
                    board[i][j] = aiSymbol
                    score = MiniMax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:        
        bestScore = 1000
        for i in range(6):
            for j in range(6):
                if board[i][j] == " ":
                    board[i][j] = playerSymbol
                    score = MiniMax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore

def GetBestMove(board, isPlayerTurn):
    bestScore = -1000
    bestMove = None

    for i in range(6):
        for j in range(6):
            if board[i][j] == " ":
                board[i][j] = aiSymbol
                score = MiniMax(board, 0, isPlayerTurn, -1000, 1000)
                board[i][j] = " "
                if score > bestScore:
                    bestScore = score
                    bestMove = (i, j)
    
    return bestMove


def NextTurn(board, playerSymbol, aiSymbol, isPlayerTurn):
    player = playerSymbol if isPlayerTurn else aiSymbol

    RenderBoard(board)
    row, column = -1, -1

    if isPlayerTurn:
        while (row > 5 or row < 0) or (column > 5 or column < 0) or (row, column) not in availableSlots:
            playerInput = input("Escolha uma posição (Escreva a coordenada separada por espaço: linha coluna):")
            if not playerInput.strip() or len(playerInput.split()) == 1:
                continue
            row, column = map(int, playerInput.split())
    else:
        row, column = GetBestMove(board, isPlayerTurn)
        # row, column = random.choice(availableSlots)
        
    board[row][column] = player
    availableSlots.remove((row, column))

    
def RenderBoard(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for r in range(0, 6):
        print(board[r][0], " |", board[r][1], "|", board[r][2], "|", board[r][3], "|", board[r][4], "|", board[r][5])
        if (r < 5):
            print("---+---+---+---+---+---")


def HasFourInline(line):
    counter = 0
    for i in range(0, len(line) - 1):
        if line[i] == line[i+1] and line[i] != " ":
            counter += 1
        else:
            counter = 0
        if counter == 3:
            return line[i]
    return None

def CheckWinner():
    winner = None

    # Verifica linhas
    for i in range(6):
        winner = HasFourInline(board[i]) if HasFourInline(board[i]) != None else winner

    # Verifica colunas
    for i in range(6):
        winner = HasFourInline([row[i] for row in board]) if HasFourInline([row[i] for row in board]) != None else winner

    # Verifica diagonais da esquerda pra direita
    for i in range(3):
        for j in range(3):
            diagonal = [board[i+k][j+k] for k in range(4)]
            winner = HasFourInline(diagonal) if HasFourInline(diagonal) is not None else winner

    # Verifica diagonais da direita pra esquerda
    for i in range(3):
        for j in range(3, 6):
            diagonal = [board[i+k][j-k] for k in range(4)]
            winner = HasFourInline(diagonal) if HasFourInline(diagonal) is not None else winner

    if winner == None and len(availableSlots) == 0 :
        return 'tie'
    else:
        return winner


# Main
StartScreen()
playerSymbol, aiSymbol = ChooseSymbol()

# playerSymbol = "O"
# aiSymbol = "X"

scores = {
    aiSymbol: 1,
    playerSymbol: -1,
    "tie": 0
}

isPlayerTurn = playerSymbol == "O"
board = BuildBoard()

# Game loop
winner = None
while (winner == None):
    winner = CheckWinner()
    NextTurn(board, playerSymbol, aiSymbol, isPlayerTurn)
    isPlayerTurn = not isPlayerTurn

if (winner == 'tie'):
    print("O jogo terminou com empate.")
else:
    print("O vencedor foi: " + winner)