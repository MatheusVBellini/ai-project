import tkinter as tk
from window import AStarSimulator


def main():
    root = tk.Tk()

    grid_size = 20
    AStarSimulator(root, grid_size=grid_size)
    root.mainloop()


if __name__ == "__main__":
    main()
