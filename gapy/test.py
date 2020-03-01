#!/usr/bin/env python3


import ga
import numpy as np
from timeit import timeit
import time


class Polynom(ga.Population):
    def fitness(self, individual):
        x = individual.get("x").value
        y = individual.get("y").value
        #  -x^4 +3*x^2 + x
        return x + 3*(x**2) - x**4 - y**6 + y/3.0 - (y**2)*4


colors = ["brown", "green", "grey", "blue", "chocolate"]


if __name__ == '__main__':

    i1, i2 = [ga.Individual() for i in range(2)]

    # i1 += ga.Gene("eye_color", ga.geneTypes.VALUE, np.random.choice(colors), availableOptions=colors, dominant=True)
    i1 += ga.Gene("x", ga.geneTypes.REAL, np.random.randint(-2, 2), min=-10, max=10)
    i1 += ga.Gene("y", ga.geneTypes.REAL, np.random.randint(-2, 2), min=-10, max=10)

    pop = Polynom(species=i1, size=100, chanceOfMutationStart=0.5, chanceOfMutationStop=0.001)

    tStart = time.time()
    pop.evolve(generations=100, verbose=True, terminateAfter=100, maxTime = 1)
    print(f"Evolved in {time.time()-tStart}s")
    print(repr(pop[-1]))

    #  print(timeit(stmt='pop = ga.Population(ga.Individual({"name":ga.Gene("name", ga.geneTypes.VALUE, "Bob", availableOptions=["Mark", "John", "BoB"], dominant=True)}), 100)', setup="import ga", number=1000)*1000, "us per population of 100 seed")
    #  print(timeit(stmt='i.mutate(.3)', setup='import ga;i=ga.Individual({"name":ga.Gene("name", ga.geneTypes.VALUE, "Bob", availableOptions=["Mark", "John", "BoB"], dominant=True)})', number=1000)*1000, "us per mutation")
