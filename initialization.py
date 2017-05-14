#!/bin/bash

from genetics import StackGenotype
from itertools import islice
import random

DEFAULTSIZE = 10


def generator_initialization(gene_choice_generator,
                             max_genotype_size=DEFAULTSIZE):
    size = random.randint(1, max_genotype_size)
    return [gene for gene in islice(gene_choice_generator, size)]
