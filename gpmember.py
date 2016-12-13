#!/bin/bash
import random
from gpoperators import ERConstantSetOperator


class StackGPMember:
    parsimony_pressure = 0
    max_size = 0

    def __init__(self, operator_tuple):
        self.gp_operators = operator_tuple
        self.fitness = None
        self.fitness_iterations = 0

    def update_fitness(self, in_fitness):
        """
        updates the fitness of an individual
        :param fitness: value to be averaged or set for the current individual fitness
        :return:
        """
        temp = (self.parsimony_pressure * len(self.gp_operators))
        fitness = in_fitness - (self.parsimony_pressure * len(self.gp_operators))
        if self.fitness_iterations == 0:
            self.fitness = 0
        self.fitness_iterations += 1
        self.fitness *= (self.fitness_iterations - 1) / self.fitness_iterations
        self.fitness += (fitness / self.fitness_iterations)

    def __len__(self):
        return len(self.gp_operators)

    def __getitem__(self, index):
        return self.gp_operators[index]

    def evaluate(self):
        """
        evaluates the member, assumes variables have been set outside for terminals
        :return:
        """
        stack = []
        # @todo possible for gp_operators to be NoneType?
        for operator in self.gp_operators:
            operator(stack)
        return stack

    @classmethod
    def set_class_vars(cls, parsimony_pressure=0, max_size=0):
        cls.parsimony_pressure = parsimony_pressure
        cls.max_size = max_size

    def print_stack(self):
        print("    Top    ")
        print("-----------")
        index = len(self.gp_operators)
        for gp_op in self.gp_operators[::-1]:
            index -= 1
            print(str(index) + ": " + gp_op.name)
        print("----------")
        print("  Bottom  ")
