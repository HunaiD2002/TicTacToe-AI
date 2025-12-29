import tkinter as tk

from gui.gui import TicTacToeGUI

if __name__ == '__main__':
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
