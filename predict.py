import logging

import azure.functions as func
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import scipy.sparse as sparse
import scipy

import os
import tempfile
import json
import pickle

class CFR():
    def __init__(self,
                 user_vecs,
                 item_vecs,
                 clicks_sparse,
                 users_arr,
                 items_arr,
                 user_to_sparse_user,
                 sparse_item_to_item):
        
        self.user_vecs = user_vecs
        self.item_vecs = item_vecs
        self.clicks_sparse = clicks_sparse
        self.users_arr = users_arr
        self.items_arr = items_arr
        self.user_to_sparse_user = user_to_sparse_user
        self.sparse_item_to_item = sparse_item_to_item
        
    
    def rec_items(self, user_id, num_items = 5):
        """
        Calculate and return the recommnded items
        Input :
            - user_id (int) : user for whom recmmendations are calculated
            - num_items (int) : number of recommnded items
        Output :
            - codes (list of int) : recommended items
            - (pd.DataFrame) : recommended items and their attached category (for easier analysis)
        """
        
        user_id = self.user_to_sparse_user[user_id]
        user_ind = np.where(self.users_arr == user_id)[0][0] 
        pref_vec = self.clicks_sparse[user_ind,:].toarray() 
        pref_vec = pref_vec.reshape(-1) + 1 
        pref_vec[pref_vec > 1] = 0 
        rec_vector = self.user_vecs[user_ind,:].dot(self.item_vecs.T) 
       
        min_max = MinMaxScaler()
        rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1,1))[:,0] 
        recommend_vector = pref_vec*rec_vector_scaled 
        
        product_idx = np.argsort(recommend_vector)[::-1][:num_items] 
       
        rec_list = [] 
        for index in product_idx:
            code = self.items_arr[index]
            code = self.sparse_item_to_item[code] 
            rec_list.append(code)
                             
        return rec_list


def init_model():  
    user_vecs = np.load("user_vecs.npy")
    #print("Avec fonction load_matrix : user_vecs.shape =", user_vecs.shape)

    item_vecs = np.load("item_vecs.npy")
    #print("Avec fonction load_matrix : item_vecs.shape =", item_vecs.shape)

    users_arr = np.load("users_arr.npy")
    #print("Avec fonction load_matrix : users_arr.shape =", users_arr.shape)

    items_arr = np.load("items_arr.npy")
    #print("Avec fonction load_matrix : items_arr.shape =", items_arr.shape)

    clicks = scipy.sparse.load_npz("clicks.npz")
    #print("Avec fonction load_matrix : clicks =\n")
    #print(clicks)

    with open("user_to_sparse_user.pkl", "rb") as f:
            user_to_sparse_user = pickle.load(f)

    with open("sparse_item_to_item.pkl", "rb") as f:
            sparse_item_to_item = pickle.load(f)

    cf_object = CFR(user_vecs,
                    item_vecs,
                    clicks,
                    users_arr,
                    items_arr,
                    user_to_sparse_user,
                    sparse_item_to_item)
    
    return cf_object
    
#
##########################################################################################################################################################################

def retourner_reco(user_):
    np_array = np.array([1, 2, 3])
    model = init_model()
    recommendations = model.rec_items(user_)[:]
    #recommendations = np_array[0]
    return recommendations

##########################################################################################################################################################################