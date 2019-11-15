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
    "A": "BREAKABLE WALL",
    "C": "MOVABLE BLOCK",
    "N": "TODO",
    "E": "TODO",
    "U": "TODO"
}

# location for training data
TRAINING_DATA_DIR = "./maps"
# TRAINING_DATA_DIR = "./simple_maps"

N_CLUSTERS = 5
CLUSTER_MODEL_DIR = "model/kmeans.pkl"