import tkinter as tk
import random
import math

# Window
root = tk.Tk()
root.title("Tic Tac Toe AI")

board = [" "]*9
buttons = []
player = "X"
ai = "O"
difficulty = tk.StringVar(value="Hard")

player_score = 0
ai_score = 0

# Score Label
score_label = tk.Label(root, text="Player: 0  AI: 0", font=("Arial", 14))
score_label.grid(row=0, column=0, columnspan=3)

# Update Score
def update_score():
    score_label.config(text=f"Player: {player_score}  AI: {ai_score}")

# Check Winner
def check_winner(b, p):
    wins = [[0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]]
    return any(b[a]==b[b1]==b[c]==p for a,b1,c in wins)

# Draw
def is_draw():
    return " " not in board

# Minimax
def minimax(b, is_max):
    if check_winner(b, ai): return 1
    if check_winner(b, player): return -1
    if " " not in b: return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]=ai
                score = minimax(b, False)
                b[i]=" "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]=player
                score = minimax(b, True)
                b[i]=" "
                best = min(best, score)
        return best

# AI Move
def ai_move():
    if difficulty.get() == "Easy":
        empty = [i for i in range(9) if board[i]==" "]
        move = random.choice(empty)
    else:
        best = -math.inf
        move = 0
        for i in range(9):
            if board[i]==" ":
                board[i]=ai
                score = minimax(board, False)
                board[i]=" "
                if score > best:
                    best = score
                    move = i

    board[move]=ai
    buttons[move].config(text=ai)

# Click
def click(i):
    global player_score, ai_score

    if board[i]==" ":
        board[i]=player
        buttons[i].config(text=player)

        if check_winner(board, player):
            player_score += 1
            update_score()
            reset()
            return

        if is_draw():
            reset()
            return

        ai_move()

        if check_winner(board, ai):
            ai_score += 1
            update_score()
            reset()
            return

        if is_draw():
            reset()

# Reset
def reset():
    global board
    board = [" "]*9
    for btn in buttons:
        btn.config(text="")

# Buttons
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 20),
                    width=5, height=2,
                    command=lambda i=i: click(i))
    btn.grid(row=1+i//3, column=i%3)
    buttons.append(btn)

# Difficulty Option
tk.Label(root, text="Difficulty:").grid(row=4, column=0)
tk.OptionMenu(root, difficulty, "Easy", "Hard").grid(row=4, column=1)

# Reset Button
tk.Button(root, text="Reset", command=reset).grid(row=4, column=2)

root.mainloop()