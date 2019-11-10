import numpy as np

def histogram_base_similarity_score(room1: np.ndarray, room2: np.ndarray) -> float:

    def manhattan_distance(x,y):
        return sum(abs(a-b) for a,b in zip(x,y))
    
    def compute_room_histogram(room):
        hist = {
            "F": 0,
            "B": 0,
            "M": 0,
            "P": 0,
            "O": 0,
            "I": 0,
            "S": 0,
            "-": 0
        }
        unique_elements, counts_elements = np.unique(room, return_counts=True)
        for idx, c in enumerate(unique_elements):
            if c == "W" or c == "D":
                continue
            hist[c] = counts_elements[idx]
        return hist

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

