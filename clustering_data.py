import copy
from typing import List
import pickle

import numpy as np
from sklearn.cluster import KMeans

from utils import readMaps, compute_room_histogram, compute_room_list_histogram
from constant import tileTypes, N_CLUSTERS

def train_store_model(training_data_dir: str, store_file: str):
    training_room_list = np.asarray(readMaps(tileTypes, training_data_dir))
    
    # using training data train clustering model
    cluster_model = cluster_data(training_room_list)
    # print(cluster_model.labels_)
    
    with open(store_file, 'wb') as fid:
        pickle.dump(cluster_model, fid)

def cluster_data(room_list: np.ndarray) -> KMeans:

    hist_list = compute_room_list_histogram(room_list)

    kmeans = KMeans(n_clusters=N_CLUSTERS).fit(hist_list)
    # print(kmeans.labels_)
    return kmeans




