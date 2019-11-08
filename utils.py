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