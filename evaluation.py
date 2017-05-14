#!/bin/bash

from structures import Stack, DataSource
from genetics import StackPhenotype


def evaluate_operator_stack(operator_stack):
    vm_structures = {
        DataSource.OperatorStack: operator_stack,
        DataSource.ResultStack: Stack(),
        DataSource.ExecutionStack: Stack(),
    }
    while not operator_stack.empty():
        operator = operator_stack.pop()
        result_destination = operator.get_destination(vm_structures)
        result = operator(vm_structures)
        result_destination.push(result)
    return vm_structures[DataSource.ResultStack]


def evaluate_gene_expression(stack_genotype, gene_dictionary):
    phenotype = StackPhenotype(stack_genotype, gene_dictionary)
    expression_operators = phenotype.express()
    return evaluate_operator_stack(expression_operators)
