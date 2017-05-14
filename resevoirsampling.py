#!/bin/bash

import numpy as np
import random


def reservoir_sample(sample_list: list, k):
    result_list = sample_list[:k]
    for sample_index in range(k, len(sample_list)):
        result_index = random.randrange(sample_index)
        if result_index < k:
            result_list[result_index] = sample_list[sample_index]
    return result_list


# A-Chao
def weighted_reservoir_sample(sample_list: list, weight_list: list, k):
    assert len(sample_list) == len(weight_list), "lengths should be the same"
    # weighted_sum = np.sum(weight_list[:k])/k
    weighted_sum = sum(weight_list[:k]) / k
    result_list = sample_list[:k]
    for sample_index in range(k, len(sample_list)):
        weighted_sum += weight_list[sample_index] / k
        sample_p = weight_list[sample_index] / weighted_sum
        result_p = random.random()
        if result_p <= sample_p:
            result_list[random.randrange(k)] = sample_list[sample_index]
    return result_list


weighted_reservoir_sample([1, 2, 3], [.4, .4, .2], 1)
