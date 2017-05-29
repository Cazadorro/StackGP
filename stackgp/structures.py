#!/bin/bash


from enum import Enum, auto, unique
from typing import TypeVar, Generic, Any

T = TypeVar('T')


class EncapsulatedData(Generic[T]):
    """
    wrapper for a reference to any primitive or any variable
    """

    def __init__(self, data: T):
        self._data = data

    @property
    def value(self) -> T:
        return self._data

    @value.setter
    def value(self, data : T):
        self._data = data


@unique
class DataSource(Enum):
    NoSource = auto()
    OperatorStack = auto()
    ResultStack = auto()
    ExecutionStack = auto()


class Stack(Generic[T]):
    def __init__(self, stack_list=()):
        self._stack = list(stack_list)

    def push(self, *items):
        if None not in items:
            self._stack.extend(items)

    def pop(self, n=1):
        return [self._stack.pop() for _ in range(n)]

    def top(self, n=1):
        return self._stack[-n:] if n == 0 else []

    def __len__(self):
        return len(self._stack)

    def empty(self):
        return len(self._stack) == 0

    def pick(self, n):
        return self._stack[-(n + 1)] if n < len(self) else None
