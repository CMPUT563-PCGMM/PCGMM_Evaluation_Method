from typing import Dict
# import collections

import numpy as np
    
def markov_base_similarity_score(room1: np.ndarray, room2: np.ndarray) -> float:
    
    # train simple MC model
    def simple_markov_chain_model(room: np.ndarray) -> Dict[str, int]:
        p_dict = {}

        room = room[2:-2, 2:-2]
        # room = room[1:-1, 1:-1]
        
        # reverse the even row
        # https://stackoverflow.com/questions/37280681/reverse-even-rows-in-a-numpy-array-or-pandas-dataframe
        room[1::2, :] = room[1::2, ::-1]
        
        # flatten rooms
        room = room.flatten()

        # print(room)

        for i in range(room.shape[0]-1):
            key = room[i+1] + room[i]

            if key in p_dict:
                p_dict[key] = p_dict[key] + 1
            else:
                p_dict[key] = 1

        return p_dict

    def manhattan_distance(dict_1, dict_2):
        ############ METHOD 1 ####
        union_list = list(set().union(dict_1.keys(), dict_2.keys()))
        # # print(union_list) 

        for k in union_list:
            if k not in dict_1:
                dict_1[k] = 0
            elif k not in dict_2:
                dict_2[k] = 0

        score = 0
        for k in dict_1.keys():
            score = score + abs(dict_1[k] - dict_2[k])

        # print(dict_1)
        # print(dict_2)
        ###########################
        
        ############ METHOD 2 ####
        # od1 = collections.OrderedDict(sorted(dict_1.items()))
        # od2 = collections.OrderedDict(sorted(dict_2.items()))

        # score = np.sum(np.abs(np.subtract(np.asarray(list(od2.values())), np.asarray(list(od1.values())))))
        ###########################
        
        return score
        
        # print(p_dict)
    p_dict_1 = simple_markov_chain_model(room1)
    p_dict_2 = simple_markov_chain_model(room2)

    score = manhattan_distance(p_dict_1, p_dict_2)
    
    return score

# training dataset = 82.52015488388466
# Basic MC = 74.5607268170426
