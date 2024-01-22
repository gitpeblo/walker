import random
import numpy as np
import os

def create_simple_map(width, height, p_hole=1):
    '''Generates a map predominantly filled with 1s (tiles), and, in a
     minor amount (less than 50%), 0s (holes).
    
    The generation procedure happens in 2 steps:
        1- A map is initialized only with 1s.
        2- Some 1s are randomly replaced by 0s.
           In this phase, a check is performed to ensure that paths remain
           wide (no adjecent 0s).

    The predominancy of 1 is can be controlled by the probability to replace a
    tile with a hole (`p_hole`).  When `p_hole` is max (=1), 50% of the tiles
    are holes.

    Parameters
    ----------
    width : int
        Desired map width in pixels.
    height : int
        Desired map height in pixels.
    p_hole : float, range: [0, 1]
        Probability to replace a tile with a hole.

    Returns
    -------
    map_data : np.ndarray, dtype: int
        A 2D array containing 1s and 0s.
    '''

    # Step 1: Initialize a grid filled with 1s:
    map_data = np.ones((height, width), dtype=int)

    # Step 2: Random 0s placement:
    for row in range(height):
        for col in range(width):
            if random.random() < p_hole:
                # Ensuring barriers are not adjacent to each other:
                if (row > 0 and map_data[row-1, col] == 0)\
                or (col > 0 and map_data[row, col-1] == 0):
                    continue
                map_data[row, col] = 0

    return map_data

def create_traversable_map(height, width, p_tile=0.3):
    '''Generates a left-to-right traversable map, i.e. a map which contains at
    least one path that crosses the map horizontally.
    The 1s represent traversable tiles and the 0s represent holes.

    The generation procedure happens in 3 steps:
        1- A map is initialized only with 0s.
        2- A guaranteed path is constructed while trasversing the map
           horizontally.
        3- Some 0s are additionally randomly replaced by 1s.
           The predominancy of 1 is can be controlled by the probability to
           replace a [non-guaranteed-path] hole with a tile (`p_tile`).
           When `p_tile` is max (=1), all the map locations are tiles (1s).

    Parameters
    ----------
    width : int
        Desired map width in pixels.
    height : int
        Desired map height in pixels.
    p_tile : float, range: [0, 1]
        Probability to replace [non-guaranteed-path] hole with a tile.

    Returns
    -------
    map_data : np.ndarray, dtype: int
        A 2D array containing 1s and 0s.
    '''

    waypoints = []
    # list of [x_map, y_map] waypoints of the traversable path

    # Step 1: Initialize a grid filled with 0s:
    map_data = np.zeros((height, width), dtype=int)

    # Step 2: Randomly create a guaranteed path, left to right:
    row = np.random.choice(range(height))
    # randomly initialize path along the left edge
    for col in range(width):
        # Move up, down, or stay in the same row:
        row += random.choice([-1, 0, 1])
        # Ensure the path does not go out of the map:
        row = max(0, min(height - 1, row))
        # Ensure the path cell is traversable:
        map_data[row][col] = 1
        # Store waypoint:
        waypoints.append([row, col])

    # Step 3: Randomly place some additional traversable tile (1s):
    for row in range(height):
        for col in range(width):
            if map_data[row][col] == 0 and random.random() < p_tile:
                map_data[row][col] = 1

    # TODO: Return waypoints and use them to get the start and goal

    return map_data

def write_map_to_file(map_data, path_to_basename):
    '''
    Writes map data to a text file.

    Parameters
    ----------
    map_data : np.ndarray, dtype: int
        A 2D array containing 1s and 0s.

    path_to_basename : str
        Path to the desired basename of the file: it will be renamed with
        sequential integers (i.e., ..._0.txt, ..._1.txt, etc.), according to
        the already existing maps in the target folder.

    Returns
    -------
    path_to_map : str
        Path to the saved map.
    '''

    # Get a unique filename for the map:
    path_to_map = get_unique_filename(path_to_basename)

    # Convert map to text:
    map_data_text = \
        "\n".join("".join(str(cell) for cell in row) for row in map_data)

    # Write to file:
    with open(path_to_map, 'w') as file:
        file.write(map_data_text)

    return path_to_map
    
def get_unique_filename(path_to_basename):
    '''
    Generates a unique filename in the specified directory by appending an
    integer suffix to the base filename.

    The function looks for existing files with the same basename in the target
    directory, and appends a sequential integer in order to obtain a unique
    filename.

    Parameters
    ----------
    path_to_basename : str
        Desired filename base (and associated path).

    Returns
    -------
    unique_filename : str
        The modified path to the unique filename.
    '''

    directory = os.path.dirname(path_to_basename)
    filename = os.path.basename(path_to_basename)

    root, extension = os.path.splitext(filename)
    counter = 0
    unique_filename = f"{root}_{counter}{extension}"

    # Loop to find a unique filename:
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{root}_{counter}{extension}"
        counter += 1

    path_to_unique_filename = directory + '/' + unique_filename

    return path_to_unique_filename
