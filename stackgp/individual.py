#!/bin/bash

from typing import List

from .operators import GeneticOperator


class Fitness:
    def __init__(self, initial_fitness=None):
        self._value = initial_fitness
        self.iterations = 0

    def update(self, new_fitness_value):
        self.iterations += 1
        if self._value is None:
            self._value = new_fitness_value
        else:
            numerator = (
                            self._value * (
                                self.iterations - 1)) + new_fitness_value
            self._value = numerator / self.iterations
            # self.fitness *= (self.iterations - 1) / self.iterations
            # self.fitness += (new_fitness / self.iterations)

    def __lt__(self, other: 'Fitness'):
        return self._value < other._value

    def __le__(self, other: 'Fitness'):
        return self._value <= other._value

    def __eq__(self, other: 'Fitness'):
        return self._value == other._value

    def __ne__(self, other: 'Fitness'):
        return self._value != other._value

    def __ge__(self, other: 'Fitness'):
        return self._value >= other._value

    def __gt__(self, other: 'Fitness'):
        return self._value > other._value

    def __str__(self):
        return "fitness : {}".format(self._value)


class Individual:
    def __init__(self, genotype, fitnessclass, fitnessmodfier):
        self._genotype = genotype
        self._fitness = fitnessclass()
        self._modifier = fitnessmodfier

    def eval(self, fitness_evaluator):
        # TODO should gene dictionary be a part of evaluator?
        fitness = fitness_evaluator(self._genotype)
        self._fitness.update(fitness + self._modifier(self))
        return self

    @property
    def genotype(self):
        return self._genotype

    def __lt__(self, other: 'Individual'):
        return self._fitness < other._fitness

    def __le__(self, other: 'Individual'):
        return self._fitness <= other._fitness

    def __eq__(self, other: 'Individual'):
        return self._fitness == other._fitness

    def __ne__(self, other: 'Individual'):
        return self._fitness != other._fitness

    def __ge__(self, other: 'Individual'):
        return self._fitness >= other._fitness

    def __gt__(self, other: 'Individual'):
        return self._fitness > other._fitness

    @property
    def fitness(self):
        return self._fitness


class IndividualFactory:
    def __init__(self, individual_class, fitnessclass, fitnessmodfier):
        self._individual_class = individual_class
        self._fitnessclass = fitnessclass
        self._fitnessmodfier = fitnessmodfier

    def __call__(self, genotype):
        return self._individual_class(genotype, self._fitnessclass,
                                      self._fitnessmodfier)


class ParsimonyPressure:
    def __init__(self, pressure):
        self.pressure = pressure

    def __call__(self, individual: Individual):
        return -1 * (self.pressure * len(individual._genotype))


def print_individual(individual: Individual, opmap: List[GeneticOperator]):
    print(individual.fitness)
    print("-----STACK-----")
    for key in individual.genotype.keys():
        print(opmap[key])
    print("------END------")
