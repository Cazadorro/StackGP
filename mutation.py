#!/bin/bash

from genetics import StackGenotype
import random
from copy import deepcopy
from individual import Individual


class MutationParameters:
    def __init__(self, gene_choice_generator=None, genes=None, gene=None,
                 prev_gene=None):
        self.gene_choice_generator = gene_choice_generator
        self.genes = genes
        self.gene = gene
        self.prev_gene = prev_gene

    @property
    def new_gene(self):
        return next(self.gene_choice_generator)

    def set_genes(self, gene=None, prev_gene=None):
        self.gene = gene
        self.prev_gene = prev_gene


def duplicate(mutation_param: MutationParameters):
    return [mutation_param.gene, deepcopy(mutation_param.gene)]


def replace(mutation_param: MutationParameters):
    return [mutation_param.new_gene]


def insert(mutation_param: MutationParameters):
    return [mutation_param.gene, mutation_param.new_gene]


def delete(muation_param: MutationParameters):
    return []


def reorder(mutation_param: MutationParameters):
    genes = mutation_param.genes
    gene = mutation_param.gene
    x = random.randint(len(genes))
    gene, genes[x] = genes[x], gene
    return [gene]


def merge(mutation_param: MutationParameters):
    if mutation_param.prev_gene is not None:
        # TODO make sure this is not an issue, will it actually merge?
        mutation_param.prev_gene.get_merge(mutation_param.gene)
    return []


# TODO inplace mutation? to mutate ERK.


class Mutator:
    def __init__(self, mutation_generator, genechoice_generator, mutation_chance):
        self._mutgenerator = mutation_generator
        self._genegenerator = genechoice_generator
        self._chance = mutation_chance

    def _mutate(self, individual: Individual):
        prev_gene = None
        new_genotype = []
        genes = individual.genotype.genes
        mutation_params = MutationParameters(self._genegenerator, genes)
        for gene in genes:
            mutation_params.set_genes(gene, prev_gene)
            if random.random() < self._chance:
                new_genes = next(self._mutgenerator)(mutation_params)
            else:
                new_genes = gene
            prev_gene = new_genes[-1]
            new_genotype.extend(new_genes)
        return StackGenotype(new_genotype)

    def __call__(self, individual: Individual, wrapper):
        return wrapper(self._mutate(individual))
