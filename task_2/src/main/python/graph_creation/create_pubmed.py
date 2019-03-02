#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 15:04:49 2018

@author: aparravi
"""

import pandas as pd
import json


if __name__ == "__main__":
    
    vertices_path = "../../../../data/Pubmed-Diabetes/data/Pubmed-Diabetes.NODE.paper.tab"
    
    vertices = []
    
    for i, line in enumerate(open(vertices_path, "r")):
        
        if i == 0:
            # Skip first line;
            continue
        elif i == 1:
            # The header contains the property names and default values;
            values = line.split("\t")
            labels = set(int(x) for x in values[0][len("cat="):-len(":label")].split(","))
            words = sorted(set(x[len("numeric:w-"):-len(":0.0")] for x in values[1:-1]))
        else:
            # Process each vertex;
            values = line.split("\t")
            vertex_id = int(values[0])
            label = int(values[1][len("label="):])
            # Create a vector of values;
            vertex_words = {w: 0.0 for w in words}
            for w in values[2:-1]:
                name, val = w.split("=")
                name = name[len("w-"):]
                val = float(val)
                vertex_words[name] = val
            summary = ",".join(sorted([w[len("w-"):].strip() for w in values[-1][len("summary="):].split(",")]))
            new_vertex = {
                    "id": vertex_id,
                    "label": label,
                    "tf-idf": ";".join(str(x) for x in vertex_words.values()),
                    "summary": summary
                    }
            for w, val in vertex_words.items():
                new_vertex[w] = val
            vertices += [new_vertex]
            
            
    #%% Create a configuration file;
            
    config = {
            "header": True,
            "vertex_id_column": "id",
            "edge_source_column": "source",
            "edge_destination_column": "dest",
            "format": "csv",
            "separator": ",",
            "vertex_id_type": "long",
            "edge_uris": ["pubmed_e.csv"],
            "vertex_uris": ["pubmed_v.csv"],
            "vertex_props": [
                    {"name": "label", "type": "int"},
                    {"name": "summary", "type": "string"},
                    {"name": "tf-idf", "type": "float", "dimension": 500}
                    ]
            }     
    
    for w in words:
        config["vertex_props"] += [{"name": w, "type": "float"}]
    
    # Save to file;
    with open("../../../../data/pgx-graphs/pubmed/pubmed.json", "w") as f:
        json.dump(config, f, indent=4)
       
        
    #%% Create the vertices file;
    
    vertices_pd = pd.DataFrame(vertices)
    cols = list(vertices_pd)
    cols.insert(0, cols.pop(cols.index('id')))
    cols.insert(1, cols.pop(cols.index('label')))
    cols.insert(2, cols.pop(cols.index('tf-idf')))
    cols.insert(3, cols.pop(cols.index('summary')))
    vertices_pd = vertices_pd.loc[:, cols]
    
    vertices_pd = vertices_pd.set_index("id")
    
    vertices_pd.to_csv("../../../../data/pgx-graphs/pubmed/pubmed_v.csv", header=True, index=True)
    
    #%% Create the edges file;
    
    edges_path = "../../../../data/Pubmed-Diabetes/data/Pubmed-Diabetes.DIRECTED.cites.tab"
    
    edges = []
    
    for i, line in enumerate(open(edges_path, "r")):
        
        # Skip first two lines;
        if i > 1:
            values = line.split("\t")
            edge_id = int(values[0])
            start = int(values[1][len("paper:"):])
            end = int(values[-1][len("paper:"):])
            
            if start not in vertices_pd.index:
                print(f"{start} is missing!")
            if end not in vertices_pd.index:
                print(f"{end} is missing!") 
            
            edges += [{"source": start, "dest": end}]
     
    edges_df = pd.DataFrame(edges)[["source", "dest"]]
    edges_df.to_csv("../../../../data/pgx-graphs/pubmed/pubmed_e.csv", header=True, index=False)
