def fill_grid_periphery(n, m, red, green, blue, periphery_colors):
    # Initialize the grid with None
    grid = [[None] * m for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Define periphery positions
    periphery_positions = [(0, j) for j in range(m)] + [(n - 1, j) for j in range(m)] + \
                          [(i, 0) for i in range(1, n - 1)] + [(i, m - 1) for i in range(1, n - 1)]

    # Shuffle periphery positions to make selection random
    random.shuffle(periphery_positions)

    # Assign periphery colors in the order given by the user
    for color in periphery_colors:
        for i, j in periphery_positions:
            if grid[i][j] is None and color_counts[color] > 0:
                grid[i][j] = color
                color_counts[color] -= 1

    # Fill remaining periphery positions with available colors
    for i, j in periphery_positions:
        if grid[i][j] is None:
            for color in 'RGB':
                if color_counts[color] > 0:
                    grid[i][j] = color
                    color_counts[color] -= 1
                    break

    # Fill the remaining empty spaces in the grid
    for i in range(m):
        for j in range(m):
            if grid[i][j] is None:
                for color in 'RGB':
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

    return grid

def fill_grid_diagonal(dimension, red, green, blue, diagonal_colors):
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    diagonal_positions = [(i, i) for i in range(dimension)]

    # Assign diagonal colors
    index = 0
    for i, j in diagonal_positions:
        if index < len(diagonal_colors) and color_counts[diagonal_colors[index]] > 0:
            grid[i][j] = diagonal_colors[index]
            color_counts[diagonal_colors[index]] -= 1
            index += 1
        else:
            # If selected diagonal colors run out, use any available color
            for color in 'RGB':
                if color_counts[color] > 0:
                    grid[i][j] = color
                    color_counts[color] -= 1
                    break

    # Fill the rest of the grid with available colors
    for i in range(dimension):
        for j in range(dimension):
            if grid[i][j] is None:
                for color in 'RGB':
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

    return grid

import random
def adjacency_const(n, m, red, green, blue, adjacency_cons):
    tile_counts = {}
    tile_counts['R'] = red
    tile_counts['G'] = green
    tile_counts['B'] = blue
    grid = [[' ' for _ in range(m)] for _ in range(n)]

    tile1, tile2 = adjacency_cons[0], adjacency_cons[1]
    if tile_counts[tile1] > tile_counts[tile2]:
        tile1, tile2 = tile2, tile1

    if tile_counts[tile2] > 4 * tile_counts[tile1]:
        print("Error: Not possible to satisfy the constraint.")
        return None, None, None

    placed_tiles = {'R': 0, 'G': 0, 'B': 0}
    adjacent_pairs = 0
    placed_positions = []

    row, col = 1, 1
    while placed_tiles[tile1] < tile_counts[tile1] and placed_tiles[tile2] < tile_counts[tile2]:
        if grid[row][col] == ' ':
            grid[row][col] = tile1
            placed_tiles[tile1] += 1
            placed_positions.append((row, col))

            adjacent_positions = [
                (row, col-1), (row, col+1),
                (row-1, col), (row+1, col)
            ]

            for adj_row, adj_col in adjacent_positions:
                if (0 <= adj_row < n and 0 <= adj_col < m and
                    grid[adj_row][adj_col] == ' ' and
                    placed_tiles[tile2] < tile_counts[tile2]):
                    grid[adj_row][adj_col] = tile2
                    placed_tiles[tile2] += 1
                    adjacent_pairs += 1

        col += 3
        if col >= m:
            col = 1
            row += 3
            if row >= n:
                break

    if placed_tiles[tile1] < tile_counts[tile1]:
        for i, j in placed_positions:
            diagonal_positions = [
                (i-1, j-1), (i-1, j+1),
                (i+1, j-1), (i+1, j+1)
            ]
            for di, dj in diagonal_positions:
                if (0 <= di < n and 0 <= dj < m and grid[di][dj] == ' ' and placed_tiles[tile1] < tile_counts[tile1]):
                    grid[di][dj] = tile1
                    placed_tiles[tile1] += 1
                    if placed_tiles[tile1] == tile_counts[tile1]:
                        break
            if placed_tiles[tile1] == tile_counts[tile1]:
                break

    if placed_tiles[tile2] < tile_counts[tile2]:
        for i, j in placed_positions:
            diagonal_positions = [
                (i-1, j-1), (i-1, j+1),
                (i+1, j-1), (i+1, j+1)
            ]
            for di, dj in diagonal_positions:
                if (0 <= di < n and 0 <= dj < m and grid[di][dj] == ' ' and placed_tiles[tile2] < tile_counts[tile2]):
                    grid[di][dj] = tile2
                    placed_tiles[tile2] += 1
                    if placed_tiles[tile2] == tile_counts[tile2]:
                        break
            if placed_tiles[tile2] == tile_counts[tile2]:
                break

    remaining_tiles = []
    for tile, count in tile_counts.items():
        remaining = count - placed_tiles[tile]
        remaining_tiles.extend([tile] * remaining)
    random.shuffle(remaining_tiles)

    for i in range(n):
        for j in range(m):
            if grid[i][j] == ' ' and remaining_tiles:
                grid[i][j] = remaining_tiles.pop()
                placed_tiles[grid[i][j]] += 1

    return grid

def no_adjcol(n, m, red, green, blue):
    """Generates a valid n x m grid with no two adjacent tiles having the same color."""
    def is_valid(grid, row, col, color, n, m):
        """Checks if placing the given color at (row, col) is valid."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < n and 0 <= c < m and grid[r][c] == color:
                return False  # Adjacent tile has the same color

        return True

    def solve(grid, row, col, color_counts, n, m):
        """Recursively fills the grid ensuring no two adjacent tiles have the same color."""
        if row == n:
            return True  # Successfully filled the entire grid

        next_row, next_col = (row, col + 1) if col + 1 < m else (row + 1, 0)

        for color in ['R', 'G', 'B']:
            if color_counts[color] > 0 and is_valid(grid, row, col, color, n, m):
                grid[row][col] = color  # Place color
                color_counts[color] -= 1

                if solve(grid, next_row, next_col, color_counts, n, m):
                    return True  # If valid solution found, return True

                grid[row][col] = None  # Backtrack
                color_counts[color] += 1

        return False  # No valid color found

    total_tiles = n * m
    if red + green + blue != total_tiles:
        print("Invalid input: Total number of tiles does not match grid size!")
        return None

    grid = [[None for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    if not solve(grid, 0, 0, color_counts, n, m):
        print("No valid grid configuration found!")
        return None

    return grid


def block_col(n, m, red, green, blue, block_color, block_size, block_count):
    """Generates a valid n × m grid with block_size × block_size blocks and fills remaining spaces randomly."""
    def place_blocks(grid, block_color, block_size, block_count, color_counts):
        """Places the required number of block_size × block_size blocks of a specific color in the grid."""
        required_tiles = block_count * (block_size ** 2)

        if required_tiles > color_counts[block_color]:
            print(f"Error: Not enough {block_color} tiles to form {block_count} blocks of size {block_size}×{block_size}.")
            return False

        placed_blocks = 0
        for _ in range(block_count):
            found = False
            for _ in range(100):
                row = random.randint(0, n - block_size)
                col = random.randint(0, m - block_size)

                if all(grid[r][c] is None for r in range(row, row + block_size) for c in range(col, col + block_size)):
                    for r in range(row, row + block_size):
                        for c in range(col, col + block_size):
                            grid[r][c] = block_color

                    placed_blocks += 1
                    color_counts[block_color] -= (block_size ** 2)
                    found = True
                    break

            if not found:
                print(f"Warning: Could not place all {block_count} blocks.")
                return False

        return True

    def fill_remaining_tiles(grid, color_counts):
        """Fills the remaining tiles randomly while ensuring total tile counts are met."""
        available_positions = [(r, c) for r in range(n) for c in range(m) if grid[r][c] is None]
        random.shuffle(available_positions)

        for color in ['R', 'G', 'B']:
            for _ in range(color_counts[color]):
                if available_positions:
                    row, col = available_positions.pop()
                    grid[row][col] = color

    total_tiles = n * m
    if red + green + blue != total_tiles:
        print("Error: The total number of tiles must be equal to n × m.")
        return None

    grid = [[None for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    if not place_blocks(grid, block_color, block_size, block_count, color_counts):
        return None

    fill_remaining_tiles(grid, color_counts)

    return grid
