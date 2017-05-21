#!/bin/bash

import population as pop
import initialization as init

def main():
    popsize = pop.PopulationSize(100, 50)
    initializer = init.
    genefunc = pop.GeneFunctions()
    selectfunc = pop.SelectionFunctions()
    popmemparam = pop.MemberProperties()
    population = pop.Population(popsize, genefunc, selectfunc, popmemparam)

    pass

if __name__ == "__main__":
    # run main program
    main()
