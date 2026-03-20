import math

# Board
board = [" " for _ in range(9)]

# Print board
def print_board():
    print()
    for i in range(3):
        print(board[i*3] + " | " + board[i*3+1] + " | " + board[i*3+2])
        if i < 2:
            print("--+---+--")
    print()

# Check winner
def check_winner(b, player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diagonals
    ]
    for condition in win_conditions:
        if b[condition[0]] == b[condition[1]] == b[condition[2]] == player:
            return True
    return False

# Check draw
def is_draw(b):
    return " " not in b

# Minimax Algorithm
def minimax(b, depth, is_maximizing):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_draw(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, depth + 1, False)
                b[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, depth + 1, True)
                b[i] = " "
                best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

# Player move
def player_move():
    while True:
        try:
            pos = int(input("Enter position (1-9): ")) - 1
            if board[pos] == " ":
                board[pos] = "X"
                break
            else:
                print("Position already taken!")
        except:
            print("Invalid input!")

# Game loop
def play_game():
    print("Tic-Tac-Toe: You (X) vs AI (O)")
    print("Positions: 1-9\n")

    print_board()

    while True:
        player_move()
        print_board()

        if check_winner(board, "X"):
            print("You Win! 🎉")
            break
        if is_draw(board):
            print("Draw!")
            break

        print("AI is thinking...")
        ai_move()
        print_board()

        if check_winner(board, "O"):
            print("AI Wins! 🤖")
            break
        if is_draw(board):
            print("Draw!")
            break

# Run game
play_game()