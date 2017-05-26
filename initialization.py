#!/bin/bash

from genetics import StackGenotype
from itertools import islice
import random
import copy


class Initializer:
    def _initialize(self, size):
        raise NotImplementedError

    def __call__(self, size, wrapper):
        x = self._initialize(size)
        return wrapper(x)


class GeneratorInitializer(Initializer):
    def __init__(self, generator):
        self._generator = generator

    def _initialize(self, size):
        size = random.randint(1, size)
        return list(islice(self._generator, size))


class SingleSourceInitializer(Initializer):
    def __init__(self, source_gene):
        self._source = source_gene

    def _initialize(self, size):
        size = random.randint(1, size)
        return list([copy.deepcopy(self._source) for _ in range(size)])


class SeedInitializer(GeneratorInitializer):
    def __init__(self, generator, seed):
        super().__init__(generator)
        self._seed = seed

    def _initialize(self, size):
        random.seed(self._seed)
        return super()._initialize(size)


class PopulationInitializer(Initializer):
    def __init__(self, init_population):
        self._population = init_population

    def _initialize(self, size):
        return list(copy.deepcopy(self._population[:size]))
