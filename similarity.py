from itertools import combinations

from utils import readMaps
from similarity_tile_base import tile_base_similarity_score
from similarity_histogram_base import histogram_base_similarity_score

####### CONFIG ############
# location for room folder
ROOMS_DIR = "./maps"
# ROOMS_DIR = "./generate_map_BMC"
# ROOMS_DIR = "./simple_maps"

# function for compute similarity score
# similarity_score_fn = tile_base_similarity_score
similarity_score_fn = histogram_base_similarity_score
###########################


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


room_list = readMaps(tileTypes, ROOMS_DIR)
print("length of room list = ", len(room_list))
print(room_list[0].shape)

comb = list(combinations(room_list, 2))

total_score = 0
for room1, room2 in comb:
    score = similarity_score_fn(room1, room2)
    # break
    total_score = total_score + score

print("average simliarity score = ", total_score/len(comb))