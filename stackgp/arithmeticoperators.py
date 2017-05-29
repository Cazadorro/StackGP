#!/bin/bash

from operator import add, sub, truediv, mul

from .operators import FunctionalSetOperator


def protected_div(a, b):
    """
    returns a/b unless b == 0, in which case returns 1
    :param a:
    :param b:
    :return:
    """

    if b == 0:
        return 1
    return truediv(a, b)

def ADD(a, b):
    return add(a, b)

def SUB(a, b):
    return sub(a, b)

def MUL(a, b):
    return mul(a, b)


addOp = FunctionalSetOperator(ADD, "ADD")
subOp = FunctionalSetOperator(SUB, "SUB")
divOp = FunctionalSetOperator(protected_div, "DIV")
mulOp = FunctionalSetOperator(MUL, "MUL")
