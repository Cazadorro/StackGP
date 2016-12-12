#!/bin/bash
from gpmember import StackGPMember
import random


def mutate(gp_stack):
    """
    mutates given stochastic chance
    :param gp_stack:
    :return:
    """
    gp_operators = []
    operator_tuple = StackGPMember.functional_tuple + StackGPMember.terminal_tuple
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
