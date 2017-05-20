#!/bin/bash

from genetics import StackGenotype
from itertools import islice
import random
import copy

DEFAULTSIZE = 10


def generator_initialization(gene_choice_generator,
                             max_genotype_size=DEFAULTSIZE):
    size = random.randint(1, max_genotype_size)
    return [gene for gene in islice(gene_choice_generator, size)]


def single_source_initialization(spawn_gene, max_genotype_size=DEFAULTSIZE):
    return [copy.deepcopy(spawn_gene) for _ in range(max_genotype_size)]


def seed_initialization(seed, gene_choice_generator,
                        max_genotype_size=DEFAULTSIZE):
    random.seed(seed)
    return generator_initialization(gene_choice_generator, max_genotype_size)


def population_initialization(init_population, max_genotype_size=DEFAULTSIZE):
    return copy.deepcopy(init_population[:max_genotype_size])
