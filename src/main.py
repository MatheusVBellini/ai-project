import tkinter as tk
from window import searchSimulator


def main():
    root = tk.Tk()

    grid_size = 20
    searchSimulator(root, grid_size=grid_size)
    root.mainloop()


if __name__ == "__main__":
    main()
