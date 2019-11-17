from itertools import combinations
import pickle

import numpy as np
import os

from PCGMM_Evaluation_Method.constant import tileTypes, TRAINING_DATA_DIR, CLUSTER_MODEL_DIR
from PCGMM_Evaluation_Method.utils import readMaps, compute_room_list_histogram
from PCGMM_Evaluation_Method.clustering_data import cluster_data
from PCGMM_Evaluation_Method.similarity_tile_base import tile_base_similarity_score
from PCGMM_Evaluation_Method.similarity_histogram_base import histogram_base_similarity_score
from PCGMM_Evaluation_Method.similarity_markov_base import markov_base_similarity_score

####### CONFIG ############
# location for room folder
# ROOMS_DIR = "map_data/map_reduced_OI" # T: 28.57, F: 76.17
# ROOMS_DIR = "generate_map/generate_map_RM_2" # 67.82 68.25
# ROOMS_DIR = "generate_map/generate_map_BMC_2" # 27.48 57.12
# ROOMS_DIR = "./simple_maps"

# function for compute similarity score
# similarity_score_fn = tile_base_similarity_score
# similarity_score_fn = histogram_base_similarity_score
# similarity_score_fn = markov_base_similarity_score

# flag if use cluster
# ENABLE_CLUSTER = False
###########################

# def total_avg_score(room_list):
#     comb = list(combinations(room_list, 2))

#     total_score = 0
#     for room1, room2 in comb:
#         score = similarity_score_fn(room1, room2)
#         total_score = total_score + score

#     return total_score / len(comb)

def evaluate_similarity(evaluate_data, similarity_function, enable_cluster):

    def total_avg_score(rooms):
        comb = list(combinations(rooms, 2))

        total_score = 0
        for room1, room2 in comb:
            score = similarity_score_fn(room1, room2)
            total_score = total_score + score

        return total_score / len(comb)
    

    sim_fn_dict = {
        "tile_base": tile_base_similarity_score,
        "histogram_base": histogram_base_similarity_score,
        "markov_base": markov_base_similarity_score
    }
    similarity_score_fn = sim_fn_dict[similarity_function]
    room_list = evaluate_data
    
    if enable_cluster:
        # restore the model
        with open(CLUSTER_MODEL_DIR, 'rb') as fid:
            cluster_model = pickle.load(fid)

        # predict label for room list
        pred_labels_ = cluster_model.predict(compute_room_list_histogram(room_list))
        
        # find index list for each unique value
        cluster_dict = {i: (pred_labels_ == i).nonzero()[0] for i in np.unique(pred_labels_)}
        # print(cluster_dict)

        total_avg = 0.0
        for v, idx in cluster_dict.items():
            # print(idx)
            cluster_room = room_list[idx]
            if cluster_room.shape[0] < 2:
                continue
            
            same_type_rooms = [cluster_room[i, :, :] for i in range(cluster_room.shape[0])]
            # print(cluster_room.shape)
            avg = total_avg_score(same_type_rooms)
            # print(avg)
            
            total_avg = total_avg + (cluster_room.shape[0] / room_list.shape[0]) * avg
        
        # print("average simliarity score = ", total_avg)

            
    else:
        total_avg = total_avg_score(room_list)
        # print("average simliarity score = ", total_avg)

    return total_avg


# if __name__ == "__main__":
#     room_list = readMaps(tileTypes, ROOMS_DIR)
#     print("length of room list = ", len(room_list))
#     print(room_list[0].shape)

#     if ENABLE_CLUSTER:
        
#         # restore the model
#         with open(CLUSTER_MODEL_DIR, 'rb') as fid:
#             cluster_model = pickle.load(fid)

#         room_list = np.asarray(room_list)

#         # predict label for room list
#         pred_labels_ = cluster_model.predict(compute_room_list_histogram(room_list))
        
#         # find index list for each unique value
#         cluster_dict = {i: (pred_labels_ == i).nonzero()[0] for i in np.unique(pred_labels_)}
#         # print(cluster_dict)

#         total_avg = 0.0
#         for v, idx in cluster_dict.items():
#             # print(idx)
#             cluster_room = room_list[idx]
#             if cluster_room.shape[0] < 2:
#                 continue
            
#             same_type_rooms = [cluster_room[i, :, :] for i in range(cluster_room.shape[0])]
#             # print(cluster_room.shape)
#             avg = total_avg_score(same_type_rooms)
#             # print(avg)
            
#             total_avg = total_avg + (cluster_room.shape[0] / room_list.shape[0]) * avg
        
#         print("average simliarity score = ", total_avg)

            
#     else:
#         total_avg = total_avg_score(room_list)
#         print("average simliarity score = ", total_avg)

