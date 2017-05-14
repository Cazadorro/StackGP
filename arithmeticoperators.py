#!/bin/bash

from operators import FunctionalSetOperator
from operator import add, sub, truediv, mul

addOp = FunctionalSetOperator(add)
subOp = FunctionalSetOperator(sub)
divOp = FunctionalSetOperator(truediv)
mulOp = FunctionalSetOperator(mul)