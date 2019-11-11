from constant import CLUSTER_MODEL_DIR, TRAINING_DATA_DIR
from clustering_data import train_store_model

###### store the model #####
train_store_model(TRAINING_DATA_DIR, CLUSTER_MODEL_DIR)