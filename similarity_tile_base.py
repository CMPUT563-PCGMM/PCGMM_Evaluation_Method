import numpy as np

def tile_base_similarity_score(room1: np.ndarray, room2: np.ndarray) -> float:

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


# training dataset = 41.59914756780927
# Basic MC = 41.824561403508774
