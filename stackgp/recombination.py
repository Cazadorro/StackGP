#!/bin/bash
import random
from copy import deepcopy
from typing import Tuple

from .individual import Individual


class Crossover:
    def _recombine(self, individuals: Tuple[Individual]):
        raise NotImplementedError

    def __call__(self, individuals: Tuple[Individual], wrapper) -> Individual:
        return wrapper(self._recombine(individuals))


class NPointCrossover(Crossover):
    def __init__(self, n):
        self._n = n

    def _recombine(self, parents: Tuple[Individual]):
        min_len = len(min(parents, key=lambda x: x.genotype))
        max_index = min_len - 1
        n = self._n if self._n <= max_index else max_index
        xover_points = sorted(random.sample(range(1, max_index), n))
        parent_choice = 0
        number_of_parents = len(parents)
        # this shuffles with out changing genotypes
        genotypes = random.sample(deepcopy(parents), number_of_parents)
        xover_start = 0
        new_genes = []
        for xover_point in xover_points:
            xover_parent = genotypes[parent_choice]
            parent_choice = (parent_choice + 1) % number_of_parents
            new_genes.extend(xover_parent.genotype[xover_start:xover_point])
            xover_start = xover_point
        xover_parent = genotypes[parent_choice]
        new_genes.extend(xover_parent.genotype[xover_start:len(xover_parent)])
        return new_genes


class UniformCrossover(Crossover):
    def _recombine(self, parents: Tuple[Individual]):
        copied_parents = deepcopy(list(parents))
        copied_parents.sort(key=lambda x: len(x.genotype), reverse=True)
        new_genes = []
        index = 0
        while len(copied_parents) > 1:
            min_parent_len = len(copied_parents[-1].genotype)
            for i in range(index, min_parent_len):
                new_genes.append(random.choice(copied_parents).genotype[index])
            index = min_parent_len
            copied_parents.pop()
        return new_genes
