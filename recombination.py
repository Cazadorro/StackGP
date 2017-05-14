#!/bin/bash
import random
from copy import deepcopy

def npoint_crossover(genotypes, n):
    genotype_length = len(genotypes[0])
    assert all(len(genotype) == genotype_length for genotype in
               genotypes), "Genotype parents are not all the same length"
    assert 0 <= n <= genotype_length, "n is too large for the length of " \
                                      "genotype or is negative"
    xover_points = sorted(random.sample(range(1, genotype_length + 1), n))
    parent_choice = 0
    number_of_parents = len(genotypes)
    # this shuffles with out changing genotypes
    genotypes = random.sample(deepcopy(genotypes), number_of_parents)
    xover_start = 0
    new_genes = []
    for xover_point in xover_points:
        xover_parent = genotypes[parent_choice]
        parent_choice = (parent_choice + 1) % number_of_parents
        new_genes.extend(xover_parent[xover_start:xover_point])
        xover_start = xover_point
    return new_genes


def uniform_crossover(genotypes):
    genotype_length = len(genotypes[0])
    assert all(len(genotype) == genotype_length for genotype in
               genotypes), "Genotype parents are not all the same length"
    new_genes = []
    for index in range(genotype_length):
        new_genes.append(random.choice(genotypes)[index])
    return new_genes
