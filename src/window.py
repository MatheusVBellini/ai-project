import tkinter as tk
from tkinter import ttk
from algorithm import a_star, bfs  # Assumindo que você tenha o método bfs disponível
import map_gen
import os
import time

class searchSimulator:
    def __init__(self, master, grid_size=10, tile_size=5):
        self.master = master
        master.title("Ambulances")

        self.grid_size = grid_size
        self.cells = {}
        self.start_points = set()
        self.end_point = None
        self.obstacles = set()
        # apply the grid layout
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        # create the text widget
        canvas_frame = tk.Frame(master)
        canvas_frame.grid(row=0, column=0, sticky=tk.EW)
        grid_canvas = tk.Canvas(canvas_frame, width = 100, height = 10000)
        grid_canvas.grid(row=0, column=0, sticky="news")

        self.grid_frame = tk.Frame(canvas_frame)
        self.grid_frame.grid(row=0, column=0, sticky="news")
        
        # create a scrollbar widget and set its command to the text widget
        scrollbary = ttk.Scrollbar(master, orient='vertical', command=grid_canvas.yview)
        scrollbary.grid(row=0, column=1, sticky=tk.NS)
        
        #  communicate back to the scrollbar
        grid_canvas['yscrollcommand'] = scrollbary.set
        grid_canvas['yscrollincrement'] = 10


        grid_canvas.create_window((0, 0), window=self.grid_frame, anchor='w')
        self.setup_grid()
        self.grid_frame.update_idletasks()

       # Inicializa com A* como o método de busca padrão
        self.search_algorithm = 'A*'

        self.map_generator = None
        self.tile_size = tile_size
        self.seed = 0
        self.setup_map_gen_ui()


    def setup_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                frame = tk.Frame(master=self.grid_frame, relief=tk.RAISED, borderwidth=0)
                frame.grid(row=i, column=j)

                screen_height = self.grid_frame.winfo_screenheight()
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


    def toggle_search_algorithm(self, text_var):
        if self.search_algorithm == 'A*':
            self.search_algorithm = 'BFS'
        else:
            self.search_algorithm = 'A*'

        text_var.set(self.search_algorithm + " (Press 'o' to toggle)")
        print(f"Search Algorithm switched to: {self.search_algorithm}")


    def setup_map_gen_ui(self):
        frame = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=0)

        frame.grid(row=self.grid_size, column=0, columnspan=self.grid_size)
        self.load_tiles("tiles")

        seed_text = ttk.Label(frame, text="Map seed:")
        seed_text.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        seed_entry = ttk.Entry(frame)
        seed_entry.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)
        generate_button = ttk.Button(
            frame, text="Generate", command=lambda: self.on_type_seed(seed_entry.get())
        )
        generate_button.grid(column=3, row=0, sticky=tk.E, padx=5, pady=5)

        search_method_text = ttk.Label(frame, text="Search Method:")
        search_method_text.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        text_var = tk.StringVar()
        text_var.set(self.search_algorithm + " (Press 'o' to toggle)")
        search_method_label = ttk.Label(frame, textvariable=text_var)
        search_method_label.grid(column=2, row=1, sticky=tk.E, padx=5, pady=5)

        self.master.bind("<Return>", self.search)
        self.master.bind("<BackSpace>", self.clear_grid)
        self.master.bind("<Escape>", lambda event: self.master.destroy())
        self.master.bind("o", lambda event: self.toggle_search_algorithm(text_var))

    def search(self, event=None):
        # time the search
        time_start = time.time()
        self.start_search()
        time_end = time.time()
        print(f"Search {self.search_algorithm} took {(time_end - time_start) * 1000}ms")

    def on_type_seed(self, seed):
        print(seed)

        if not seed:
            print("seed not set!")
            return

        self.clear_grid()
        self.set_seed(seed)
        self.generate_map()

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
    def load_tiles(self, directory):  # loads the tile files
        tiles = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                f = os.path.join(directory, filename)
                tiles.append(map_gen.Tile.from_file(f))
        map_tiles_size = int(self.grid_size / self.tile_size)
        self.map_generator = map_gen.MapGenerator(tiles, map_tiles_size, map_tiles_size)
        print(f"loaded tiles from {directory}!")

    def set_seed(self, seed):
        int_seed = int(seed)
        print(f"seed set to {int_seed}")
        self.seed = int_seed

    def generate_map(self):
        print(f"generating map with seed {self.seed}...")
        if not self.map_generator or not self.seed:
            print("tiles or seed not set!")
            return

        generated_map = self.map_generator.generate_map(self.seed)
        print("map generated! applying to ui...")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = generated_map[i][j]
                if value == 0 and (i, j) in self.obstacles:
                    self.cells[(i, j)].config(bg="white")
                    self.obstacles.remove((i, j))
                elif (
                    value == 1
                    and (i, j) != self.end_point
                    and (i, j) not in self.start_points
                ):
                    self.cells[(i, j)].config(bg="black")
                    self.obstacles.add((i, j))
        print("done!")

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
        if (
            (i, j) in self.start_points
            or (i, j) in self.obstacles
            or self.end_point == (i, j)
        ):
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

        # Prepare the grid to apply search algorithm
        grid = [
            [0 if (i, j) not in self.obstacles else 1 for j in range(self.grid_size)]
            for i in range(self.grid_size)
        ]

        # Gather least distance initial nodes
        search_solutions = []
        if self.search_algorithm == 'A*':
            for start_point in self.start_points:
                alg_result = a_star(start_point, self.end_point, grid)
                search_solutions.append(alg_result)
        else:
            alg_result = bfs(self.end_point, self.start_points, grid)
            search_solutions.append(alg_result)

        # sum all explored nodes from all solutions
        explored_count = 0
        for solution in search_solutions:
            explored_count += len(solution[1])

        search_solutions = list(  # Throw away empty solution
            filter(lambda alg_result: alg_result[2] is not None, search_solutions)
        )

        min_distance = min(
            alg_result[2] for alg_result in search_solutions
        )  # Find minimum cost

        search_solutions = list(  # Filter for solutions with minimal cost
            filter(lambda alg_result: alg_result[2] == min_distance, search_solutions)
        )

        # Loop through solution paths
        for solution in search_solutions:
            path, explored, _ = solution
            start_point = path[0]

            # Update grid with visited nodes
            for position in explored:
                curr_cell = self.cells[position]
                if position not in (start_point, self.end_point) and curr_cell["bg"] not in ("blue", "green"):
                    curr_cell.config(bg="lightgray")

            if path is None:
                print("Não foi possível encontrar um caminho.")
                return

            # Update grid with the found path
            for position in path:
                curr_cell = self.cells[position]
                if (position not in (start_point, self.end_point) and curr_cell["bg"] != "green"):
                    curr_cell.config(bg="blue")

        print(f"Explorados: {explored_count}")

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
