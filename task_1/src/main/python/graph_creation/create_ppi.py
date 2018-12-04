#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:10:56 2018

@author: aparravi
"""

import pandas as pd
import json
import numpy as np


if __name__ == "__main__":
    
    graph_path = "../../../../data/ppi/ppi-G.json"
    class_path = "../../../../data/ppi/ppi-class_map.json"
    feat_path = "../../../../data/ppi/ppi-feats.npy"
    id_path = "../../../../data/ppi/ppi-id_map.json"
        
    with open(graph_path, "r") as f:
        graph_dict = json.load(f)
    
    with open(class_path, "r") as f:
        class_dict = json.load(f)
        
    with open(id_path, "r") as f:
        id_dict = json.load(f)
        
    with open(feat_path, "r") as f:
        features = np.load(feat_path)
        
        
    #%% Create the vertex set;
    
    vertices = []
    
    for v in graph_dict["nodes"]:
        vertex_id = int(v["id"])
        
        # Vertex type;
        if v["test"]:
            v_type = "test"
        elif v["val"]:
            v_type = "val"
        else:
            v_type = "train"
        
        # Vertex class;
        classes = class_dict[str(v["id"])]
        class_vector = ";".join(str(x) for x in classes)
        
        # Features;
        features_v = features[id_dict[str(v["id"])], :]
        features_vector = ";".join(str(x) for x in features_v)
        
        vertices += [{
                "id": vertex_id,
                "dataset": v_type,
                "labels": class_vector,
                "features": features_vector
                }]

    
    #%% Create the edge set;
    
    edges = [{"source": e["source"], "dest": e["target"]} for e in graph_dict["links"]]
    
    
    #%% Turn everything into dataframes;
    
    vertices_pd = pd.DataFrame(vertices)
    cols = list(vertices_pd)
    cols.insert(0, cols.pop(cols.index('id')))
    cols.insert(1, cols.pop(cols.index('dataset')))
    cols.insert(2, cols.pop(cols.index('labels')))
    cols.insert(3, cols.pop(cols.index('features')))
    vertices_pd = vertices_pd.loc[:, cols]
    
    vertices_pd = vertices_pd.set_index("id")
    
    vertices_pd.to_csv("../../../../data/pgx-graphs/ppi/ppi_v.csv", header=True, index=True)
    
    edges_df = pd.DataFrame(edges)[["source", "dest"]]
    edges_df.to_csv("../../../../data/pgx-graphs/ppi/ppi_e.csv", header=True, index=False)
    
    
    #%% Create a configuration file;
            
    config = {
            "header": True,
            "vertex_id_column": "id",
            "edge_source_column": "source",
            "edge_destination_column": "dest",
            "format": "csv",
            "separator": ",",
            "vertex_id_type": "long",
            "edge_uris": ["ppi_e.csv"],
            "vertex_uris": ["ppi_v.csv"],
            "vertex_props": [
                    {"name": "dataset", "type": "string"},
                    {"name": "labels", "type": "int", "dimension": 121},
                    {"name": "features", "type": "float", "dimension": 50}
                    ]
            }     
    
    # Save to file;
    with open("../../../../data/pgx-graphs/ppi/ppi.json", "w") as f:
        json.dump(config, f, indent=4)
       
    
    
