import glob

import numpy as np
from typing import Dict

def readMaps(tileTypes: Dict[str, str], maps_path: str):
    maps_lst = []

    files = glob.glob(maps_path + "/*.txt")
    for fileName in files:
        # print(fileName)
        map = []
        # Read this map
        map_f = open(fileName, 'r')
        # print(fileName)
        for row in map_f:
            row_chars = []
            for char in row.rstrip():
                if char not in tileTypes:
                    print('Invalid char')
                    print(char)
                row_chars.append(char)
            map.append(row_chars)

        map_arr = np.asarray(map, dtype=str)
        maps_lst.append(map_arr)
        # maps_lst = np.asarray(maps_lst, dtype=str)

    return maps_lst


def manhattan_distance(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

def compute_room_histogram(room: np.ndarray) -> Dict[str, int]:
    hist = {
        "F": 0,
        "B": 0,
        "M": 0,
        "P": 0,
        "S": 0,
        "-": 0,
        "C": 0
    }

    ignore = ["D", "W", "A", "N", "E", "U"]
    
    unique_elements, counts_elements = np.unique(room, return_counts=True)
    for idx, c in enumerate(unique_elements):
        if c in ignore:
            continue
        hist[c] = counts_elements[idx]
    return hist

def compute_room_list_histogram(room_list: np.ndarray) -> np.ndarray:
    hist_list = []
    for i in range(room_list.shape[0]):
        hist_list.append(list(compute_room_histogram(room_list[i, :, :]).values()))

    # print(hist_list.shape)
    return np.asarray(hist_list)
