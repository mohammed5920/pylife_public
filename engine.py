import numpy as np
import numba
from tqdm import tqdm

numba.config.CACHE_DIR = "__pycache__"
numba.config.THREADING_LAYER = "workqueue"

@numba.jit(nopython=True, nogil=True, cache=True)
def get_edge_neighbours(original_x, original_y, array : np.ndarray):
    width, height = array.shape[:2]
    result = 0
    for x in range(original_x - 1, original_x + 2):
        for y in range(original_y - 1, original_y + 2):
            if (x, y) == (original_x, original_y): 
                continue
            result += array[x % width, y % height, 0]
    return result
    
@numba.jit(nopython=True, parallel=True, nogil=True, cache=True)
def iterate_game(current_array : np.ndarray):
    next_array = np.zeros_like(current_array)
    width, height = current_array.shape[:2]
    for y in numba.prange(height):
        for x in range(width):
            if x in (0, width-1) or y in (0, height-1):
                neighbours = get_edge_neighbours(x, y, current_array)
            else:
                #unrolled because it's faster
                neighbours = current_array[x-1, y-1, 0] + \
                             current_array[x-1, y, 0] + \
                             current_array[x-1, y+1, 0] + \
                             current_array[x,   y-1, 0] + \
                             current_array[x,   y+1, 0] + \
                             current_array[x+1, y-1, 0] + \
                             current_array[x+1, y, 0] + \
                             current_array[x+1, y+1, 0]
            
            #game of life rules - if there are 3 neighbours or it's a live cell with 2-3 neighbours, it lives
            if neighbours == 3*255 or (current_array[x, y, 0] and neighbours == 2*255): 
                next_array[x, y] = 255 #all other cells are automatically dead
    return next_array

if __name__ == "__main__":
    SCALE = 1
    RESOLUTION = (3840 // SCALE, 2160 // SCALE)
    current_array = np.zeros((RESOLUTION[0], RESOLUTION[1], 3), np.uint8)
    for _ in tqdm(range(1000)):
        iterate_game(current_array)