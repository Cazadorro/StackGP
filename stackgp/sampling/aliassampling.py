#!/bin/bash

import numpy as np
import random


def alias_table(probabilities: list):
    assert sum(probabilities) == 1.0, "error, sum of probabilities is not 1"
    n = len(probabilities)
    probability_array = np.array(probabilities) * n
    u_probability_array = np.empty(n, float)
    alias_index_list = np.empty(n, dtype=np.uint64)
    lt_one_list = []
    gte_one_list = []
    for index, probability in enumerate(probability_array):
        if probability < 1:
            lt_one_list.append(index)
        else:
            gte_one_list.append(index)

    while lt_one_list and gte_one_list:
        lt_index = lt_one_list.pop()
        gte_index = gte_one_list.pop()
        prob_lt = probability_array[lt_index]
        u_probability_array[lt_index] = prob_lt
        alias_index_list[lt_index] = gte_index
        probability_array[gte_index] = probability_array[
                                           gte_index] + prob_lt - 1
        if probability_array[gte_index] < 1:
            lt_one_list.append(gte_index)
        else:
            gte_one_list.append(gte_index)

    while gte_one_list:
        gte_index = gte_one_list.pop()
        u_probability_array[gte_index] = 1

    while lt_one_list:
        lt_index = lt_one_list.pop()
        u_probability_array[lt_index] = 1

    return u_probability_array, alias_index_list


def alias_index_selection(probability_array: np.array,
                          alias_index_list: np.array):
    n = len(probability_array)
    i = random.randrange(n)
    r = random.random()
    if r < probability_array[i]:
        return i
    else:
        return alias_index_list[i]


def alias_selection(elements: list, probability_array: np.array,
                    alias_index_list: np.array):
    index = alias_index_selection(probability_array, alias_index_list)
    return elements[index]


def weighted_choice_generator(elements: list, probabilities: list):
    assert len(elements) == len(
        probabilities), "error not all elements have matching probabilities"
    u_prob_array, alias_index = alias_table(probabilities)
    print("probarray ", u_prob_array)
    print("aliasindex ", alias_index)
    while True:
        yield alias_selection(elements, u_prob_array, alias_index)


class AliasSampler:
    def __init__(self, elements: list, probabilities: list):
        self._generator = weighted_choice_generator(elements, probabilities)

    def choice(self):
        return next(self._generator)

    def choices(self, n):
        return [self.choice() for _ in range(n)]
