#!/bin/bash

import operator
import random
from operator import attrgetter, itemgetter

from gpoperators import FunctionalSetOperator, TerminalSetOperator, ERConstantSetOperator, EncapsulatedData
from gpselection import n_elitist, stochastic_parent_selection
from gpmutation import mutate
from gprecombination import recombine
from gpmember import StackGPMember
from gppopulation import StackGPPopulation
from gpinitialization import uniform_initialization


def function_evaluate(gp_stack, expected_list):
    """
    terminals must be updated before
    :param expected_list: list of expected values
    :return:
    """

    num_out = len(expected_list)
    output_stack = gp_stack.evaluate()

    yhat = []
    for i in range(num_out):
        if len(output_stack) > 0:
            yhat.append(output_stack.pop())
        else:
            yhat.append(None)
    fitness = 0
    prev_diff = 1
    inc_diff = 0
    num_correct = 0
    num_incorrect = -1
    for i in range(num_out):
        if yhat[i] is not None:
            absdiff = abs((yhat[i] - expected_list[i]))
            fitness -= absdiff
            if absdiff == 0:
                prev_diff *= (prev_diff + 1)
                num_correct += 1
            else:
                if inc_diff == 0:
                    inc_diff = 1
                else:
                    inc_diff *= (inc_diff + 1)
        else:
            fitness -= abs(expected_list[i]) ** 3
    num_incorrect = len(yhat) - num_correct
    # fitness += prev_diff
    fitness -= inc_diff
    if num_incorrect == 0:
        fitness += 10
    gp_stack.update_fitness(fitness)
    return yhat


def protected_div(a, b):
    """
    returns a/b unless b == 0, in which case returns 1
    :param a:
    :param b:
    :return:
    """

    if b == 0:
        return 1
    return operator.truediv(a, b)


def main():
    target_function = lambda x: 0.5 * (x ** 2)

    add = FunctionalSetOperator(operator.add, 2, name="add")
    sub = FunctionalSetOperator(operator.sub, 2, name="sub")
    div = FunctionalSetOperator(protected_div, 2, name="div")
    mul = FunctionalSetOperator(operator.mul, 2, name="mul")
    functional_operators = (add, sub, div, mul)
    X = EncapsulatedData(0)
    terminal_x = TerminalSetOperator(X, name="x")
    terminal_operators = (terminal_x,)
    ERConstantSetOperator.set_range(-10, 10)
    StackGPMember.set_class_vars(0.1, 10)
    operator_tuple = functional_operators + terminal_operators + (ERConstantSetOperator(),)
    operator_tuple = functional_operators + terminal_operators

    gp_mu = 50
    gp_lambda = 25
    max_evals = 100

    x_vals = [0, 1, 2, 4, 8, 16, 32]
    y_vals = [target_function(x) for x in x_vals]

    population = StackGPPopulation(gp_mu, gp_lambda, operator_tuple, uniform_initialization, recombine, mutate,
                                   stochastic_parent_selection, n_elitist)

    for eval_num in range(max_evals):
        unevaluated = population.loan_unevaluated()
        evaluated = []
        for member in unevaluated:
            for test_set_i in range(len(x_vals)):
                X.data = x_vals[test_set_i]
                function_evaluate(member, [y_vals[test_set_i]])
            evaluated.append(member)
        population.return_unevaluated(evaluated)
        population.progress_generation()
        # for member in population.evaluated:
        #     member.print_stack()
        #     print(member.fitness)

    best_member = max(population.evaluated, key=attrgetter('fitness'))

    for test_set_i in range(len(x_vals)):
        X.data = x_vals[test_set_i]
        print("stack eval = ", function_evaluate(best_member, [y_vals[test_set_i]]), " y eval = ", [y_vals[test_set_i]])
    best_member.print_stack()
    print(best_member.fitness)


if __name__ == "__main__":
    # run main program
    main()
