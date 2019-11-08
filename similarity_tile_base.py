from itertools import combinations

import numpy as np

from utils import readMaps

def compute_similarity_score(room1: np.ndarray, room2: np.ndarray) -> int:

	##########################################
	def internal_sim_score(room1, rotate_room2):
		score = 0
		h, w = room1.shape
		board_length = 2*h + 2*(w-2)
		second_board_length = 2*(h-2) + 2*(w-4)

		for i in range(h):
			for j in range(w):
				if room1[i, j] == room2[i, j]:
					score = score + 1

		score = score - board_length - second_board_length

		return score
	##########################################

	# print(np.flipud(np.fliplr(room2)))
	score = internal_sim_score(room1, room2)
	score = max(score, internal_sim_score(room1, np.fliplr(room2)))
	score = max(score, internal_sim_score(room1, np.flipud(room2)))
	score = max(score, internal_sim_score(room1, np.flipud(np.fliplr(room2))))
	
	return score


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

# read the room
# room_list = readMaps(tileTypes, "./maps")
room_list = readMaps(tileTypes, "./generate_map_BMC")
print("lenght of room list = ", len(room_list))
print(room_list[0].shape)

comb = list(combinations(room_list, 2))

total_score = 0
for room1, room2 in comb:
	# print(room1)
	# print(room2)
	score = compute_similarity_score(room1, room2)
	# print("score = ", score)
	total_score  = total_score + score

# training dataset = 41.59914756780927
# Basic MC = 41.824561403508774
print("average simliarity score = ", total_score/len(comb))
