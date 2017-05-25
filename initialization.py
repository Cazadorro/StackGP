#!/bin/bash

from genetics import StackGenotype
from itertools import islice
import random
import copy


class Initializer:
    def _initialize(self, size, wrapper):
        raise NotImplementedError

    def __call__(self, size, genotype_wrapper, member_wrapper):
        def wrapper(gene): member_wrapper(genotype_wrapper(gene))

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
