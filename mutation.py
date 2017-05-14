#!/bin/bash

from genetics import StackGenotype
import random
from copy import deepcopy

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

#TODO inplace mutation? to mutate ERK.


def mutate(genotype, mutator_generator, gene_choice_generator):
    prev_gene = None
    new_genotype = []
    genes = genotype.genes
    mutation_params = MutationParameters(gene_choice_generator, genes)
    for gene in genes:
        mutation_params.set_genes(gene, prev_gene)
        new_genes = next(mutator_generator)(mutation_params)
        prev_gene = new_genes[-1]
        new_genotype.extend(new_genes)
    return StackGenotype(new_genotype)
