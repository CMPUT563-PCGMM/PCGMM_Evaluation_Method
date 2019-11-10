"""
    Tile Representation
    F = FLOOR
    B = BLOCK
    M = MONSTER
    P = ELEMENT (LAVA, WATER)
    O = ELEMENT + FLOOR (LAVA/BLOCK, WATER/BLOCK)
    I = ELEMENT + BLOCK
    D = DOOR
    S = STAIR
    W = WALL
    - = VOID
    
    walkable: F, M, O,
    obstacle: B, P, I, W, -
    start/end: D, S 
"""
from typing import List, Tuple
from itertools import combinations
import glob
import random
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


WALKABLE = ["F", "M", "O"]
OBSTACLE = ["B", "P", "I", "W", "-"]
START_END = ["D", "S"]

def pathfinder_compatibility_conversion(file_name: str) -> Tuple[List, List[List[int]]]:
    room_matrix = []
    row_idx = 0
    start_end = []
    with open(file_name, 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            room_line = []
            for column_idx, tile in enumerate(line):
                if tile in OBSTACLE:
                    room_line.append(0)
                elif tile in WALKABLE:
                    room_line.append(1)
                elif tile in START_END:
                    room_line.append(1)
                    start_end.append((row_idx, column_idx))

            row_idx = row_idx + 1
            room_matrix.append(room_line)

    return (start_end, room_matrix)

def is_playable(start_end: List, room_matrix: List[List[int]], print_path: bool=False) -> bool:
    if len(start_end) < 2:
        playable = True

        return playable

    grid = Grid(matrix=room_matrix)
    comb = list(combinations(start_end, 2))
    playable = True
    # random.shuffle(comb)

    for _start, _end in comb:
        # print(_start, _end)
        abs_dis = abs(_start[0] - _end[0]) + abs(_start[1] - _end[1])
        if abs_dis < 2:
            continue
        
        start = grid.node(_start[1], _start[0])
        end = grid.node(_end[1], _end[0])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)

        if print_path:
            print('operations:', runs, 'path length:', len(path))
            print(grid.grid_str(path=path, start=start, end=end))
        
        grid.cleanup()

        if len(path) == 0:
            playable = False
            break

    return playable



if __name__ == "__main__":
    """
        Question:
        Is void walkable? [m]aps/tloz6_1_room_16.txt]
        maps/tloz5_1_room_13.txt felt odd ??
    """

    ####### TEST SECTION ########
    # # file_name = 'tloz9_2_room_6.txt'
    # # file_name = 'unplayable_tloz9_2_room_6.txt'
    # file_name = 'maps/tloz6_1_room_16.txt'
    # start_end, room_matrix = pathfinder_compatibility_conversion(file_name)
    # print(start_end)
    # print(np.matrix(room_matrix))
    # try:
    #     playable = is_playable(start_end, room_matrix)
    # except:
    #     print("{} is not right".format(file_name))
    # print("'{}' is playable: {}".format(file_name,playable))
    ##############################

    files = glob.glob("generate_map_BMC/*.txt")
    n = 0
    p = 0
    for file_name in files:
        start_end, room_matrix = pathfinder_compatibility_conversion(file_name)
        # print(start_end)
        # print(np.matrix(room_matrix))
        try:
            playable = is_playable(start_end, room_matrix, print_path=False)
            n = n + 1
            if playable:
                p = p + 1
        except Exception as e:
            print("error: {} in file {}".format(str(e), file_name))

        print("'{}' is playable: {}".format(file_name,playable))
    print(p/n)
    

