#!/bin/bash
from .structures import DataSource

from .operators import MultiSourceOperator


def xpush_func(result_stack, operator_stack):
    n = result_stack.pop()
    return operator_stack.pop(n)


def xpop_func(execution_stack):
    return execution_stack.pop()


def xpick_func(result_stack, execution_stack):
    depth = result_stack.pop()
    return execution_stack.pick(depth)


xpush = MultiSourceOperator(xpush_func,
                            [DataSource.ResultStack, DataSource.OperatorStack])

xpop = MultiSourceOperator(xpop_func, [DataSource.ExecutionStack])

xpick = MultiSourceOperator(xpick_func,
                            [DataSource.ResultStack, DataSource.ExecutionStack])
