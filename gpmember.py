#!/bin/bash
import random
from gpoperators import ERConstantSetOperator


class StackGPMember:
    functional_tuple = None
    terminal_tuple = None
    parsimony_pressure = 0
    max_size = 0

    def __init__(self, init_max_size=0, init_method=None, erk_enabled=True):
        self.gp_operators = None
        self.fitness = None
        self.fitness_iterations = 0
        if init_method == "uniform random":
            if erk_enabled:
                operator_tuple = self.functional_tuple + self.terminal_tuple + (ERConstantSetOperator(),)
            else:
                operator_tuple = self.functional_tuple + self.terminal_tuple
            size = random.randint(1, init_max_size)
            self.gp_operators = tuple(random.choice(operator_tuple) for _ in range(size))

    def update_fitness(self, in_fitness):
        """
        updates the fitness of an individual
        :param fitness: value to be averaged or set for the current individual fitness
        :return:
        """
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
        for operator in self.gp_operators:
            operator(stack)
        return stack

    @classmethod
    def from_recombination(cls, gp_stack_l, gp_stack_r, f_recombine):
        new_gp_stack = cls()
        new_gp_stack.gp_operators = f_recombine(gp_stack_l, gp_stack_r)
        return new_gp_stack

    @classmethod
    def from_mutation(cls, gp_stack, f_mutate):
        new_gp_stack = cls()
        new_gp_stack.gp_operators = f_mutate(gp_stack)
        return new_gp_stack

    @classmethod
    def from_recomb_mutation(cls, gp_stack_l, gp_stack_r, f_recombine, f_mutate):
        recomb_gp_stack = cls.from_recombination(gp_stack_l, gp_stack_r, f_recombine)
        new_gp_stack = cls.from_mutation(recomb_gp_stack, f_mutate)
        return new_gp_stack

    @classmethod
    def set_class_vars(cls, functional_set, terminal_set, parsimony_pressure=0, max_size=0):
        cls.functional_tuple = functional_set
        cls.terminal_tuple = terminal_set
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
