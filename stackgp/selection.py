#!/bin/bash
import random

from .sampling.combinedsampling import replacement_sampler, \
    no_replacement_sampler


def selection_assertion(individual_list, n, with_replacement):
    assert n <= len(individual_list) or with_replacement, \
        "Error, can't return more individuals than the " \
        "population with out replacement"


class Selector:
    def __init__(self, get_worst: bool, replacement: bool):
        self.get_worst = get_worst
        self.replacement = replacement

    def __call__(self, individual_list: list, n: int):
        selection_assertion(individual_list, n, self.replacement)


class ElitistSelector(Selector):
    def __call__(self, individual_list: list, n: int):
        super().__call__(individual_list, n)
        selected = []
        individual_list.sort(reverse=self.get_worst)
        selections_left = n
        while selections_left:
            n_selected = selections_left % len(individual_list)
            selected.extend(individual_list[:n_selected])
            selections_left -= n_selected
        return selected


class FitnessProportionalSelector(Selector):
    def __init__(self, get_worst: bool, replacement: bool):
        super().__init__(get_worst, replacement)
        if get_worst:
            self.fitness_normalizer = self.worst_normalized
        else:
            self.fitness_normalizer = self.best_normalized
        if replacement:
            self.sampler = self.replacement_sample
        else:
            self.sampler = self.no_replacement_sample

    @staticmethod
    def worst_normalized(fitness_sum, fitnesses):
        return [1 - (fitness / fitness_sum) for fitness in fitnesses]

    @staticmethod
    def best_normalized(fitness_sum, fitnesses):
        return [(fitness / fitness_sum) for fitness in fitnesses]

    @staticmethod
    def replacement_sample(individual_list: list, n: int, normalized_fitnesses):
        return replacement_sampler(individual_list, normalized_fitnesses, n)

    @staticmethod
    def no_replacement_sample(individual_list: list, n: int,
                              normalized_fitnesses):
        return no_replacement_sampler(individual_list, normalized_fitnesses, n)

    def __call__(self, individual_list: list, n: int):
        super().__call__(individual_list, n)
        normalized_fitness = [individual.fitness for individual in
                              individual_list]
        fitness_sum = sum(normalized_fitness)
        normalized_fitnesses = self.fitness_normalizer(fitness_sum,
                                                       normalized_fitness)
        return self.sampler(individual_list, n, normalized_fitnesses)


class StochasticSelector(Selector):
    def __init__(self, get_worst: bool, replacement: bool):
        super().__init__(get_worst, replacement)
        if replacement:
            self.sampler = self.replacement_sample
        else:
            self.sampler = self.no_replacement_sample

    @staticmethod
    def replacement_sample(individual_list: list, n: int):
        return random.choices(individual_list, k=n)

    @staticmethod
    def no_replacement_sample(individual_list: list, n: int):
        return random.sample(individual_list, n)

    def __call__(self, individual_list: list, n: int):
        super().__call__(individual_list, n)
        return self.sampler(individual_list, n)


class TournamentSelector(Selector):
    def __init__(self, get_worst: bool, replacement: bool, k: int):
        super().__init__(get_worst, replacement)
        self.fitness_selector = min if get_worst else max
        if replacement:
            self.sampler = self.replacement_sample
        else:
            self.sampler = self.no_replacement_sample
        self.k = k

    def replacement_sample(self, individual_list: list, n: int):
        selected = []
        for tournament_round in range(n):
            contestants = [individual_list[random.randrange(n)] for _ in
                           range(self.k)]
            selected.append(
                self.fitness_selector(contestants, key=lambda x: x.fitness))
        return selected

    def no_replacement_sample(self, individual_list: list, n: int):
        selected = []
        index_dictionary = {i: individual for i, individual in
                            enumerate(individual_list)}
        for tournament_round in range(n):
            contestant_keys = random.choice(list(index_dictionary.keys()),
                                            k=self.k)
            selected_key = self.fitness_selector(contestant_keys,
                                                 key=lambda x: index_dictionary[
                                                     x].fitness)
            selected.append(index_dictionary.pop(selected_key))
        return selected

    def __call__(self, individual_list: list, n: int):
        super().__call__(individual_list, n)
        return self.sampler(individual_list, n)
