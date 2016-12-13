#!/bin/bash
from gpmember import StackGPMember
import random


def mutate(gp_stack, operator_tuple):
    """
    mutates given stochastic chance
    :param gp_stack:
    :return:
    """
    mutation_chance = 1.0
    gp_operators = []
    for operator in gp_stack:
        if random.random() < mutation_chance:
            r = random.randint(0, 2)
            if r == 0:
                pass
            elif r == 1:
                gp_operators.append(random.choice(operator_tuple).clone())
            elif r == 2:
                gp_operators.append(random.choice(operator_tuple).clone())
                gp_operators.append(operator)
        else:
            gp_operators.append(operator)
    if random.random() < mutation_chance:
        gp_operators.append(random.choice(operator_tuple).clone())
    return StackGPMember(tuple(gp_operators))
