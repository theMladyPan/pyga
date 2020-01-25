#!/usr/bin/env python3


import ga
import numpy as np
from timeit import timeit
import time


class Localizations(ga.Population):
    def fitness(self):
        pass


colors = ["brown", "green", "grey", "blue", "chocolate"]


if __name__ == '__main__':

    i1, i2 = [ga.Individual() for i in range(2)]

    i1 += ga.Gene("eye_color", ga.geneTypes.VALUE, np.random.choice(colors), availableOptions=colors, dominant=True)
    i1 += ga.Gene("height", ga.geneTypes.NATURAL, np.random.randint(100, 200), min=1, max=300)

    pop = ga.Population(i1, 100)
    print(pop)
    tStart = time.time()
    pop.evolve(iterations=1000)
    print(pop)
    print(time.time()-tStart)


    # print(timeit(stmt='pop = ga.Population(ga.Individual({"name":ga.Gene("name", ga.geneTypes.VALUE, "Bob", availableOptions=["Mark", "John", "BoB"], dominant=True)}), 100)', setup="import ga", number=1000)*1000, "us per population of 100 seed")
    # print(timeit(stmt='i.mutate(.3)', setup='import ga;i=ga.Individual({"name":ga.Gene("name", ga.geneTypes.VALUE, "Bob", availableOptions=["Mark", "John", "BoB"], dominant=True)})', number=1000)*1000, "us per mutation")
