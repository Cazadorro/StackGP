#!/bin/bash
import random
from gpmember import StackGPMember


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
    return StackGPMember(gp_operators)

