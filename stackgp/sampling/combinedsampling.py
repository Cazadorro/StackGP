#!/bin/bash

from .aliassampling import weighted_choice_generator
from .resevoirsampling import weighted_reservoir_sample


def n_choice_sampler(sample_list: list, weight_list: list, n: int, *,
                     replacement: bool):
    if replacement:
        alias_generator = weighted_choice_generator(sample_list, weight_list)
        return [next(alias_generator) for _ in range(n)]
    else:
        return weighted_reservoir_sample(sample_list, weight_list, n)


def replacement_sampler(sample_list: list, weight_list: list, n: int):
    alias_generator = weighted_choice_generator(sample_list, weight_list)
    return [next(alias_generator) for _ in range(n)]


def no_replacement_sampler(sample_list: list, weight_list: list, n: int):
    return weighted_reservoir_sample(sample_list, weight_list, n)
