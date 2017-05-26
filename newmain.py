#!/bin/bash

import population as pop
import initialization as init
import mutation as mut
import recombination as recom
import parentpairing as pairing
import selection as sel
from generators import uniform_elem_generator, uniform_gene_generator
from enum import IntEnum, unique
from operators import TerminalSetOperator
from structures import EncapsulatedData
from arithmeticoperators import addOp, subOp, mulOp, divOp
from evaluation import BasicFitnessEvaluator, TerminalDataSet, \
    absolute_error_fitness_function, CountCorrectFitnessEvaluator
from structures import Stack
from genetics import StackGenotype
from individual import Individual, print_individual, IndividualFactory, \
    ParsimonyPressure, Fitness


@unique
class OpEnum(IntEnum):
    add = 0
    sub = 1
    mul = 2
    div = 3
    x = 4


def pow2datasetgen(xlist: list):
    return [x ** 2 for x in xlist]


def main():
    popsize = pop.PopulationSize(10, 5, 2, 16)
    x = EncapsulatedData(None)
    termx = TerminalSetOperator(x, "X")
    op_list = [addOp, subOp, mulOp, divOp, termx]
    terminals = [x]

    op_enums = [OpEnum.add, OpEnum.sub, OpEnum.mul, OpEnum.div, OpEnum.x]
    gene_generator = uniform_gene_generator(op_enums)
    mutator_list = [mut.duplicate, mut.replace, mut.insert, mut.delete,
                    mut.reorder, mut.merge]
    mutator_generator = uniform_elem_generator(mutator_list)
    initializer = init.GeneratorInitializer(gene_generator)
    mutator = mut.Mutator(mutator_generator, gene_generator, 0.1)
    recombinator = recom.UniformCrossover()
    genefunc = pop.GeneFunctions(initializer, mutator, recombinator)
    parent_selector = sel.StochasticSelector(True, True)
    pairing_selector = pairing.stochastic_pairing
    survival_selector = sel.ElitistSelector(True, True)
    selectfunc = pop.SelectionFunctions(parent_selector, pairing_selector,
                                        survival_selector)
    data_x = [[-1000], [-10], [-1], [-0.1], [0], [0.1], [1], [10], [1000]]
    expected_x = pow2datasetgen([x[0] for x in data_x])
    expected_x = [[x] for x in expected_x]
    terminal_dataset = TerminalDataSet(op_list, terminals, data_x, expected_x)
    fitness_evaluator = CountCorrectFitnessEvaluator(
        absolute_error_fitness_function,
        terminal_dataset, 2)

    modifier = ParsimonyPressure(4)
    individual_wrapper = IndividualFactory(Individual, Fitness,
                                           modifier)
    popmemparam = pop.MemberProperties(StackGenotype, individual_wrapper,
                                       fitness_evaluator)
    population = pop.Population(popsize, genefunc, selectfunc, popmemparam)

    population.initialize()
    population.evaluate(population.get_mu())
    while population.generations < 10:
        print("new round")
        population.select_parents()
        print("evaluated parents")
        population.select_pairs()
        print("selected pairs")
        population.recombine()
        print("recombined")
        population.mutate()
        print("mutated")
        population.select_survivors()
        print("selected survivors")
        population.progress_generation()
        print("progressed to the next generation")
        population.evaluate(population.get_lambda())
        print_individual(population.best, op_list)
    pass


if __name__ == "__main__":
    # run main program
    main()
