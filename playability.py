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
from typing import List, Tuple, Dict
from itertools import combinations
import glob
import random
import copy

import numpy as np
# https://pypi.org/project/pathfinding/
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from PCGMM_Evaluation_Method.constant import tileTypes



# WALKABLE = ["F", "M", "O"]
# START_END = ["D", "S"]
# ALL_WALKABLE = WALKABLE + START_END

# OBSTACLE = ["B", "P", "I", "W", "-"]
# BRIDGEABLE = ["P"]

WALKABLE = ["F", "M", "-", "C"]
START_END = ["D", "S"]
# START_END = ["D", "S", "A"]
ALL_WALKABLE = WALKABLE + START_END

OBSTACLE = ["B", "P", "W"]
BRIDGEABLE = ["P"]
DOOR_REPLACEABLE = ["A", "N", "E", "U"]


# OBSTACLE = ["B", "I", "W", "-"]
# BRIDGEABLE = ["P"]

# def pathfinder_compatibility_conversion(file_name: str) -> Tuple[List, List[List[int]]]:
#     room_matrix = []
#     row_idx = 0
#     start_end = []
#     with open(file_name, 'r') as fp:
#         while True:
#             line = fp.readline()
#             if not line:
#                 break

#             room_line = []
#             for column_idx, tile in enumerate(line):
#                 if tile in OBSTACLE:
#                     room_line.append(0)
#                 elif tile in WALKABLE:
#                     room_line.append(1)
#                 elif tile in START_END:
#                     room_line.append(1)
#                     start_end.append((row_idx, column_idx))

#             row_idx = row_idx + 1
#             room_matrix.append(room_line)

#     return (start_end, room_matrix)

def select_real_start_end(start_end, room_matrix):
    result = {"D": [], "S": []}

    for k in start_end:
        for coor1 in start_end[k]:
            # print("-", coor1)
            is_add = True
            for coor2 in result[k]:
                # print("*", coor2)
                # up down left right
                if (coor1[0] == coor2[0] and coor1[1]-1 == coor2[1]) or \
                (coor1[0] == coor2[0] and coor1[1]+1 == coor2[1]) or \
                (coor1[1] == coor2[1] and coor1[0]-1 == coor2[0]) or \
                (coor1[1] == coor2[1] and coor1[0]+1 == coor2[0]):
                    is_add = False
                    break
                if (coor1[0] == coor2[0] and coor1[1]-2 == coor2[1]) or \
                (coor1[0] == coor2[0] and coor1[1]+2 == coor2[1]) or \
                (coor1[1] == coor2[1] and coor1[0]-2 == coor2[0]) or \
                (coor1[1] == coor2[1] and coor1[0]+2 == coor2[0]):
                    is_add = False
                    break
            
            if is_add:
                # print("add", coor1)
                result[k].append(coor1)
        # print("--",result)

    all_start_end = []
    for k in start_end:
        all_start_end = all_start_end + result[k]
    
    # print(all_start_end)
    if len(all_start_end) == 1:
        # if ony one door, at least can go inside room
        farest_loc = (-1,-1)
        farest_dist = 0
        for i in range(len(room_matrix)):
            for j in range(len(room_matrix[0])):
                if room_matrix[i][j] != 1:
                    continue
                
                dist = abs(i - all_start_end[0][0]) + abs(j - all_start_end[0][1])
                if dist > farest_dist:
                    farest_dist = dist
                    farest_loc = (i, j)

        result["D"].append(farest_loc)

    return result
            

def pathfinder_compatibility_conversion(room: np.ndarray) -> Tuple[List, List[List[int]]]:
    room_matrix = []
    start_end = {}

    # print(room)
    for i in range(room.shape[0]):
        room_line = []
        for j in range(room.shape[1]):
            tile = room[i, j]
            if tile in OBSTACLE:
                room_line.append(0)
            elif tile in WALKABLE:
                room_line.append(1)
            elif tile in START_END:
                room_line.append(1)
                # start_end.append((i, j))
                if tile not in start_end:
                    start_end[tile] = [(i, j)]
                else:
                    start_end[tile].append((i,j))
            # elif tile == "A":
            #     room_line.append(1)
            #     if tile not in start_end:
            #         start_end["D"] = [(i, j)]
            #     else:
            #         start_end["D"].append((i,j))

        room_matrix.append(room_line)

    return (start_end, room_matrix)

def read_file(file_name: str) -> Tuple[np.ndarray, bool]:
    room = []
    has_bridge_block = False

    with open(file_name, 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            room_line = []
            for tile in line:
                if tile in tileTypes: 
                    if tile in DOOR_REPLACEABLE:
                        room_line.append("D")
                    else:
                        room_line.append(tile)
                elif tile not in tileTypes and tile != '\n':
                    raise ValueError('new tile type = {}'.format(tile))

                if tile in BRIDGEABLE:
                    has_bridge_block = True

            room.append(room_line)
            
    
    return (np.asarray(room), has_bridge_block)

def is_playable(start_end: Dict, room_matrix: List[List[int]], print_path: bool=False) -> bool:
    # TODO: invesgate
    # if len(start_end) < 2:
    #     playable = True
    #     return playable

    all_start_end = []
    for k in start_end:
        all_start_end = all_start_end + start_end[k]

    grid = Grid(matrix=room_matrix)
    comb = list(combinations(all_start_end, 2))
    playable = True
    # random.shuffle(comb)

    for _start, _end in comb:
        # print(_start, _end)
        # hardcode here
        
        # if (_start in start_end["D"] and _end in start_end["D"]) or (_start in start_end["S"] and _end in start_end["S"]):
        #     abs_dis = abs(_start[0] - _end[0]) + abs(_start[1] - _end[1])
        #     if abs_dis < 4:
        #         continue
        
        
        start = grid.node(_start[1], _start[0])
        end = grid.node(_end[1], _end[0])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)

        if print_path and len(path) > 0:
            print('operations:', runs, 'path length:', len(path))
            print(grid.grid_str(path=path, start=start, end=end))
        
        grid.cleanup()

        if len(path) == 0:
            playable = False
            break

    return playable

def final_playable(start_end: Dict, room: np.ndarray, room_matrix: List[List[int]], has_bridge_block: bool) -> bool:
    playable = is_playable(start_end=start_end, room_matrix=room_matrix, print_path=False)
    # return playable
    # print(playable)
    # print(has_bridge_block)
    if playable == False and has_bridge_block:
        result = np.where(room=="P")
        # print(bridge_block_locs[0])
        listOfCoordinates= list(zip(result[0], result[1]))
        # print("before select candidates", listOfCoordinates)
        candidates_coor = select_candidates(listOfCoordinates, room)
        # print("after select candidates", candidates_coor)

        n = 1
        break_flag = False
        
        while True:
            # print(n)
            comb = list(combinations(candidates_coor, n))

            for coors in comb:
                room_matrix_2 = copy.deepcopy(room_matrix)
                # print(coors)
                if n == 1:
                    room_matrix_2[coors[0][0]][coors[0][1]] = 1
                    # playable = is_playable(start_end, room_matrix_2, print_path=True)
                    playable = is_playable(start_end, room_matrix_2, print_path=False)

                elif n > 1:
                    # check if the points has contact                    
                    if is_contact(coors):
                        continue

                    # if not is_connect_to_WALKABLE(coors, room):
                    #     continue
                    
                    for i in range(n):
                        room_matrix_2[coors[i][0]][coors[i][1]] = 1
                    
                    # playable = is_playable(start_end, room_matrix_2, print_path=True)
                    playable = is_playable(start_end, room_matrix_2, print_path=False)

                if playable == True:
                    # print(np.asarray(room_matrix_2))
                    return True
            
            n = n + 1
            if n > 5:
                return False
            # break
        # return playable
    else:
        return playable



def manhattan_distance(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))


def is_contact(list_loc) -> bool:
    # print(list_loc)
    
    comb = list(combinations(list_loc, 2))
    # print(comb)

    for i in range(len(comb)):
        loc1 = comb[i][0]
        loc2 = comb[i][1]
        # print(loc1)
        # print(loc2)
        if manhattan_distance(loc1, loc2) == 1:
            return True
        else:
            continue

    return False

def select_candidates(listOfCoordinates, room):
    candidates_coor = []

    for coors in listOfCoordinates:
        if is_connect_to_WALKABLE([coors], room):
            candidates_coor.append(coors)

    return candidates_coor

def is_connect_to_WALKABLE(list_loc, room):
    # print(list_loc)
    for x, y in list_loc:
        # print(x,y)
        if room[x-1, y] in ALL_WALKABLE and room[x+1, y] in ALL_WALKABLE:
            continue
        elif room[x, y-1] in ALL_WALKABLE and room[x, y+1] in ALL_WALKABLE:
            continue
        else:
            # print("haha")
            return False

    return True

def evaluate_playability(evaluate_data):
    unplayable_room= []
    playability = 0.0
    n = 0
    p = 0
    for i in range(evaluate_data.shape[0]):
        room = evaluate_data[i, :, :]
        
        # print(np.where(room == "P")[0].shape[0])
        # print(room[np.where(np.isin(room, BRIDGEABLE))].shape[0])
        if room[np.where(np.isin(room, BRIDGEABLE))].shape[0] > 0:
            has_bridge_block = True
        else:
            has_bridge_block = False

        # replace DOOR_REPLACABLE tile to door
        room[np.where(np.isin(room, DOOR_REPLACEABLE))] = "D"
        # print(room)

        try:
            start_end, room_matrix = pathfinder_compatibility_conversion(room)
            # print(room_matrix)
            start_end = select_real_start_end(start_end, room_matrix)
        except Exception as e:
            print("!"*10)
            print(e)
            print("room is not valid, idx={}".format(i))
            print(room)
            print("!"*10)

        playable = final_playable(start_end, room, room_matrix, has_bridge_block)
        # print(has_bridge_block)
        # print(playable)

        n = n + 1
        if playable:
            p = p + 1
        else:
            unplayable_room.append(room)

    playability = p / n
    
    return (unplayable_room, playability)

if __name__ == "__main__":
    """
        Question:
        Is void walkable? [m]aps/tloz6_1_room_16.txt]
        maps/tloz5_1_room_13.txt felt odd ??
    """

    ####### TEST SECTION ########
    # # file_name = 'tloz8_2_room_29.txt'
    # # file_name = 'tloz5_1_room_13.txt'
    # file_name = 'map_data/map_reduced_OI/tloz8_2_room_14.txt'
    # # file_name = 'tloz8_2_room_7.txt'
    # # file_name = 'unplayable_tloz9_2_room_6.txt'
    # # file_name = 'maps/tloz6_1_room_16.txt'

    # room, has_bridge_block = read_file(file_name)
    # start_end, room_matrix = pathfinder_compatibility_conversion(room)
    # print("start:", start_end)
    # start_end = select_real_start_end(start_end, room_matrix)
    # print("after select: ", start_end)
    # # print(np.matrix(room_matrix))
    # print(room)
    
    # playable = final_playable(start_end, room, room_matrix, has_bridge_block)
    # print("'{}' is playable: {}".format(file_name,playable))

    # '''
    # # try:
    # #     playable = is_playable(start_end, room_matrix, print_path=False)
    # # except:
    # #     print("{} is not right".format(file_name))
    # # print("'{}' is playable: {}".format(file_name,playable))
    # '''
    ##############################

    # files = glob.glob("map_data/map_reduced_OI/*.txt") # 0.9651
    # files = glob.glob("generate_map/generate_map_BMC_2/*.txt") #0.8025
    files = glob.glob("generate_map/generate_map_RM_2/*.txt")
    
    n = 0
    p = 0
    for file_name in files:
        # print(file_name)
        # print(n)
        try:
            room, has_bridge_block = read_file(file_name)
            # start_end, room_matrix = pathfinder_compatibility_conversion(file_name)
            start_end, room_matrix = pathfinder_compatibility_conversion(room)
            start_end = select_real_start_end(start_end, room_matrix)
        except Exception as e:
            print(file_name)
            print(e)
            break

        # print(start_end)
        # print(np.matrix(room_matrix))
        # try:
        # playable = is_playable(start_end, room_matrix, print_path=False)
        playable = final_playable(start_end, room, room_matrix, has_bridge_block)
        n = n + 1
        if playable:
            p = p + 1
        # except Exception as e:
        #     print("error: {} in file {}".format(str(e), file_name))

        # print("'{}' is playable: {}".format(file_name,playable))
        if not playable:
            print(file_name)
    print(p)
    print(n)
    print(p/n)
    

