# !/bin/bash


class PopulationSize:
    def __init__(self, _mu, _lambda):
        self._mu = _mu
        self._lambda = _lambda

    @property
    def maxsize(self):
        return self._mu

    @property
    def offspring(self):
        return self._lambda


class GeneFunctions:
    def __init__(self, initializer, mutator, recombinator):
        self._initializer = initializer
        self._mutator = mutator
        self._recombinator = recombinator

    def initialize(self, individual_wrapper):
        return self._initializer(individual_wrapper)

    def mutate(self, genotype):
        return self._mutator(genotype)

    def recombine(self, genotypes):
        return self._recombinator(genotypes)


class SelectionFunctions:
    def __init__(self, parent_selector, pairing_selector, survival_selector):
        self._parent_selector = parent_selector
        self._pairing_selector = pairing_selector
        self._survival_selector = survival_selector

    def select_parents(self, population):
        return self._parent_selector(population)

    def select_pairs(self, selected_parents):
        return self._parent_selector(selected_parents)

    def select_survivors(self, population):
        return self._survival_selector(population)


class PopulationMemberParam:
    def __init__(self, gene_class, evaluator, gene_individual_wrapper):
        self._gene_class = gene_class
        self._evaluator = evaluator
        self._gene_individual_wrapper = gene_individual_wrapper

    # @TODO do we deal with individual?
    def evaluate(self, individual):
        return self._evaluator(individual)

    @property
    def gene_wrapper(self):
        return self._gene_individual_wrapper


class Population:
    def __init__(self, population_size: PopulationSize,
                 gene_functions: GeneFunctions,
                 selection_functions: SelectionFunctions,
                 population_member: PopulationMemberParam):
        self._popsize = population_size
        self._mutator = gene_functions
        self._selector = selection_functions
        self._memberparams = population_member
        self._evaluated = []
        self._unevaluated = self._mutator.initialize(
            self._memberparams.gene_wrapper)
        self._recombined = []
        self._mutated = []
        self._parents = []
        self._parent_pairs = []
        self._evaluations = 0
        self._generations = 0

    def evaluate(self, n):
        self._evaluated = [self._memberparams.evaluate(self._evaluated.pop())
                           for _ in range(n)]
        self._evaluations += n

    def select_parents(self):
        self._parents = self._selector.select_parents(self._evaluated)

    def select_pairs(self):
        self._parent_pairs = self._selector.select_pairs(self._parents)

    # TODO enough list size?
    def recombine(self):
        self._recombined = [self._mutator.recombine(pair) for pair in
                            self._parent_pairs]

    def mutate(self):
        self._mutated = [self._mutator.mutate(genotype) for genotype in
                         self._recombined]

    def select_survivors(self):
        self._unevaluated = self._selector.select_survivors(self._mutated)

    def progress_generation(self):
        if self._can_progress():
            self._generations += 1
            print("New Generation: ", self._generations)
            print("\tNumber of members evaluated: ", self._evaluations)
            print('')

    def _can_progress(self):
        return (self._evaluations - self._popsize.maxsize) >= (
        self._generations * self._popsize.maxsize)
