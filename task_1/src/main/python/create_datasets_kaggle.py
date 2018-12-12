#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 15:24:59 2018

@author: aparravi
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np


#%%
if __name__ == "__main__":
    
    #%% Create Pubmed;
    
    # Read the graph to obtain the vertex features and classes;
    folder = "../../../data/pgx-graphs/pubmed"
    vertices_path = os.path.join(folder, "pubmed_v.csv")
    
    vertices_df = pd.read_csv(vertices_path, sep=",", index_col="id")
    
    seed = 777
    vertices_train, vertices_val = train_test_split(vertices_df, test_size=500, random_state=seed)
    vertices_train, vertices_test = train_test_split(vertices_train, test_size=1000, random_state=seed)
    
    # Remove features from the validation set;
    vertices_val_nf = vertices_val[["label"]]
    vertices_test_nf = vertices_test[["label"]]
    
    vertices_test_nf["Usage"] = "public"
    vertices_val_nf["Usage"] = "private"
    
    vertices_test_val = pd.concat([vertices_test_nf, vertices_val_nf])
    
    # Save results;
    vertices_test_val.to_csv(os.path.join(folder, "pubmed_test_val.csv"))
    vertices_val_nf.to_csv(os.path.join(folder, "pubmed_val.csv"))
    vertices_test.to_csv(os.path.join(folder, "pubmed_test.csv"))
    vertices_train.to_csv(os.path.join(folder, "pubmed_train.csv"))
    
    # Sample submission;
    sample_sub = pd.DataFrame(np.random.randint(1, 4, len(vertices_test_val)), index=vertices_test_val.index, columns=["label"])
    sample_sub.to_csv(os.path.join(folder, "sample_solution.csv"))
    
    
    #%% Create PPI;
    
    def bool_to_int(labels: list, use_int: bool=True) -> list:
        return [i if use_int else str(i) for i, x in enumerate(labels) if (x == 1 if use_int else x == "1")]
    
    def str_labels_to_ids(labels_str: str) -> str:
        return " ".join(bool_to_int(labels_str.split(";"), use_int=False))
        
    
    # Read the graph to obtain the vertex features and classes;
    folder = "../../../data/pgx-graphs/ppi"
    vertices_path = os.path.join(folder, "ppi_v.csv")
    
    vertices_df = pd.read_csv(vertices_path, sep=",", index_col="id")
    
    # Store the vertex set without labels;
    vertices_df.drop(columns=["labels"]).replace({"dataset": {"val": "test"}}).to_csv(os.path.join(folder, "ppi_vertices.csv"))
        
    v_train = vertices_df[vertices_df["dataset"] == "train"]
    v_test = vertices_df[vertices_df["dataset"] == "test"]
    v_val = vertices_df[vertices_df["dataset"] == "val"]
    
    v_train = v_train.drop(columns=["dataset"])
    v_test = v_test.drop(columns=["dataset"])
    v_val = v_val.drop(columns=["dataset"])
    
    v_test["Usage"] = "public"
    v_val["Usage"] = "private"
    v_test_val = pd.concat([v_test, v_val])
    # Remove the labels and usage, this is given to the students;
    v_test_val_2 = v_test_val.drop(columns=["labels", "Usage"])
    # This is used as "real solution" on kaggle;
    v_test_val_3 = v_test_val.drop(columns=["features"])
    
    v_test_val_2.to_csv(os.path.join(folder, "ppi_test.csv"))
    
    v_train.to_csv(os.path.join(folder, "ppi_train.csv"))
    
    # Fix the labels format of the solution file, to be compliant with Kaggle's format;
    v_test_val_3["labels"] = v_test_val_3["labels"].apply(lambda x: str_labels_to_ids(x))
    v_test_val_3.to_csv(os.path.join(folder, "ppi_kaggle_solution.csv"))
    
    # Sample submission;
    sample_sub = pd.DataFrame([str_labels_to_ids(";".join([str(x) for x in np.random.randint(0,2,122)])) for i in range(len(v_test_val))],
                               index=v_test_val.index, columns=["labels"])
    sample_sub.to_csv(os.path.join(folder, "sample_solution.csv"))
    
    # Perfect submission;
    v_test_val_3[["labels"]].to_csv(os.path.join(folder, "perfect.csv"))