import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# إعداد الواجهة
root = tk.Tk()
root.title("XO Game with AI")
root.geometry("460x600")
root.configure(bg="#4682B4")
root.resizable(False, False)

current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
ai_enabled = False
ai_difficulty = "Hard"

scores = {"X": 0, "O": 0}
player_names = {"X": "Player X", "O": "Player O"}

def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] != "": return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "": return True
    if board[0][0] == board[1][1] == board[2][2] != "": return True
    if board[0][2] == board[1][1] == board[2][0] != "": return True
    return False

def is_draw():
    return not any("" in row for row in board)

def reset_board():
    global current_player, board
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", fg="black")
    status_label.config(text=f"Turn: {current_player} — {player_names[current_player]}")

def reset_game():
    reset_board()
    scores["X"] = scores["O"] = 0
    score_label.config(text=f"{player_names['X']}: {scores['X']}  |  {player_names['O']}: {scores['O']}")
    select_mode()

def update_score(winner):
    scores[winner] += 1
    score_label.config(text=f"{player_names['X']}: {scores['X']}  |  {player_names['O']}: {scores['O']}")

def minimax(board_state, is_maximizing):
    if check_winner(): return -1 if is_maximizing else 1
    if is_draw(): return 0

    if is_maximizing:
        best = -99
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == "":
                    board_state[i][j] = "O"
                    score = minimax(board_state, False)
                    board_state[i][j] = ""
                    best = max(best, score)
        return best
    else:
        best = 99
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == "":
                    board_state[i][j] = "X"
                    score = minimax(board_state, True)
                    board_state[i][j] = ""
                    best = min(best, score)
        return best

def get_best_move():
    best, move = -99, None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                sc = minimax(board, False)
                board[i][j] = ""
                if sc > best:
                    best, move = sc, (i, j)
    return move

def ai_move():
    global current_player
    if ai_difficulty == "Easy":
        move = random.choice([(i,j) for i in range(3) for j in range(3) if board[i][j]==""])
    elif ai_difficulty == "Medium" and random.random() < 0.5:
        move = get_best_move()
    else:
        move = get_best_move()
    if not move:
        return
    i, j = move
    board[i][j], buttons[i][j]["text"], buttons[i][j]["fg"] = "O", "O", "#337AFF"
    if check_winner():
        messagebox.showinfo("Game Over", f"{player_names['O']} (AI) wins!")
        update_score("O")
        reset_board()
    elif is_draw():
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()
    else:
        current_player = "X"
        status_label.config(text=f"Turn: {current_player} — {player_names[current_player]}")

def on_click(i, j):
    global current_player
    if board[i][j] == "" and current_player == "X":
        board[i][j] = "X"
        buttons[i][j].config(text="X", fg="#FF5733")
        if check_winner():
            messagebox.showinfo("Game Over", f"{player_names['X']} wins!")
            update_score("X")
            reset_board()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            if ai_enabled:
                current_player = "O"
                status_label.config(text=f"Turn: {current_player} — {player_names[current_player]}")
                root.after(500, ai_move)
            else:
                current_player = "O"
                status_label.config(text=f"Turn: {current_player} — {player_names[current_player]}")

def select_mode():
    global ai_enabled
    board.clear()
    reset_board()
    mode = simpledialog.askstring("Game Mode", "Enter mode: 'PVP' or 'AI'")
    if not mode: 
        root.quit(); return
    mode = mode.strip().upper()
    if mode == "PVP":
        ai_enabled = False
        player_names["X"] = simpledialog.askstring("Player X", "Enter name for Player X") or "Player X"
        player_names["O"] = simpledialog.askstring("Player O", "Enter name for Player O") or "Player O"
    else:
        ai_enabled = True
        player_names["X"] = simpledialog.askstring("Player", "Enter your name") or "Player"
        player_names["O"] = "Computer"
        diff = simpledialog.askstring("Difficulty", "Enter difficulty: Easy / Medium / Hard").strip().capitalize()
        if diff in ("Easy","Medium","Hard"):
            globals()["ai_difficulty"] = diff
        else:
            globals()["ai_difficulty"]="Hard"
    score_label.config(text=f"{player_names['X']}: {scores['X']}  |  {player_names['O']}: {scores['O']}")
    status_label.config(text=f"Turn: {current_player} — {player_names[current_player]}")

frame = tk.Frame(root, bg="#4682B4")
frame.place(relx=0.5, rely=0.5, anchor="center")

buttons = [[None]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        b = tk.Button(frame, text="", font=("Helvetica", 30), width=4, height=2,
                      bg="#E6E6FA", relief="raised", bd=5,
                      command=lambda i=i,j=j: on_click(i,j))
        b.grid(row=i, column=j, padx=7, pady=7)
        buttons[i][j] = b

score_label = tk.Label(root, text="", font=("Arial", 14), bg="#4682B4", fg="white")
score_label.pack(pady=10)
status_label = tk.Label(root, text="", font=("Arial", 16), bg="#4682B4", fg="white")
status_label.pack(pady=5)

restart_btn = tk.Button(root, text="🔁 Restart Game", font=("Arial", 14),
                        bg="#90EE90", command=reset_game)
restart_btn.pack(pady=10)

select_mode()
root.mainloop()
