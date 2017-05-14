#!/bin/bash

import inspect
from structures import DataSource, EncapsulatedData


def get_arg_limit(arg_spec):
    if arg_spec.varargs is not None:
        return float('inf')
    return len(arg_spec.args)


def get_number_args(func):
    arg_spec = inspect.getfullargspec(func)
    return get_arg_limit(arg_spec)


class GeneticOperator:
    argument_source = DataSource.NoSource
    result_destination = DataSource.ResultStack

    @staticmethod
    def _get_virtual_machine_structure(vm_structures, structure_key):
        return vm_structures[
            structure_key] if structure_key in vm_structures else None

    @classmethod
    def get_arguments(cls, vm_structures):
        return cls._get_virtual_machine_structure(vm_structures,
                                                  cls.argument_source)

    @classmethod
    def get_destination(cls, vm_structures):
        return cls._get_virtual_machine_structure(vm_structures,
                                                  cls.result_destination)


class FunctionalSetOperator(GeneticOperator):
    argument_source = DataSource.OperatorStack

    def __init__(self, func):
        self.num_args = get_number_args(func)
        self.func = func

    def __call__(self, vm_structures):
        result_stack = self.get_arguments(vm_structures)
        if self.num_args >= len(result_stack):
            arguments = result_stack.pop(self.num_args)
            return self.func(*arguments)
        return None


class TerminalSetOperator(GeneticOperator):
    def __init__(self, data: EncapsulatedData):
        self.data = data

    def __call__(self, ignore):
        return self.data.value


class MultiSourceOperator(GeneticOperator):
    result_destination = DataSource.OperatorStack

    def __init__(self, exec_func, arg_source_list):
        self.func = exec_func
        self.arg_source_list = arg_source_list

    def __call__(self, vm_structures):
        arguments = [vm_structures[arg] for arg in self.arg_source_list]
        return self.func(*arguments)