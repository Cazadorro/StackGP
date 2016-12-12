#!/bin/bash
import random
from operator import attrgetter, itemgetter


class EncapsulatedData:
    """
    wrapper for a reference to any primitive or any variable
    """

    def __init__(self, data):
        self.data = data


class EncapsulatedDataUpdater:
    """
    functor wrapper that updates the data
    """

    def __init__(self, encapsulated_data):
        self.e_data = encapsulated_data

    def __call__(self, updated_value):
        self.e_data.data = updated_value


class TerminalStackOperator:
    """
    represents a terminal set member that can operate on a stack
    """

    def __init__(self, encapsulated_data, **kwargs):
        """

        :param encapsulated_data: EncapsulatedData object meant to be modified outside scope of function
        """
        self.encapsulated = encapsulated_data
        if 'name' in kwargs:
            self.name = kwargs['name']

    def __call__(self, stack):
        stack.append(self.encapsulated.data)


class FunctionalStackOperator:
    def __init__(self, function, num_args, **kwargs):
        self.function = function
        self.num_args = num_args
        if 'name' in kwargs:
            self.name = kwargs['name']

    def __call__(self, stack):
        if len(stack) >= self.num_args:
            arguments = [stack.pop() for _ in range(self.num_args)]
            stack.append(self.function(*arguments))


class ERandomConstantStackOperator:
    min_range = None
    max_range = None
    _name = "ERK"

    def __init__(self):
        self.data = None

    def __call__(self, stack):
        if self.data is None:
            self.data = random.uniform(self.min_range, self.max_range)
        stack.append(self.data)

    @classmethod
    def set_range(cls, min_range, max_range):
        cls.min_range = min_range
        cls.max_range = max_range

    @property
    def name(self):
        return self._name + " " + str(self.data)


class GPStackTuple:
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
                operator_tuple = self.functional_tuple + self.terminal_tuple + (ERandomConstantStackOperator(),)
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

    def eval(self, expected_list):
        """
        terminals must be updated before
        :param expected_list: list of expected values
        :return:
        """

        num_out = len(expected_list)
        stack = []
        for operator in self.gp_operators:
            operator(stack)

        yhat = []
        for i in range(num_out):
            if len(stack) > 0:
                yhat.append(stack.pop())
            else:
                yhat.append(None)
        fitness = 0
        for i in range(num_out):
            if yhat[i] is not None:
                fitness -= abs(yhat[i] - expected_list[i])
            else:
                fitness -= abs(expected_list[i]) ** 3
        self.update_fitness(fitness)
        return yhat

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
    def set_class_vars(cls, functional_set, terminal_set, parsimony_pressure = 0, max_size=0):
        cls.functional_tuple = functional_set
        cls.terminal_tuple = terminal_set
        cls.parsimony_pressure = parsimony_pressure
        cls.max_size = max_size


def recombine(gp_stack_l, gp_stack_r):
    gp_operators = []
    min_gp_stack = min(gp_stack_l, gp_stack_r, key=len)
    max_gp_stack = max(gp_stack_r, gp_stack_l, key=len)
    gp_len_diff = len(max_gp_stack) - len(min_gp_stack)
    for i in range(len(min_gp_stack)):
        if random.randint(0, 1):
            gp_operators.append(min_gp_stack[i])
        else:
            gp_operators.append(max_gp_stack[i])

    new_len = len(min_gp_stack) + random.randint(0, gp_len_diff)
    for i in range(len(min_gp_stack), new_len):
        gp_operators.append(max_gp_stack[i])

    return tuple(gp_operators)


def mutate(gp_stack):
    gp_operators = []
    operator_tuple = GPStackTuple.functional_tuple + GPStackTuple.terminal_tuple
    for operator in gp_stack:
        r = random.randint(0, 2)
        if r == 0:
            pass
        elif r == 1:
            gp_operators.append(operator)
        elif r == 2:
            gp_operators.append(operator)
            gp_operators.append(random.choice(operator_tuple))
    return tuple(gp_operators)


def n_elitist(gp_stack_list, num_returned):
    sorted_stacks = sorted(gp_stack_list, key=attrgetter('fitness'), reverse=True)
    return sorted_stacks[:num_returned]


def stochastic_parent_selection(gp_stack_list, num_children):
    parents1 = []
    parents2 = []
    for i in range(num_children):
        parents1.append(random.choice(gp_stack_list))
        parents2.append(random.choice(gp_stack_list))
    return parents1, parents2
