#!/bin/bash
import random
from operator import attrgetter, itemgetter


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
