# !/bin/bash


class PopulationSize:
    def __init__(self, _mu: int, _lambda: int, pairsize: int, initsize: int):
        self._mu = _mu
        self._lambda = _lambda
        self._pairsize = pairsize
        self._initsize = initsize
        self._parentsize = self._pairsize * self._lambda
        self._survivesize = self._mu - self._lambda if self._mu > self._lambda else 0

    @property
    def maxsize(self):
        return self._mu

    @property
    def offspring(self):
        return self._lambda

    @property
    def pairsize(self):
        return self._pairsize

    @property
    def initsize(self):
        return self._initsize

    @property
    def parentsize(self):
        return self._parentsize

    @property
    def survivesize(self):
        return self._survivesize


class GeneFunctions:
    def __init__(self, initializer, mutator, recombinator):
        self._initializer = initializer
        self._mutator = mutator
        self._recombinator = recombinator

    def initialize(self, size, wrapper):
        return self._initializer(size, wrapper)

    def mutate(self, genotype, wrapper):
        return self._mutator(genotype, wrapper)

    def recombine(self, genotypes, wrapper):
        return self._recombinator(genotypes, wrapper)


class SelectionFunctions:
    def __init__(self, parent_selector, pairing_selector, survival_selector):
        self._parent_selector = parent_selector
        self._pairing_selector = pairing_selector
        self._survival_selector = survival_selector

    def select_parents(self, population, n):
        return self._parent_selector(population, n)

    def select_pairs(self, selected_parents, pair_size):
        return self._pairing_selector(selected_parents, pair_size)

    def select_survivors(self, population, n):
        return self._survival_selector(population, n)


class MemberProperties:
    def __init__(self, genotype_class, member_wrapper, fitness_evaluator):
        self._genotype_class = genotype_class
        self._member_wrapper = member_wrapper
        self._fitness_evaluator = fitness_evaluator

        def wrapper(gene): return member_wrapper(genotype_class(gene))

        self._wrapper = wrapper

    # @TODO do we deal with individual?
    def evaluate(self, individual):
        return individual.eval(self._fitness_evaluator)

    @property
    def genotype_wrapper(self):
        return self._genotype_class

    @property
    def member_wrapper(self):
        return self._member_wrapper

    @property
    def wrapper(self):
        return self._wrapper


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
        self._unevaluated = [self._mutator.initialize(
            self._popsize.initsize,
            self._memberprops.wrapper) for _ in
            range(self._popsize.maxsize)]
        self._recombined = []
        # self._mutated = []
        self._parents = []
        self._parent_pairs = []
        self._evaluations = 0
        self._generations = 0

    # TODO need to do to deal with multiple items for evaluation?
    def evaluate(self, n):
        self._evaluated.extend(
            [self._memberprops.evaluate(self._unevaluated.pop())
             for _ in range(n)])
        self._evaluations += n

    def select_parents(self):
        self._parents = self._selector.select_parents(self._evaluated,
                                                      self._popsize.parentsize)

    def select_pairs(self):
        self._parent_pairs = self._selector.select_pairs(self._parents,
                                                         self._popsize.pairsize)

    # TODO enough list size?
    def recombine(self):
        self._recombined = [
            self._mutator.recombine(pair, self._memberprops.wrapper) for pair in
            self._parent_pairs]

    def mutate(self):
        self._unevaluated = [
            self._mutator.mutate(individual, self._memberprops.wrapper) for
            individual in self._recombined]

    def select_survivors(self):
        self._evaluated = self._selector.select_survivors(
            self._evaluated,
            self._popsize.survivesize)

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
