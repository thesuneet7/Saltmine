def fill_grid_periphery(dimension, red, green, blue, periphery_colors):
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Define periphery positions
    periphery_positions = [(0, j) for j in range(dimension)] + [(dimension - 1, j) for j in range(dimension)] + \
                          [(i, 0) for i in range(1, dimension - 1)] + [(i, dimension - 1) for i in range(1, dimension - 1)]

    # Assign periphery colors
    index = 0
    for i, j in periphery_positions:
        if index < len(periphery_colors) and color_counts[periphery_colors[index]] > 0:
            grid[i][j] = periphery_colors[index]
            color_counts[periphery_colors[index]] -= 1
            index += 1
        else:
            # If selected periphery colors run out, use any available color
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
