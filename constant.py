import os

# tileTypes = {
#     "F": "FLOOR",
#     "B": "BLOCK",
#     "M": "MONSTER",
#     "P": "ELEMENT (LAVA, WATER)",
#     "O": "ELEMENT + FLOOR (LAVA/BLOCK, WATER/BLOCK)",
#     "I": "ELEMENT + BLOCK",
#     "D": "DOOR",
#     "S": "STAIR",
#     "W": "WALL",
#     "-": "VOID"
# }
tileTypes = {
    "F": "FLOOR",
    "B": "BLOCK",
    "M": "MONSTER",
    "P": "ELEMENT (LAVA, WATER)",
    "D": "DOOR",
    "S": "STAIR",
    "W": "WALL",
    "-": "VOID",
    "C": "MOVABLE BLOCK",
    "A": "BREAKABLE WALL",
    "N": "TODO",
    "E": "TODO",
    "U": "TODO"
}

dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

# location for training data
TRAINING_DATA_DIR = dir_path + "/" + "map_data/map_reduced_OI"
# TRAINING_DATA_DIR = "./simple_maps"

N_CLUSTERS = 5
CLUSTER_MODEL_DIR = dir_path + "/" + "model/kmeans.pkl"