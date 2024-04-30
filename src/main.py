import tkinter as tk
from window import searchSimulator


def main():
    root = tk.Tk()
    root.geometry("800x800")

    grid_size = 50
    searchSimulator(root, grid_size=grid_size)
    root.mainloop()


if __name__ == "__main__":
    main()
