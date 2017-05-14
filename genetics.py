#!/bin/bash

from structures import Stack


class StackGeneGroup:
    def __init__(self, *gene_keys):
        self._gene_keys = gene_keys

    @property
    def keys(self):
        return self._gene_keys

    def get_merge(self, other_gene_group):
        gene_keys = list(self.keys)
        gene_keys.extend(other_gene_group.keys)
        return StackGeneGroup(*gene_keys)


class StackGenotype:
    def __init__(self, genes):
        self._genes = genes

    @property
    def genes(self):
        return self._genes

    def keys(self):
        gene_keys = []
        for gene in self._genes:
            gene_keys.extend(gene.keys)
        return gene_keys

    def clone(self):
        return

    def remove(self, index):
        return self._genes.pop(index)

    def add(self, gene_group):
        return self._genes.append(gene_group)

    def __len__(self):
        return len(self._genes)

    def __iter__(self):
        for gene in self._genes:
            yield gene

    def __getitem__(self, index):
        return self._genes[index]


class StackPhenotype:
    def __init__(self, genotype, gene_dictionary):
        self._genotype = genotype
        self._gene_dictionary = gene_dictionary

    def express(self):
        return Stack(
            [self._gene_dictionary[key] for key in self._genotype.keys()])


def stack_crossover_wrapper(gpfunction, stackgenotypes):
    genelist = gpfunction([genotype.genes for genotype in stackgenotypes])
    return StackGenotype(genelist)
