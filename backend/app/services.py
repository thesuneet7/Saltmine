def fill_grid_periphery(n, m, red, green, blue, periphery_colors):
        grid = [[None] * m for _ in range(n)]  # Create a grid with the specified n and columns
        color_counts = {'R': red, 'G': green, 'B': blue}

        # Define periphery positions
        periphery_positions = [(0, j) for j in range(m)] + [(n - 1, j) for j in range(m)] + \
                            [(i, 0) for i in range(1, n - 1)] + [(i, m - 1) for i in range(1, n - 1)]

        # Shuffle the periphery positions for randomness
        random.shuffle(periphery_positions)

        # Assign periphery colors
        index = 0
        for i, j in periphery_positions:
            if index < len(periphery_colors) and color_counts[periphery_colors[index]] > 0:
                grid[i][j] = periphery_colors[index]
                color_counts[periphery_colors[index]] -= 1
                index += 1
            else:
                # If selected periphery colors run out, shuffle available colors and use one
                available_colors = [color for color in 'RGB' if color_counts[color] > 0]
                random.shuffle(available_colors)  # Shuffle the available colors
                for color in available_colors:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

        # Collect remaining positions for filling (inside grid)
        remaining_positions = [(i, j) for i in range(n) for j in range(m) if grid[i][j] is None]

        # Shuffle the remaining positions
        random.shuffle(remaining_positions)

        # Create a list of available colors based on the remaining counts
        available_colors = []
        for color, count in color_counts.items():
            available_colors.extend([color] * count)

        # Shuffle the available colors
        random.shuffle(available_colors)

        # Fill the remaining positions with shuffled colors
        for pos, color in zip(remaining_positions, available_colors):
            i, j = pos
            grid[i][j] = color

        return grid

def fill_grid_diagonal(dimension, red, green, blue, diagonal_colors):
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Check if we have exactly the right number of colors to fill the grid
    total_cells = dimension * dimension
    total_colors = red + green + blue

    if total_colors != total_cells:
        return None  # Incorrect number of colors

    # Get all diagonal positions (both main diagonal and anti-diagonal)
    main_diagonal = [(i, i) for i in range(dimension)]
    anti_diagonal = [(i, dimension-1-i) for i in range(dimension)]

    # Remove duplicates (center cell in odd-sized grids)
    all_diagonal_positions = []
    for pos in main_diagonal + anti_diagonal:
        if pos not in all_diagonal_positions:
            all_diagonal_positions.append(pos)

    # First, try to fill all diagonal positions according to priority order
    for i, j in all_diagonal_positions:
        filled = False
        # Try each color in the priority list
        for priority_color in diagonal_colors:
            if color_counts[priority_color] > 0:
                grid[i][j] = priority_color
                color_counts[priority_color] -= 1
                filled = True
                break

        # If no priority color is available, try any color
        if not filled:
            for color in 'RGB':
                if color_counts[color] > 0:
                    grid[i][j] = color
                    color_counts[color] -= 1
                    filled = True
                    break

    # Then fill the rest of the grid
    for i in range(dimension):
        for j in range(dimension):
            if grid[i][j] is None:
                for color in 'RGB':
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

    # Check if all cells are filled
    for i in range(dimension):
        for j in range(dimension):
            if grid[i][j] is None:
                return None  # Could not fill the entire grid

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

import sys
import random

def patternn(n, m, red, green, blue, pattern_length, pattern):
    """Generates an n × m grid using the specified tile pattern and fills remaining spaces randomly."""
    def max_patterns(X, Y, Z, pattern):
        x = pattern.count('R')
        y = pattern.count('G')
        z = pattern.count('B')
        x = X // x if x > 0 else float('inf')
        y = Y // y if y > 0 else float('inf')
        z = Z // z if z > 0 else float('inf')
        return min(x, y, z)

    def fill_with_patterns(grid, pattern, pattern_length, color_counts, n, m, max_patterns):
        row, applied_patterns = 0, 0
        while applied_patterns < max_patterns and row < n:
            for start_col in range(0, m, pattern_length):
                end_col = start_col + pattern_length
                if end_col > m:
                    break
                pattern_slice = list(pattern[:end_col - start_col])
                if all(color_counts[color] >= pattern_slice.count(color) for color in pattern_slice):
                    grid[row][start_col:end_col] = pattern_slice
                    for color in pattern_slice:
                        color_counts[color] -= 1
                    applied_patterns += 1
                if applied_patterns >= max_patterns:
                    return
            row += 1

    def fill_remaining(grid, color_counts, n, m):
        available_tiles = [color for color, count in color_counts.items() for _ in range(count)]
        random.shuffle(available_tiles)
        tile_index = 0
        for row in range(n):
            for col in range(m):
                if grid[row][col] is None and tile_index < len(available_tiles):
                    grid[row][col] = available_tiles[tile_index]
                    tile_index += 1

    total_tiles = n * m
    given_tiles = red + green + blue
    if given_tiles != total_tiles:
        print("\n❌ Invalid Configuration: The total number of tiles does not match the grid size!")
        sys.exit(1)
    if pattern_length > m:
        print("\n❌ This configuration cannot be possible! The pattern length exceeds the number of columns.")
        sys.exit(1)
    if len(pattern) != pattern_length:
        print("\n❌ Invalid Pattern: The specified pattern length does not match the given pattern!")
        sys.exit(1)

    max_patterns_count = max_patterns(red, green, blue, pattern)
    print(f"\n✅ Maximum number of patterns that can be formed: {max_patterns_count}")
    if max_patterns_count == 0:
        print("\n❌ This configuration cannot be possible!")
        sys.exit(1)
    
    grid = [[None for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    
    fill_with_patterns(grid, pattern, pattern_length, color_counts, n, m, max_patterns_count)
    fill_remaining(grid, color_counts, n, m)
    
    return grid

def periphery_diagonal(dimension, red, green, blue, periphery_colors, diagonal_colors, constraint_priority="diagonal"):
    def initialize_grid():
        return [[None] * dimension for _ in range(dimension)]

    def get_positions():
        periphery = [(0, j) for j in range(dimension)] + \
                    [(i, dimension - 1) for i in range(1, dimension)] + \
                    [(dimension - 1, j) for j in range(dimension - 2, -1, -1)] + \
                    [(i, 0) for i in range(dimension - 2, 0, -1)]
        diagonal = list(set([(i, i) for i in range(dimension)] + [(i, dimension - 1 - i) for i in range(dimension)]))
        return periphery, diagonal

    def assign_priority():
        return [(diagonal_positions, diagonal_colors), (periphery_positions, periphery_colors)] if constraint_priority == "diagonal" else [(periphery_positions, periphery_colors), (diagonal_positions, diagonal_colors)]

    def fill_positions(priority_order):
        for positions, color_priority in priority_order:
            if not color_priority:
                continue
            for i, j in positions:
                if grid[i][j] is not None:
                    continue
                assigned = False
                for color in color_priority:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        assigned = True
                        break
                if not assigned:
                    for color in 'RGB':
                        if color_counts[color] > 0:
                            grid[i][j] = color
                            color_counts[color] -= 1
                            break

    def fill_remaining():
        for i in range(dimension):
            for j in range(dimension):
                if grid[i][j] is None:
                    for color in 'RGB':
                        if color_counts[color] > 0:
                            grid[i][j] = color
                            color_counts[color] -= 1
                            break

    grid = initialize_grid()
    color_counts = {'R': red, 'G': green, 'B': blue}
    periphery_positions, diagonal_positions = get_positions()
    priority_order = assign_priority()
    fill_positions(priority_order)
    fill_remaining()
    return grid

def diagonal_adj(dimension, red, green, blue, diagonal_colors, adjacency_cons):
    def fill_grid():
        total_cells = dimension * dimension
        total_colors = red + green + blue

        if total_colors != total_cells:
            print("Error: Incorrect number of colors.")
            return None

        color_counts.update({'R': red, 'G': green, 'B': blue})
        main_diagonal = [(i, i) for i in range(dimension)]
        anti_diagonal = [(i, dimension - 1 - i) for i in range(dimension)]
        all_diagonal_positions = list(dict.fromkeys(main_diagonal + anti_diagonal))
        random.shuffle(all_diagonal_positions)

        for i, j in all_diagonal_positions:
            filled = False
            for priority_color in diagonal_colors:
                if color_counts[priority_color] > 0:
                    grid[i][j] = priority_color
                    color_counts[priority_color] -= 1
                    filled = True
                    break

            if not filled:
                available_colors = [c for c in 'RGB' if color_counts[c] > 0]
                random.shuffle(available_colors)
                for color in available_colors:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

    def violates_adjacency(row, col, tile):
        adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        other_colors = {'R', 'G', 'B'} - set(adjacency_cons)
        same_adjacent_count = 0

        for r, c in adjacent_positions:
            if 0 <= r < dimension and 0 <= c < dimension:
                if grid[r][c] == tile:
                    return True
                if grid[r][c] in other_colors:
                    same_adjacent_count += 1

        return same_adjacent_count >= 2

    def fill_with_adjacency():
        tile1, tile2 = sorted(adjacency_cons, key=lambda x: color_counts[x])
        tile1_positions = []
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)

        for i, j in empty_positions[:]:
            if color_counts[tile1] > 0 and not violates_adjacency(i, j, tile1):
                grid[i][j] = tile1
                color_counts[tile1] -= 1
                tile1_positions.append((i, j))
                empty_positions.remove((i, j))
                adjacent_positions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                random.shuffle(adjacent_positions)

                for ai, aj in adjacent_positions:
                    if (0 <= ai < dimension and 0 <= aj < dimension and grid[ai][aj] is None and color_counts[tile2] > 0):
                        grid[ai][aj] = tile2
                        color_counts[tile2] -= 1
                        empty_positions.remove((ai, aj))

        for i, j in tile1_positions:
            diagonal_positions = [(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
            for di, dj in diagonal_positions:
                if (0 <= di < dimension and 0 <= dj < dimension and grid[di][dj] is None and color_counts[tile1] > 0):
                    grid[di][dj] = tile1
                    color_counts[tile1] -= 1
                    empty_positions.remove((di, dj))
                    if color_counts[tile1] == 0:
                        break
            if color_counts[tile1] == 0:
                break

        remaining_tiles = [tile for tile, count in color_counts.items() for _ in range(count)]
        random.shuffle(remaining_tiles)

        for i, j in empty_positions:
            if remaining_tiles:
                grid[i][j] = remaining_tiles.pop()

    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {}

    fill_grid()
    if None in [tile for row in grid for tile in row]:
        fill_with_adjacency()

    return grid

import random

def periphery_bb(n, m, red, green, blue, periphery_colors, block_color, block_size, block_count):
    if n * m != red + green + blue:
        print("Error: The total number of colored cells does not match the grid size!")
        return []
    
    grid = [[' ' for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    positions = [(0, i) for i in range(m)] + [(n - 1, i) for i in range(m)] + [(i, 0) for i in range(1, n - 1)] + [(i, m - 1) for i in range(1, n - 1)]
    random.shuffle(positions)
    
    for color in periphery_colors:
        for x, y in positions:
            if grid[x][y] == ' ' and color_counts.get(color, 0) > 0:
                grid[x][y] = color
                color_counts[color] -= 1
    
    max_possible_blocks = min(block_count, color_counts.get(block_color, 0) // (block_size ** 2))
    placed_blocks = 0
    row_index = 1
    
    while row_index + block_size - 1 < n - 1 and placed_blocks < max_possible_blocks:
        col_index = 1
        while col_index + block_size - 1 < m - 1 and placed_blocks < max_possible_blocks:
            if all(grid[r][c] == ' ' for r in range(row_index, row_index + block_size) for c in range(col_index, col_index + block_size)):
                for r in range(row_index, row_index + block_size):
                    for c in range(col_index, col_index + block_size):
                        grid[r][c] = block_color
                placed_blocks += 1
                color_counts[block_color] -= (block_size ** 2)
            col_index += block_size
        row_index += block_size
    
    if placed_blocks < block_count:
        print(f"Warning: Could only place {placed_blocks} out of {block_count} blocks.")
    
    empty_positions = [(r, c) for r in range(n) for c in range(m) if grid[r][c] == ' ']
    random.shuffle(empty_positions)
    
    for r, c in empty_positions:
        available_colors = [color for color in color_counts if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[r][c] = chosen_color
            color_counts[chosen_color] -= 1
    
    return grid

def diagonal_periphery_pattern(dimension, red, green, blue, periphery_colors, diagonal_colors):
    total_cells = dimension * dimension
    if red + green + blue != total_cells:
        print(f"Error: The sum of tiles must equal {total_cells} (dimension²). Please try again.")
        exit()
    total_cells = dimension * dimension
    
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    periphery_positions = []
    for j in range(dimension):
        periphery_positions.append((0, j))
    for i in range(1, dimension):
        periphery_positions.append((i, dimension - 1))
    for j in range(dimension - 2, -1, -1):
        periphery_positions.append((dimension - 1, j))
    for i in range(dimension - 2, 0, -1):
        periphery_positions.append((i, 0))

    main_diagonal = [(i, i) for i in range(dimension)]
    anti_diagonal = [(i, dimension - 1 - i) for i in range(dimension)]
    all_diagonal_positions = main_diagonal + anti_diagonal

    diagonal_index = 0
    for pos in all_diagonal_positions:
        i, j = pos
        if grid[i][j] is not None:
            continue
        if diagonal_colors and diagonal_index < len(diagonal_colors) and color_counts[diagonal_colors[diagonal_index]] > 0:
            grid[i][j] = diagonal_colors[diagonal_index]
            color_counts[diagonal_colors[diagonal_index]] -= 1
        else:
            for color in 'RGB':
                if color_counts[color] > 0:
                    grid[i][j] = color
                    color_counts[color] -= 1
                    break
        diagonal_index = (diagonal_index + 1) % len(diagonal_colors) if diagonal_colors else 0

    periphery_index = 0
    for pos in periphery_positions:
        i, j = pos
        if grid[i][j] is not None:
            continue
        if periphery_colors and periphery_index < len(periphery_colors) and color_counts[periphery_colors[periphery_index]] > 0:
            grid[i][j] = periphery_colors[periphery_index]
            color_counts[periphery_colors[periphery_index]] -= 1
        else:
            for color in 'RGB':
                if color_counts[color] > 0:
                    grid[i][j] = color
                    color_counts[color] -= 1
                    break
        periphery_index = (periphery_index + 1) % len(periphery_colors) if periphery_colors else 0

    empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
    random.shuffle(empty_positions)
    
    remaining_colors = []
    for _ in range(color_counts['R']):
        remaining_colors.append('R')
    for _ in range(color_counts['G']):
        remaining_colors.append('G')
    for _ in range(color_counts['B']):
        remaining_colors.append('B')
    random.shuffle(remaining_colors)
    
    for i, (x, y) in enumerate(empty_positions):
        grid[x][y] = remaining_colors[i]

    return grid

def diagonal_periphery_priority(dimension, red, green, blue, periphery_colors, diagonal_colors, constraint_priority):
    def initialize_grid():
        return [[None] * dimension for _ in range(dimension)]

    def get_positions():
        periphery = [(0, j) for j in range(dimension)] + \
                    [(i, dimension - 1) for i in range(1, dimension)] + \
                    [(dimension - 1, j) for j in range(dimension - 2, -1, -1)] + \
                    [(i, 0) for i in range(dimension - 2, 0, -1)]
        diagonal = list(set([(i, i) for i in range(dimension)] + [(i, dimension - 1 - i) for i in range(dimension)]))
        random.shuffle(periphery)
        random.shuffle(diagonal)
        return periphery, diagonal

    def assign_priority():
        return [(diagonal_positions, diagonal_colors), (periphery_positions, periphery_colors)] if constraint_priority == "diagonal" else [(periphery_positions, periphery_colors), (diagonal_positions, diagonal_colors)]

    def fill_positions(priority_order):
        for positions, color_priority in priority_order:
            if not color_priority:
                continue
            for i, j in positions:
                if grid[i][j] is not None:
                    continue
                assigned = False
                for color in color_priority:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        assigned = True
                        break
                if not assigned:
                    for color in 'RGB':
                        if color_counts[color] > 0:
                            grid[i][j] = color
                            color_counts[color] -= 1
                            break

    def fill_remaining():
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)
        available_colors = ['R'] * color_counts['R'] + ['G'] * color_counts['G'] + ['B'] * color_counts['B']
        random.shuffle(available_colors)
        
        for (i, j), color in zip(empty_positions, available_colors):
            grid[i][j] = color

    if red + green + blue != dimension * dimension:
        raise ValueError(f"Error: The sum of tiles must equal {dimension * dimension} (dimension²). Please try again.")

    grid = initialize_grid()
    color_counts = {'R': red, 'G': green, 'B': blue}
    periphery_positions, diagonal_positions = get_positions()
    priority_order = assign_priority()
    fill_positions(priority_order)
    fill_remaining()
    return grid

def periphery_pattern(n, m, red, green, blue, periphery_colors, pattern_length, pattern):
    if n * m != red + green + blue:
        return "Error: The total number of colored cells does not match the grid size!", 0
    if pattern_length > m:
        return "\n❌ This configuration cannot be possible! The pattern length exceeds the number of columns.", 0
    if len(pattern) != pattern_length:
        return "\n❌ Invalid Pattern: The specified pattern length does not match the given pattern!", 0

    def max_patterns_count(color_counts, pattern):
        pattern_color_counts = {color: pattern.count(color) for color in set(pattern)}
        return min(
            (color_counts.get(color, 0) // count if count > 0 else float('inf'))
            for color, count in pattern_color_counts.items()
        )

    def fill_remaining(grid, color_counts):
        empty_positions = [(r, c) for r in range(n) for c in range(m) if grid[r][c] == ' ']
        random.shuffle(empty_positions)
        for r, c in empty_positions:
            available_colors = [color for color in color_counts if color_counts[color] > 0]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[r][c] = chosen_color
                color_counts[chosen_color] -= 1

    def fill_with_patterns(grid, pattern, max_patterns_count):
        applied_patterns = 0
        row_positions = list(range(1, n - 1))
        random.shuffle(row_positions)
        
        for r in row_positions:
            if applied_patterns >= max_patterns_count:
                break
            col_positions = list(range(0, m - pattern_length + 1))
            random.shuffle(col_positions)
            for start_col in col_positions:
                end_col = start_col + pattern_length
                if applied_patterns >= max_patterns_count:
                    break
                if all(grid[r][c] == ' ' for c in range(start_col, end_col)):
                    for i, color in enumerate(pattern):
                        grid[r][start_col + i] = color
                        color_counts[color] -= 1
                    applied_patterns += 1
        return applied_patterns

    def fill_periphery(grid):
        positions = [(0, i) for i in range(m)] + [(n - 1, i) for i in range(m)] + [(i, 0) for i in range(1, n - 1)] + [(i, m - 1) for i in range(1, n - 1)]
        random.shuffle(positions)
        for color in periphery_colors:
            for x, y in positions:
                if grid[x][y] == ' ' and color_counts.get(color, 0) > 0:
                    grid[x][y] = color
                    color_counts[color] -= 1

    grid = [[' ' for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    if max_patterns_count(color_counts, pattern) == 0:
        return "\n❌ This configuration cannot be possible!", 0

    fill_periphery(grid)
    patterns_applied = fill_with_patterns(grid, pattern, max_patterns_count(color_counts, pattern))
    fill_remaining(grid, color_counts)

    print(f"\nTotal patterns applied: {patterns_applied}")

    return grid

def periphery_nonadj(n, m, red, green, blue, periphery_colors):
    """Generates a valid grid based on user input."""

    def is_valid(grid, x, y, color):
        """Check if placing color at (x, y) does not touch the same color."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        return all(
            not (0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]) and grid[x + dx][y + dy] == color)
            for dx, dy in directions
        )

    def fill_grid(grid, color_counts):
        """Fills the grid with colors based on given constraints."""
        positions = [(0, i) for i in range(m)] + [(n - 1, i) for i in range(m)] + \
                    [(i, 0) for i in range(1, n - 1)] + [(i, m - 1) for i in range(1, n - 1)]
        
        random.shuffle(positions)
        
        # Place colors in periphery first
        for color in periphery_colors:
            for x, y in positions:
                if grid[x][y] == ' ' and color_counts[color] > 0:
                    grid[x][y] = color
                    color_counts[color] -= 1

        # Fill remaining positions
        empty_positions = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == ' ']
        random.shuffle(empty_positions)
        
        for x, y in empty_positions:
            for color in random.sample(['R', 'G', 'B'], 3):
                if color_counts[color] > 0 and is_valid(grid, x, y, color):
                    grid[x][y] = color
                    color_counts[color] -= 1
                    break
        
        # Final pass to fill any remaining empty spaces
        empty_positions = [(i, j) for i in range(n) for j in range(m) if grid[i][j] == ' ']
        random.shuffle(empty_positions)
        
        for x, y in empty_positions:
            for color in random.sample(['R', 'G', 'B'], 3):
                if color_counts[color] > 0:
                    grid[x][y] = color
                    color_counts[color] -= 1
                    break

    if n * m != red + green + blue:
        print("Error: The total number of colored cells does not match the grid size!")
        return None

    grid = [[' ' for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    
    fill_grid(grid, color_counts)

    return grid

def adj_dia_peri(dimension, red, green, blue, periphery_colors, diagonal_colors, adjacent_tiles):
    if dimension < 2:
        raise ValueError("Dimension must be at least 2")
    if any(c < 0 for c in (red, green, blue)):
        raise ValueError("Tile counts must be non-negative")
    
    def initialize_grid_and_counts():
        """Initialize an empty grid and color counts dictionary"""
        return [[None] * dimension for _ in range(dimension)], {'R': red, 'G': green, 'B': blue}

    def get_positions():
        """Get periphery and diagonal positions"""
        periphery = [(0, j) for j in range(dimension)] + \
                    [(i, dimension - 1) for i in range(1, dimension)] + \
                    [(dimension - 1, j) for j in range(dimension - 2, -1, -1)] + \
                    [(i, 0) for i in range(dimension - 2, 0, -1)]
        diagonal = list(dict.fromkeys([(i, i) for i in range(dimension)] +
                                      [(i, dimension - 1 - i) for i in range(dimension)]))
        return periphery, diagonal

    def fill_periphery(grid, periphery_positions, color_counts):
        """Fill periphery with available colors, prioritizing periphery_colors"""
        random.shuffle(periphery_positions)
        for i, j in periphery_positions:
            if grid[i][j] is None and periphery_colors and color_counts[periphery_colors[0]] > 0:
                grid[i][j] = periphery_colors[0]
                color_counts[periphery_colors[0]] -= 1

    def fill_diagonal(grid, diagonal_positions, color_counts):
        """Fill diagonal with available B tiles"""
        random.shuffle(diagonal_positions)
        for i, j in diagonal_positions:
            if grid[i][j] is None and diagonal_colors and color_counts[diagonal_colors[0]] > 0:
                grid[i][j] = diagonal_colors[0]
                color_counts[diagonal_colors[0]] -= 1

    def ensure_adjacency(grid, color_counts, tile1, tile2):
        """Ensure tile1 and tile2 are adjacent where possible"""
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)
        pairs_needed = min(color_counts[tile1], color_counts[tile2])

        for _ in range(pairs_needed):
            for i, j in empty_positions[:]:
                if color_counts[tile1] > 0:
                    grid[i][j] = tile1
                    color_counts[tile1] -= 1
                    empty_positions.remove((i, j))
                    adjacent_positions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    random.shuffle(adjacent_positions)
                    for ai, aj in adjacent_positions:
                        if (0 <= ai < dimension and 0 <= aj < dimension and
                            grid[ai][aj] is None and color_counts[tile2] > 0):
                            grid[ai][aj] = tile2
                            color_counts[tile2] -= 1
                            empty_positions.remove((ai, aj))
                            break
                    break

    def fill_remaining(grid, color_counts):
        """Fill remaining positions with exact counts"""
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        remaining_tiles = [tile for tile, count in color_counts.items() for _ in range(count)]
        random.shuffle(remaining_tiles)
        
        valid_colors = ['R', 'G', 'B']
        while len(remaining_tiles) < len(empty_positions):
            remaining_tiles.append(random.choice(valid_colors))
        
        for (i, j), tile in zip(empty_positions, remaining_tiles[:len(empty_positions)]):
            grid[i][j] = tile

    # Validate constraints
    total_cells = dimension * dimension
    valid_colors = {'R', 'G', 'B'}
    if not all(c in valid_colors for c in periphery_colors + diagonal_colors + adjacent_tiles):
        raise ValueError("Invalid colors detected. Use only R, G, B.")
    if len(adjacent_tiles) != 2:
        raise ValueError("Exactly 2 adjacent tiles required.")
    if red + green + blue != total_cells:
        raise ValueError(f"Color counts ({red + green + blue}) don't match grid size ({total_cells}).")

    # Generate one grid with randomization for variety
    grid, color_counts = initialize_grid_and_counts()
    periphery_positions, diagonal_positions = get_positions()

    fill_periphery(grid, periphery_positions, color_counts)
    fill_diagonal(grid, diagonal_positions, color_counts)
    ensure_adjacency(grid, color_counts, adjacent_tiles[0], adjacent_tiles[1])
    fill_remaining(grid, color_counts)

    return grid
