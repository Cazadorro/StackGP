#!/bin/bash
from operator import attrgetter, itemgetter


class StackGPPopulation:
    def __init__(self, gp_mu, gp_lambda, gp_operators, init_f, recombine_f, mutate_f, parent_f, survival_f):
        self.gp_mu = gp_mu
        self.gp_lambda = gp_lambda
        self.gp_saved = self.gp_mu - self.gp_lambda if self.gp_mu >= self.gp_lambda else 0
        self.gp_operators = gp_operators

        self.init_method = init_f
        self.recombine_method = recombine_f
        self.mutate_method = mutate_f
        self.parent_selection = parent_f
        self.survival_selection = survival_f

        self.un_evaluated = []
        self.evaluated = []
        self.n_members_loaned = 0
        self.n_members_evaluated = 0
        self.n_generations = 0

        self.initialize_population()

    def initialize_population(self):
        self.un_evaluated = self.init_method(self.gp_mu, self.gp_operators)

    def loan_unevaluated(self, num_loaned=None):
        if num_loaned is None:
            num_loaned = len(self.un_evaluated)
        self.n_members_loaned += num_loaned
        return [self.un_evaluated.pop() for _ in range(num_loaned)]

    def return_unevaluated(self, returned):
        self.evaluated.extend(returned)
        self.n_members_evaluated += len(returned)
        self.n_members_loaned -= len(returned)

    def gen_children(self):
        parents1, parents2 = self.parent_selection(self.evaluated, self.gp_lambda)
        children = []
        for child_i in range(self.gp_lambda):
            recombined = self.recombine_method(parents1[child_i], parents2[child_i])
            mutated = self.mutate_method(recombined, self.gp_operators)
            children.append(mutated)
        self.un_evaluated.extend(children)

    def cull_parents(self):
        self.evaluated = self.survival_selection(self.evaluated, self.gp_saved)

    def get_best(self):
        max(self.evaluated, key=attrgetter('fitness'))

    def progress_generation(self):

        if self.n_members_evaluated >= self.gp_mu:
            if (self.n_members_evaluated - self.gp_mu) % self.gp_lambda == 0:
                self.n_generations += 1
                self.gen_children()
                self.cull_parents()
                print("New Generation: ", self.n_generations)
                print("\tNumber of members evaluated: ", self.n_members_evaluated)
                print('')
