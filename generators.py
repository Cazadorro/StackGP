#!/bin/bash

import random
import math
import numpy as np


def binary_search(search_list, value, min_index=0, max_index=None):
    _max_index = len(search_list) if max_index is None else max_index
    return _binary_search(search_list, value, min_index, _max_index)


def _binary_search(search_list, value, min_index, max_index):
    assert max_index >= min_index, "error, max should not be greater than min"
    mid_point = min_index + int(math.floor((max_index - min_index) / 2))
    if min_index == max_index:
        return mid_point
    elif value > search_list[mid_point]:
        return _binary_search(search_list, value, mid_point + 1, max_index)
    elif value < search_list[mid_point]:
        return _binary_search(search_list, value, min_index, mid_point)
    else:
        return mid_point


def normalize_probabilities(probabilities):
    total_sum = sum(probabilities)
    return [probability/total_sum for probability in probabilities]

class CumulativeProbabilities:
    def __init__(self, probability_list):
        self.cumulative_distribution = np.cumsum(probability_list)
        self.cumulative_distribution /= self.cumulative_distribution[-1]

    def __getitem__(self, probability):
        return binary_search(self.cumulative_distribution, probability)

    def __len__(self):
        return len(self.cumulative_distribution)


def weighted_gene_choice(genes: list, probabilities: list):
    cumulative_prob = CumulativeProbabilities(probabilities)
    while True:
        r = random.random()
        yield genes[cumulative_prob[r]]


def uniform_gene_choice(genes: list):
    while True:
        yield random.choice(genes)


def weighted_mutator_choice(mutators: list, probabilities: list):
    cumulative_prob = CumulativeProbabilities(probabilities)
    while True:
        r = random.random()
        yield mutators[cumulative_prob[r]]
