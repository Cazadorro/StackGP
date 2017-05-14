#!/bin/bash

from genetics import StackPhenotype


class Fitness:
    def __init__(self):
        self._value = None
        self.iterations = 0

    def update(self, new_fitness_value):
        self.iterations += 1
        if self._value is None:
            self._value = new_fitness_value
        else:
            numerator = (
                        self._value * (self.iterations - 1)) + new_fitness_value
            self._value = numerator / self.iterations
            # self.fitness *= (self.iterations - 1) / self.iterations
            # self.fitness += (new_fitness / self.iterations)

    def __lt__(self, other):
        return self._value < other._value

    def __le__(self, other):
        return self._value <= other._value

    def __eq__(self, other):
        return self._value == other._value

    def __ne__(self, other):
        return self._value != other._value

    def __ge__(self, other):
        return self._value >= other._value

    def __gt__(self, other):
        return self._value > other._value


class Individual:
    def __init__(self, genotype):
        self.genotype = genotype
        self.fitness = Fitness()

    def eval(self, fitness_evaluator):
        # TODO should gene dictionary be a part of evaluator?
        fitness = fitness_evaluator(self.genotype)
        self.fitness.update(fitness)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness
