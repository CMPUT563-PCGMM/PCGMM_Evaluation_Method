import numpy as np

from utils import compute_room_histogram, manhattan_distance

def histogram_base_similarity_score(room1: np.ndarray, room2: np.ndarray) -> float:

    score = 0
    # change room1, room2 to histogram
    his_room1 = compute_room_histogram(room1)
    his_room2 = compute_room_histogram(room2)

    score = manhattan_distance(his_room1.values(), his_room2.values())
    # print(his_room1)
    # print(his_room2)
    # print(his_room1.values())
    # print(his_room2.values())
    # print(score)
    
    return score


# training dataset = 65.92672508110473
# Basic MC = 65.11814536340852

