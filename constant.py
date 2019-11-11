tileTypes = {
    "F": "FLOOR",
    "B": "BLOCK",
    "M": "MONSTER",
    "P": "ELEMENT (LAVA, WATER)",
    "O": "ELEMENT + FLOOR (LAVA/BLOCK, WATER/BLOCK)",
    "I": "ELEMENT + BLOCK",
    "D": "DOOR",
    "S": "STAIR",
    "W": "WALL",
    "-": "VOID"
}

# location for training data
TRAINING_DATA_DIR = "./maps"
# TRAINING_DATA_DIR = "./simple_maps"

N_CLUSTERS = 5
CLUSTER_MODEL_DIR = "model/kmeans.pkl"