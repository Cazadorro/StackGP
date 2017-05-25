# !/bin/bash


class PopulationSize:
    def __init__(self, _mu: int, _lambda: int, pairsize: int):
        self._mu = _mu
        self._lambda = _lambda
        self._pairsize = pairsize

    @property
    def maxsize(self):
        return self._mu

    @property
    def offspring(self):
        return self._lambda

    def pairsize(self):
        return self._pairsize


class GeneFunctions:
    def __init__(self, initializer, mutator, recombinator):
        self._initializer = initializer
        self._mutator = mutator
        self._recombinator = recombinator

    def initialize(self, size, genotype_wrapper, member_wrapper):
        return self._initializer(size, genotype_wrapper, member_wrapper)

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

    def select_pairs(self, selected_parents, pair_size):
        return self._parent_selector(selected_parents)

    def select_survivors(self, population):
        return self._survival_selector(population)


class MemberProperties:
    def __init__(self, genotype_class, member_wrapper, fitness_evaluator):
        self._genotype_class = genotype_class
        self._member_wrapper = member_wrapper
        self._fitness_evaluator = fitness_evaluator

    # @TODO do we deal with individual?
    def evaluate(self, individual):
        return individual.eval(self._fitness_evaluator)

    @property
    def genotype_wrapper(self):
        return self._genotype_class

    @property
    def member_wrapper(self):
        return self._member_wrapper


class Population:
    def __init__(self, population_size: PopulationSize,
                 gene_functions: GeneFunctions,
                 selection_functions: SelectionFunctions,
                 member_properties: MemberProperties):
        self._popsize = population_size
        self._mutator = gene_functions
        self._selector = selection_functions
        self._memberprops = member_properties
        self._evaluated = []
        self._unevaluated = []
        self._recombined = []
        self._mutated = []
        self._parents = []
        self._parent_pairs = []
        self._evaluations = 0
        self._generations = 0


    def initialize(self):
        self._evaluated = []
        self._unevaluated = self._mutator.initialize(
            self._popsize.offspring,
            self._memberprops.genotype_wrapper,
            self._memberprops.member_wrapper)
        self._recombined = []
        self._mutated = []
        self._parents = []
        self._parent_pairs = []
        self._evaluations = 0
        self._generations = 0

    # TODO need to do to deal with multiple items for evaluation?
    def evaluate(self, n):
        self._evaluated = [self._memberprops.evaluate(self._evaluated.pop())
                           for _ in range(n)]
        self._evaluations += n

    def select_parents(self):
        self._parents = self._selector.select_parents(self._evaluated)

    def select_pairs(self):
        self._parent_pairs = self._selector.select_pairs(self._parents,
                                                         self._popsize.pairsize)

    # TODO enough list size?
    def recombine(self):
        self._recombined = [self._mutator.recombine(pair) for pair in
                            self._parent_pairs]

    def mutate(self):
        self._mutated = [self._mutator.mutate(individual.genotype) for
                         individual in self._recombined]

    def select_survivors(self):
        self._unevaluated = self._selector.select_survivors(self._mutated)

    def progress_generation(self):
        if self._can_progress():
            self._generations += 1
            print("New Generation: ", self._generations)
            print("\tNumber of members evaluated: ", self._evaluations)
            print('')
            return True
        return False

    def _can_progress(self):
        return (self._evaluations - self._popsize.maxsize) >= (
            self._generations * self._popsize.offspring)

    def get_lambda(self):
        return self._popsize.offspring

    def get_mu(self):
        return self._popsize.maxsize

    @property
    def generations(self):
        return self._generations

    @property
    def evaluations(self):
        return self._evaluations

    @property
    def best(self):
        return max(self._evaluated)