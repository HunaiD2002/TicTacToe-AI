import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random

from agent.agent import TicTacToeAgent

class TicTacToeGUI:
    def __init__(self, root, agent_model_path=None):
        self.root = root
        self.root.title('TicTacToe - PyTorch Agent')
        self.buttons = [None] * 9
        self.board = [''] * 9
        self.current_player = 'X'
        self.agent = None
        if agent_model_path and os.path.exists(agent_model_path):
            try:
                self.agent = TicTacToeAgent(agent_model_path)
                print('Loaded agent from', agent_model_path)
            except Exception as e:
                print('Failed to load agent:', e)
        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)
        for i in range(9):
            btn = tk.Button(frame, text='', font=('Arial', 24), width=4, height=2,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons[i] = btn

        ctrl = tk.Frame(self.root)
        ctrl.pack(pady=8)
        tk.Button(ctrl, text='Restart', command=self.restart).pack(side='left', padx=5)
        tk.Button(ctrl, text='Load Model', command=self.load_model_dialog).pack(side='left', padx=5)

    def on_click(self, idx):
        if self.board[idx] != '' or self.current_player != 'X':
            return
        self.make_move(idx, 'X')
        if self.check_winner('X'):
            messagebox.showinfo('Game over', 'You (X) win!')
            return
        if all(self.board[i] != '' for i in range(9)):
            messagebox.showinfo('Game over', 'Draw')
            return
        self.current_player = 'O'
        self.root.after(300, self.agent_turn)

    def agent_turn(self):
        # --- PHASE 1: IMMEDIATE REFLEXES (Win or Block) ---
        
        # 1. Can I (O) win right now? -> DO IT.
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                if self.check_winner('O'):
                    self.make_move(i, 'O')
                    messagebox.showinfo('Game over', 'Agent (O) wins!')
                    return
                self.board[i] = '' # Undo

        # 2. Can the Opponent (X) win right now? -> BLOCK THEM.
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'X'
                if self.check_winner('X'):
                    self.board[i] = ''
                    self.make_move(i, 'O') # Block!
                    self.current_player = 'X'
                    return
                self.board[i] = '' # Undo

        # 3. Strategic Opening (Take Center)
        if self.board[4] == '':
            self.make_move(4, 'O')
            self.current_player = 'X'
            return

        # --- PHASE 2: AGGRESSIVE BRAIN (Perspective Swap) ---
        move = None
        if self.agent:
            print("Thinking aggressively...")
            probs = []
            for idx in range(9):
                if self.board[idx] == '':
                    # Simulate the move
                    tmp_board = self.board.copy()
                    tmp_board[idx] = 'O'
                    
                    # SWAP PERSPECTIVE: 
                    # The brain only knows how to predict if 'X' wins.
                    # So we trick it: We pretend O is X, and X is O.
                    swapped_board = []
                    for cell in tmp_board:
                        if cell == 'O': swapped_board.append('X')
                        elif cell == 'X': swapped_board.append('O')
                        else: swapped_board.append('')
                    
                    # Now ask: "Does 'X' (actually Me) win in this future?"
                    # We look at index [1] which is the "Win" probability
                    p_my_win = self.agent.predict_proba(swapped_board)[1]
                    probs.append((p_my_win, idx))
            
            if probs:
                # MAXIMIZE my own winning chance (Aggressive)
                # instead of minimizing opponent's winning chance (Defensive)
                _, move = max(probs, key=lambda x: x[0])
        
        # Fallback
        if move is None:
            empties = [i for i, v in enumerate(self.board) if v == '']
            if empties:
                move = random.choice(empties)

        # Execute
        self.make_move(move, 'O')
        if self.check_winner('O'):
            messagebox.showinfo('Game over', 'Agent (O) wins!')
            return
        if all(self.board[i] != '' for i in range(9)):
            messagebox.showinfo('Game over', 'Draw')
            return
        self.current_player = 'X'

    def make_move(self, idx, symbol):
        self.board[idx] = symbol
        self.buttons[idx]['text'] = symbol

    def check_winner(self, symbol):
        b = self.board
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(b[i]==symbol and b[j]==symbol and b[k]==symbol for (i,j,k) in wins)

    def restart(self):
        self.board = [''] * 9
        for b in self.buttons:
            b['text'] = ''
        self.current_player = 'X'

    def load_model_dialog(self):
        path = filedialog.askopenfilename(title='Load PyTorch model (.pt)', filetypes=[('PyTorch', '*.pt'), ('All', '*.*')])
        if path:
            try:
                self.agent = TicTacToeAgent(path)
                messagebox.showinfo('Model', f'Loaded model from {path}')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load model: {e}')