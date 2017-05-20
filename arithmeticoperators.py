#!/bin/bash

from operators import FunctionalSetOperator
from operator import add, sub, truediv, mul


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


addOp = FunctionalSetOperator(add)
subOp = FunctionalSetOperator(sub)
divOp = FunctionalSetOperator(protected_div)
mulOp = FunctionalSetOperator(mul)
