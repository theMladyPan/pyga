#!/usr/bin/env python3


import ga


class Localizations(ga.Population):
    def fitness(self):
        pass


if __name__ == '__main__':

    i1, i2 = [ga.Individual() for i in range(2)]

    i1 += ga.Gene("name", ga.geneTypes.VALUE, "Bob", availableOptions=["Mark", "John"], dominant=True)
    i2 += ga.Gene("name", ga.geneTypes.VALUE, "Jossie", availableOptions=["Rachel", "Lisa"])

    pop = Localizations(i1, 40)
    pop.fitness()
    pop.evolve()
