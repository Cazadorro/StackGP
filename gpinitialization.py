#!/bin/bash
from gpmember import StackGPMember
import random

max_init_size = 10


def uniform_initialization(gp_mu, operator_tuple, init_max_size = max_init_size):
    size = random.randint(1, init_max_size)
    gp_operators = tuple(random.choice(operator_tuple).clone() for _ in range(size))
    return [StackGPMember(gp_operators) for _ in range(gp_mu)]
