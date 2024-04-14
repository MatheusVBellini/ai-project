import random
import imageio.v3 as iio

class Tile:
    def __init__(self, w, h):
        self.w = w;
        self.h = h;
        self.mat = [[0 for y in range(h)] for x in range(w)]
    def get_connection(self, conn):
        if conn == "N":
            return tuple(self.mat[x][0] for x in range(self.w))
        elif conn == "S":
            return tuple(self.mat[x][self.w - 1] for x in range(self.w))
        elif conn == "W":
            return tuple(self.mat[0][y] for y in range(self.h))
        elif conn == "E":
            return tuple(self.mat[self.w - 1][y] for y in range(self.h))
        else:
            return tuple()
    def from_file(file_name):
        im = iio.imread(file_name)
        assert len(im.shape) < 3, "The image needs to be grayscale!"
        t = Tile(im.shape[0], im.shape[1])
        t.mat = [[1 if im[x][y] < 127 else 0 for y in range(t.h)] for x in range(t.w)]
        return t

class MapGenerator:
    def __init__(self, tiles, map_w_tiles, map_h_tiles):
        self.tiles = tiles
        self.tiles_w = tiles[0].w
        self.tiles_h = tiles[0].h
        self.map_w_tiles = map_w_tiles
        self.map_h_tiles = map_h_tiles
        # creates connections lookup table
        self.connections = {'N': dict(), 'S': dict(), 'E': dict(), 'W': dict()}
        for i in range(len(tiles)):
            print(f'tile={i}')
            tile = tiles[i]
            for direction in self.connections:
                conn = tile.get_connection(direction)
                print(f'\t{conn}({direction})')
                if conn not in self.connections[direction]:
                    self.connections[direction][conn] = []
                self.connections[direction][conn].append(tile)

    def generate_map(self, seed):
        random.seed(seed)
        generated_map = [[0 for y in range(self.tiles_h * self.map_h_tiles)] for x in range(self.tiles_w * self.map_w_tiles)]
        last_tile = Tile(0,0)
        last_start_of_line_tile = Tile(0,0)
        for tiles_y in range(self.map_h_tiles):
            for tiles_x in range(self.map_w_tiles):
                # choose random tile based on previous ones
                current_tile = Tile(0,0)
                if tiles_x == 0 and tiles_y == 0: # starting tile
                    current_tile = random.choice(self.tiles)
                else:
                    if tiles_x == 0: # start of new line
                        current_tile = random.choice(self.connections["N"][last_start_of_line_tile.get_connection("S")])
                    else:
                        current_tile = random.choice(self.connections["W"][last_tile.get_connection("E")])
                # copy mat from the tile to the map mat
                for y in range(current_tile.h):
                    for x in range(current_tile.w):
                        pos_x_in_map = tiles_x * self.tiles_w + x
                        pos_y_in_map = self.tiles_h * tiles_y + y
                        generated_map[pos_x_in_map][pos_y_in_map] = current_tile.mat[x][y]
                # set the last tiles vars
                last_tile = current_tile
                if tiles_x == 0: # this tile started a line, so it will be used for the next one
                    last_start_of_line_tile = current_tile

        return generated_map

                        








        
