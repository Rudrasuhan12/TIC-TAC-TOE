import sys
import numpy as np

# Check if required modules are available
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    sys.exit("Error: Tkinter is not installed or not supported in this environment.")


# Initialize the board
def reset_board():
    global board, player_turn, mode
    board = np.array([["" for _ in range(3)] for _ in range(3)], dtype=object)
    player_turn = "X"
    update_buttons()


def update_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j], state=("normal" if board[i][j] == "" else "disabled"))


def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    for col in board.T:
        if col[0] == col[1] == col[2] and col[0] != "":
            return col[0]
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != "":
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != "":
        return board[0, 2]
    if "" not in board:
        return "Draw"
    return None


def minimax(board, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    if winner == "O":
        return 1
    if winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = "O"
                    score = minimax(board, False)
                    board[i, j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = "X"
                    score = minimax(board, True)
                    board[i, j] = ""
                    best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == "":
                board[i, j] = "O"
                score = minimax(board, False)
                board[i, j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move] = "O"
        update_buttons()
        check_game_over()


def check_game_over():
    winner = check_winner()
    if winner:
        if winner == "Draw":
            messagebox.showinfo("Game Over", "It's a Draw!")
        else:
            messagebox.showinfo("Game Over", f"{winner} Wins!")
        reset_board()


def on_click(i, j):
    global player_turn
    if board[i, j] == "":
        board[i, j] = player_turn
        update_buttons()
        if not check_winner():
            if mode == "AI" and player_turn == "X":
                best_move()
            else:
                player_turn = "O" if player_turn == "X" else "X"
        check_game_over()


def set_mode(selected_mode):
    global mode
    mode = selected_mode
    reset_board()


# GUI Setup
root = tk.Tk()
root.title("Tic-Tac-Toe")

mode = "AI"  # Default mode is AI
player_turn = "X"

buttons = [[tk.Button(root, text="", font=("Arial", 24), width=5, height=2,
                      command=lambda i=i, j=j: on_click(i, j)) for j in range(3)] for i in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i, column=j)

mode_frame = tk.Frame(root)
mode_frame.grid(row=3, column=0, columnspan=3)

tk.Button(mode_frame, text="Play vs AI", command=lambda: set_mode("AI"), width=10).pack(side=tk.LEFT)
tk.Button(mode_frame, text="2 Player", command=lambda: set_mode("2P"), width=10).pack(side=tk.RIGHT)

reset_board()
root.mainloop()
