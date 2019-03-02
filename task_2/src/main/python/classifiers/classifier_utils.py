# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:53:42 2019

@author: albyr
"""

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def hamming_accuracy(prediction, true_values):
    """
    Metric used in multioutput-label classification,
    for each example measures the % of correctly predicted labels.
    
    Equivalent to traditional accuracy in a single-output scenario;
    """
    return np.mean(np.sum(np.equal(prediction, true_values)) / float(true_values.size))


def get_score(prediction, true_values):    
    print("\tHamming accuracy: {:.3f}".format(hamming_accuracy(prediction, true_values)))
    print("\tAccuracy, exact matches: {:.3f}".format(accuracy_score(prediction, true_values)))
    print("\tMacro F1 Score: {:.3f}".format(f1_score(y_true=true_values, y_pred=prediction, average="macro")))
    print("\tMicro F1 Score: {:.3f}".format(f1_score(y_true=true_values, y_pred=prediction, average="micro")))
    

def build_dataframe(input_data: pd.DataFrame, col_name: str, preserve_int_col_name=False) -> pd.DataFrame:
    """
    Given an input DataFrame and a column name, return a new DataFrame in which the column has been cleaned.
    Used to transform features and labels columns from "0;1;1;0" to [0, 1, 1, 0]
    """
    vertices_dict = []
    for i, row_i in input_data.iterrows():
        features = [int(float(x)) for x in row_i[f"{col_name}s"].split(";")]
        
        new_v = {"id": i}
        for j, f in enumerate(features):
            new_v[j if preserve_int_col_name else f"{col_name}_{j}"] = f
        vertices_dict += [new_v]
    res_df = pd.DataFrame(vertices_dict)
    return res_df.set_index("id")


def bool_to_int(labels: list) -> list:
    """
    Turn a list of 0s and 1s into a list whose values are the indices of 1s.
    Used to create a valid Kaggle submission.
    E.g. [1, 0, 0, 1, 1] -> [0, 3, 4]
    """
    return [i for i, x in enumerate(labels) if x == 1]