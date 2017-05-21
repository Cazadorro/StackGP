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


class Initializer:
    def _initialize(self, size, wrapper):
        raise NotImplementedError

    def __call__(self, size, wrapper):
        return self._initialize(size, wrapper)


class GeneratorInitializer(Initializer):
    def __init__(self, generator):
        self._generator = generator

    def _initialize(self, size, wrapper):
        size = random.randint(1, size)
        return [wrapper(gene) for gene in islice(self._generator, size)]


class SingleSourceInitializer(Initializer):
    def __init__(self, source_gene):
        self._source = source_gene

    def _initialize(self, size, wrapper):
        [wrapper(copy.deepcopy(self._source)) for _ in range(size)]


class SeedInitializer(GeneratorInitializer):
    def __init__(self, generator, seed):
        super().__init__(generator)
        self._seed = seed

    def _initialize(self, size, wrapper):
        random.seed(self._seed)
        return super()._initialize(size, wrapper)


class PopulationInitializer(Initializer):
    def __init__(self, init_population):
        self._population = init_population

    def _initialize(self, size, wrapper):
        return list(map(wrapper, copy.deepcopy(self._population[:size])))
