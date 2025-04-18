# utils.py
import numpy as np


def create_collapsible_json(data):
    if isinstance(data, np.ndarray):
        data = data.tolist()
    return str(data)
