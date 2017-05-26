# !/bin/bash

from structures import Stack, DataSource
from genetics import StackPhenotype
from typing import List, Callable, Any
from structures import EncapsulatedData


def evaluate_operator_stack(operator_stack):
    vm_structures = {
        DataSource.OperatorStack: operator_stack,
        DataSource.ResultStack: Stack(),
        DataSource.ExecutionStack: Stack(),
    }
    while not operator_stack.empty():
        operator = operator_stack.pop()[0]
        result_destination = operator.get_destination(vm_structures)
        result = operator(vm_structures)
        result_destination.push(result)
    return vm_structures[DataSource.ResultStack]


def evaluate_gene_expression(stack_genotype, gene_dictionary) -> Stack:
    phenotype = StackPhenotype(stack_genotype, gene_dictionary)
    expression_operators = phenotype.express()
    return evaluate_operator_stack(expression_operators)


def evaluate_using_result(stack_genotype, gene_dictionary,
                          fitness_evaluator):
    return fitness_evaluator(
        evaluate_gene_expression(stack_genotype, gene_dictionary))


class TerminalDataSet:
    def __init__(self, operator_map, terminal_operators,
                 terminal_inputs: List[List[Any]],
                 terminal_results: List[List[Any]]):
        assert len(terminal_results[0]) <= len(terminal_operators)

        self._operator_map = operator_map
        self._terminal_operators = terminal_operators
        self._inputs_list = terminal_inputs
        self._results_list = terminal_results

        self._input_result_zip = list(
            zip(self._inputs_list, self._results_list))

    @property
    def opmap(self):
        return self._operator_map

    def terminal_setting_generator(self):
        for input_data, result_data in self._input_result_zip:
            for terminal, data in zip(self._terminal_operators, input_data):
                terminal.value = data
            yield result_data


class FitnessEvaluator:
    def __init__(self, fitness_function: Callable,
                 terminal_dataset: TerminalDataSet):
        self._fitness_fuction = fitness_function
        self._dataset = terminal_dataset

    def _evaluate(self, stack_genotype):
        raise NotImplementedError

    def __call__(self, stack_genotype):
        return self._evaluate(stack_genotype)


class BasicFitnessEvaluator(FitnessEvaluator):
    def _evaluate(self, stack_genotype):
        fitness = 0
        for expected_vector in self._dataset.terminal_setting_generator():
            result_stack = evaluate_gene_expression(stack_genotype,
                                                    self._dataset.opmap)
            fitness += self._fitness_fuction(result_stack, expected_vector)
        return fitness


class CountCorrectFitnessEvaluator(FitnessEvaluator):
    def __init__(self, fitness_function: Callable,
                 terminal_dataset: TerminalDataSet,
                 count_weight: float,
                 diff_tolerance: float = 0):
        super().__init__(fitness_function, terminal_dataset)
        self._count_weight = count_weight
        self._tolerance = diff_tolerance

    def _evaluate(self, stack_genotype):
        fitness = 0
        correct_count = 0
        for expected_vector in self._dataset.terminal_setting_generator():
            result_stack = evaluate_gene_expression(stack_genotype,
                                                    self._dataset.opmap)
            sub_fitness = self._fitness_fuction(result_stack, expected_vector)
            if abs(sub_fitness) == self._tolerance:
                correct_count += 1
            fitness += sub_fitness
        count_score = self._count_weight ** correct_count if correct_count != 0 else 0
        return fitness + count_score


def absolute_error_fitness_function(result_stack: Stack,
                                    expected_vector: List[Any]):
    fitness = 0
    for expected in expected_vector:
        if result_stack.empty():
            fitness -= 10
        else:
            calculated = result_stack.pop()[0]
            if expected > calculated:
                A = calculated
                B = expected
            else:
                A = expected
                B = calculated
            if A == 0:
                A = .000000000001
            fitness += -abs((A - B) / A)
    return fitness
