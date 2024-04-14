import tkinter as tk
from tkinter import ttk
from algorithm import a_star
import map_gen
import os

class AStarSimulator:
    def __init__(self, master, grid_size=10, tile_size=5):
        self.master = master
        master.title("Ambulances")

        self.grid_size = grid_size
        self.cells = {}
        self.start_points = set()
        self.end_point = None
        self.obstacles = set()
        self.setup_grid()
        self.setup_keybindings()

        self.map_generator = None
        self.tile_size = tile_size
        self.seed = 0
        self.setup_map_gen_ui()

    def setup_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                frame = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=0)
                frame.grid(row=i, column=j)

                screen_height = self.master.winfo_screenheight()
                label_size = 20
                height = int(screen_height / label_size / (self.grid_size + 1))
                width = int(height * 2.5)
                cell = tk.Label(master=frame, bg="white", width=width, height=height)
                cell.pack(padx=1, pady=1)

                cell.bind("<Button-1>", self.on_left_click(i, j))
                cell.bind(
                    "<Button-2>", self.on_middle_click(i, j)
                )  # For mac users, this must be <Button-3>
                cell.bind("<Button-3>", self.on_right_click(i, j))
                self.cells[(i, j)] = cell

    def setup_keybindings(self):
        self.master.bind("<Return>", self.start_search)
        self.master.bind("<BackSpace>", self.clear_grid)
        self.master.bind("<Escape>", lambda event: self.master.destroy())
    
    def setup_map_gen_ui(self):

        frame = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=0)
        screen_height = self.master.winfo_screenheight()
        label_size = 20
        cell_height = int(screen_height / label_size / (self.grid_size + 1))
        cell_width = int(cell_height * 2.5)
        frame.grid(row=self.grid_size, column=0, columnspan=self.grid_size)
        
        load_tiles_button = ttk.Button(
            frame,
            text='Load Tiles',
            command=lambda: self.load_tiles('tiles')
        )
        load_tiles_button.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)
        generate_map_button = ttk.Button(
            frame,
            text='Generate Map',
            command=lambda: self.generate_map()
        )
        generate_map_button.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        seed_entry = ttk.Entry(
            frame,
            textvariable = "0"
        )
        seed_entry.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)
        seed_set_button = ttk.Button(
            frame,
            text='Set Seed',
            command=lambda: self.set_seed(int(seed_entry.get()))
        )
        seed_set_button.grid(column=3, row=0, sticky=tk.E, padx=5, pady=5)

    
    def on_left_click(self, i, j):
        def handler(event):
            self.set_start(i, j)

        return handler

    def on_middle_click(self, i, j):
        def handler(event):
            self.set_obstacle(i, j)

        return handler

    def on_right_click(self, i, j):
        def handler(event):
            self.set_end(i, j)

        return handler
    
    # map generation ---
    def load_tiles(self, directory): # loads the tile files
        tiles = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                f = os.path.join(directory, filename)
                tiles.append(map_gen.Tile.from_file(f))
        map_tiles_size = int(self.grid_size / self.tile_size); 
        self.map_generator = map_gen.MapGenerator(tiles, map_tiles_size, map_tiles_size)
        print(f'loaded tiles from {directory}!')

    def set_seed(self, seed):
        print(f'seed set to {seed}')
        self.seed = seed

    def generate_map(self):
        print(f'generating map with seed {self.seed}...')
        generated_map = self.map_generator.generate_map(self.seed)
        print('map generated! applying to ui...')
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = generated_map[i][j]
                if value == 0 and (i, j) in self.obstacles:
                        self.cells[(i, j)].config(bg="white")
                        self.obstacles.remove((i, j))
                elif value == 1 and (i, j) != self.end_point and (i, j) not in self.start_points:
                    self.cells[(i, j)].config(bg="black")
                    self.obstacles.add((i, j))
        print('done!')
    # ---

    def set_start(self, i, j):
        if (i, j) in self.start_points:
            self.cells[(i, j)].config(bg="white")
            self.start_points.remove((i, j))
            self.clear_path()
        elif (i, j) != self.end_point and (i, j) not in self.obstacles:
            self.cells[(i, j)].config(bg="green")
            self.start_points.add((i, j))
    
    def set_end(self, i, j):
        if (i,j) in self.start_points or (i,j) in self.obstacles or self.end_point == (i,j):
            return
        if self.end_point:
            self.cells[self.end_point].config(bg="white")
            self.end_point = None
            self.clear_path()

        self.end_point = (i, j)
        self.cells[(i, j)].config(bg="red")

    def set_obstacle(self, i, j):
        if (i, j) in self.obstacles:
            self.cells[(i, j)].config(bg="white")
            self.obstacles.remove((i, j))
        elif (i, j) != self.end_point and (i, j) not in self.start_points:
            self.cells[(i, j)].config(bg="black")
            self.obstacles.add((i, j))

    def start_search(self, event=None):
        if self.start_points is None or self.end_point is None:
            print("Ponto de início ou fim não definido!")
            return

        # Clean the grid maintaining start, end and obstacle points
        self.clear_path()

        # Prepare the grid to apply A*
        grid = [
            [0 if (i, j) not in self.obstacles else 1 for j in range(self.grid_size)]
            for i in range(self.grid_size)
        ]

        # Gather least distance initial nodes
        a_start_solutions = []
        for start_point in self.start_points:
            alg_result = a_star(start_point, self.end_point, grid)
            a_start_solutions.append(alg_result)
        a_start_solutions = list( # Throw away empty solution
            filter(lambda alg_result: alg_result[2] is not None, a_start_solutions)
        )
        min_distance = min(alg_result[2] for alg_result in a_start_solutions) # Find minimum cost
        a_start_solutions = list( # Filter for solutions with minimal cost
            filter(lambda alg_result: alg_result[2] == min_distance, a_start_solutions)
        )
        
        # Loop through solution paths
        for solution in a_start_solutions:
            path, explored, _ = solution
            start_point = path[0]

            # Update grid with visited nodes
            for position in explored:
                curr_cell = self.cells[position]
                if position not in (start_point, self.end_point) and curr_cell[
                    "bg"
                ] not in ("blue", "green"):
                    curr_cell.config(bg="lightgray")

            if path is None:
                print("Não foi possível encontrar um caminho.")
                return

            # Update grid with the found path
            for position in path:
                curr_cell = self.cells[position]
                if (
                    position not in (start_point, self.end_point)
                    and curr_cell["bg"] != "green"
                ):
                    curr_cell.config(bg="blue")

    def clear_path(self, event=None):
        for (i, j), cell in self.cells.items():
            if (
                (i, j) not in self.obstacles
                and (i, j) not in self.start_points
                and (i, j) != self.end_point
            ):
                cell.config(bg="white")

    def clear_grid(self, event=None):
        for cell in self.cells.values():
            cell.config(bg="white")
        self.start_points.clear()
        self.end_point = None
        self.obstacles.clear()
