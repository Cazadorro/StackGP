#!/bin/bash

import operator
import random
from operator import attrgetter, itemgetter

from gpoperators import FunctionalSetOperator, TerminalSetOperator, ERConstantSetOperator, EncapsulatedData
from gpselection import n_elitist, stochastic_parent_selection
from gpmutation import mutate
from gprecombination import recombine
from gpmember import StackGPMember


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
    for i in range(num_out):
        if yhat[i] is not None:
            absdiff = abs((yhat[i] - expected_list[i]))
            fitness -= absdiff
            if absdiff == 0:
                prev_diff *= (prev_diff + 1)
        else:
            fitness -= abs(expected_list[i]) ** 10
    fitness += prev_diff
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
    target_function = lambda x: x ** 4

    add = FunctionalSetOperator(operator.add, 2, name="add")
    sub = FunctionalSetOperator(operator.sub, 2, name="sub")
    div = FunctionalSetOperator(protected_div, 2, name="div")
    mul = FunctionalSetOperator(operator.mul, 2, name="mul")
    functional_operators = (add, sub, div, mul)
    X = EncapsulatedData(0)
    terminal_x = TerminalSetOperator(X, name="x")
    terminal_operators = (terminal_x,)
    ERConstantSetOperator.set_range(-10, 10)
    StackGPMember.set_class_vars(functional_operators, terminal_operators, 0.5)

    _mu = 400
    _lambda = 300
    left_over = _mu - _lambda
    max_gp_size = 10
    uneval_stack_list = [StackGPMember(max_gp_size, "uniform random", erk_enabled=False) for _ in range(_mu)]
    eval_stack_list = []
    max_evals = 200

    x_vals = [-1, -2, -3, 1, 2, 3]
    y_vals = [target_function(x) for x in x_vals]
    for eval_num in range(max_evals):
        # evaluating
        for unevaled in uneval_stack_list:
            for test_set_i in range(len(x_vals)):
                X.data = x_vals[test_set_i]
                function_evaluate(unevaled, [y_vals[test_set_i]])
            eval_stack_list.append(unevaled)
        uneval_stack_list = []
        parents1, parents2 = stochastic_parent_selection(eval_stack_list, _lambda)
        for i in range(_lambda):
            uneval_stack_list.append(StackGPMember.from_recomb_mutation(parents1[i], parents2[i], recombine, mutate))
        if eval_num < max_evals - 1:
            eval_stack_list = n_elitist(eval_stack_list, left_over)
        print(eval_num)
    best_member = max(eval_stack_list, key=attrgetter('fitness'))
    for test_set_i in range(len(x_vals)):
        X.data = x_vals[test_set_i]
        print("stack eval = ", function_evaluate(best_member, [y_vals[test_set_i]]), " y eval = ", [y_vals[test_set_i]])

    best_member.print_stack()


if __name__ == "__main__":
    # run main program
    main()
