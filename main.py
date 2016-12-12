#!/bin/bash
from stackgpdef import FunctionalStackOperator, TerminalStackOperator, GPStackTuple, EncapsulatedData, \
    ERandomConstantStackOperator, n_elitist, stochastic_parent_selection, mutate, recombine
import operator
import random
from operator import attrgetter, itemgetter


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
    target_function = lambda x: 0.5 * x ** 2

    add = FunctionalStackOperator(operator.add, 2, name="add")
    sub = FunctionalStackOperator(operator.sub, 2, name="sub")
    div = FunctionalStackOperator(protected_div, 2, name="div")
    mul = FunctionalStackOperator(operator.mul, 2, name="mul")
    functional_operators = (add, sub, div, mul)
    X = EncapsulatedData(0)
    terminal_x = TerminalStackOperator(X, name="x")
    terminal_operators = (terminal_x,)
    ERandomConstantStackOperator.set_range(-10, 10)
    GPStackTuple.set_class_vars(functional_operators, terminal_operators, 0.3)

    _mu = 400
    _lambda = 300
    left_over = _mu - _lambda
    max_gp_size = 10
    uneval_stack_list = [GPStackTuple(max_gp_size, "uniform random", erk_enabled=False) for _ in range(_mu)]
    eval_stack_list = []
    max_evals = 40

    x_vals = [-1, 7, 23, 578, 23455, 9, 65, 5003]
    y_vals = [target_function(x) for x in x_vals]
    for eval_num in range(max_evals):
        # evaluating
        for unevaled in uneval_stack_list:
            for test_set_i in range(len(x_vals)):
                X.data = x_vals[test_set_i]
                unevaled.eval([y_vals[test_set_i]])
            eval_stack_list.append(unevaled)
        uneval_stack_list = []
        parents1, parents2 = stochastic_parent_selection(eval_stack_list, _lambda)
        for i in range(_lambda):
            uneval_stack_list.append(GPStackTuple.from_recomb_mutation(parents1[i], parents2[i], recombine, mutate))
        if eval_num < max_evals - 1:
            eval_stack_list = n_elitist(eval_stack_list, left_over)
        print(eval_num)
    best_member = max(eval_stack_list, key=attrgetter('fitness'))
    for test_set_i in range(len(x_vals)):
        X.data = x_vals[test_set_i]
        print("stack eval = ", best_member.eval([y_vals[test_set_i]]), " y eval = ", [y_vals[test_set_i]])

    print("Top")
    print("-----")
    for member in best_member[::-1]:
        print(member.name)
    print("-----")
    print("Bottom")


if __name__ == "__main__":
    # run main program
    main()
