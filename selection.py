#!/bin/bash
import random
from functools import wraps
from operator import attrgetter, itemgetter


def selection_decorator(func):
    @wraps(func)
    def selection_with_assertion(*args, **kwargs):
        selection_assertion(*args, **kwargs)
        return func(*args, **kwargs)

    return selection_with_assertion


def selection_assertion(n, individual_list, with_replacement):
    assert n <= len(individual_list) or with_replacement, \
        "Error, can't return more individuals than the " \
        "population with out replacement"


def n_elitist(gp_stack_list, num_returned):
    sorted_stacks = sorted(gp_stack_list, key=attrgetter('fitness'),
                           reverse=True)
    return sorted_stacks[:num_returned]


def stochastic_parent_selection(gp_stack_list, num_children):
    parents1 = []
    parents2 = []
    for i in range(num_children):
        parents1.append(random.choice(gp_stack_list))
        parents2.append(random.choice(gp_stack_list))
    return parents1, parents2


# TODO, need with/without replacement, and ability to select for worst or best
def n_elitst(individual_list, n, *, get_worst, with_replacement):
    selection_assertion(n, individual_list, with_replacement)
    selected = []
    individual_list.sort(reverse=get_worst)
    selections_left = n
    while selections_left:
        n_selected = selections_left % len(individual_list)
        selected.extend(individual_list[:n_selected])
        selections_left -= n_selected
    return selected


def fitness_proportional(individual_list, n, *, get_worst, with_replacement):
    selection_assertion(n, individual_list, with_replacement)

    pass


def stochastic_selection(individual_list, n, *, get_worst, with_replacement):
    selection_assertion(n, individual_list, with_replacement)
    pass


def k_tournament_selection(individual_list, n, *, get_worst, with_replacement):
    selection_assertion(n, individual_list, with_replacement)
    pass
