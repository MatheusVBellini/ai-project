import heapq

# A* Algorithm
# f(n) = g(n) + h(n)
#
# g(n) = path cost from starting node to n node
# h(n) = heuristic prediction from n node to end node
# f(n) = g(n) + h(n) = total predicted cost


# grid cell
class Cell:

    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0  # g(n)
        self.h = 0  # h(n)
        self.f = 0  # f(n)

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Cell({self.pos}, {self.f})"


def a_star(start, end, grid):
    start_cell = Cell(start)
    end_cell = Cell(end)

    open_list = []
    closed_list = set()

    # Put start_cell in path
    heapq.heappush(open_list, start_cell)
    explored = set()

    # Loop until open_list is empty
    while open_list:
        # Get node with least f(n) in open_list
        current_cell = heapq.heappop(open_list)
        closed_list.add(current_cell.pos)
        explored.add(current_cell.pos)

        # Check if reached objective
        if current_cell == end_cell:
            path = []
            cost = 0
            while current_cell:
                path.append(current_cell.pos)
                cost = cost + current_cell.g
                current_cell = current_cell.parent
            return (
                path[::-1],
                explored,
                cost,
            )  # Return (reversed path, explored nodes, path cost)

        # Generate neighboors of current node
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (
                current_cell.pos[0] + new_position[0],
                current_cell.pos[1] + new_position[1],
            )

            # Verify whether new position is obstacle
            if (
                0 <= node_position[0] < len(grid)
                and 0 <= node_position[1] < len(grid[0])
                and not grid[node_position[0]][node_position[1]]
            ):
                if node_position in closed_list:
                    continue

                new_cell = Cell(node_position, current_cell)

                # Calculate g, h and f
                new_cell.g = current_cell.g + 1
                new_cell.h = abs(node_position[0] - end[0]) + abs(
                    node_position[1] - end[1]
                )
                new_cell.f = new_cell.g + new_cell.h

                # Add cell to open_list if not there already
                if not any(
                    cell
                    for cell in open_list
                    if cell.pos == new_cell.pos and cell.f <= new_cell.f
                ):
                    heapq.heappush(open_list, new_cell)

    return None, explored, None  # if no path found
