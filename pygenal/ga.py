#!/usr/bin/env python3

import time
import math
import numpy as np
import copy
import random

from enum import Enum


__all__ = [
    "Duration",
    "CustomException",
    "geneTypes",
    "dummy",
    "Gene",
    "Individual",
    "Population",
    ]

__author__ = "Stanislav Rubint"
__year__ = 2020
__doc__ = """"""
__version__ = "1.0.4"


class Duration:
    def __init__(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, miliseconds: int = 0):
        self._seconds = days*24*3600 + hours*3600 + minutes*60 + seconds + miliseconds/1000.0

    @property
    def miliseconds(self):
        return self._seconds*1000

    @property
    def seconds(self):
        return self._seconds

    @property
    def minutes(self):
        return self._seconds/60.0

    @property
    def hours(self):
        return self.minutes/60.0

    @property
    def days(self):
        return self.hours/24.0

    def __float__(self):
        return self._seconds


class geneTypes(Enum):
    VALUE = 1
    NATURAL = 2
    INTEGER = 3
    REAL = 4


def dummy(**kwargs):
    return 0


class CustomException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class Gene:
    """Declaration"""
    pass


class Gene:
    def __init__(self, uname: str, type: geneTypes, value: object, *, dominant: bool = False, rateOfMutation: float = 1, availableOptions: list = [], max: object = math.inf, min: object = -math.inf):
        super().__init__()
        self.uname = uname
        self.type = type
        self.dominant = bool(dominant)
        self.rate = rateOfMutation
        self.value = value
        if type == geneTypes.VALUE:
            self.options = availableOptions
        elif type == geneTypes.NATURAL:
            self.min = 0
            self.max = max
        else:
            self.min = min
            self.max = max

    def mutate(self, chance: float) -> Gene:
        chance = chance*self.rate
        random = np.random.random()
        if self.type == geneTypes.VALUE:
            if chance >= random:
                self.value = np.random.choice(self.options)
        else:
            # determine span for mutation
            diff = self.max - self.min
            # calculate something in 10% radii of current value
            delta = diff * ((2 * random) - 1) * chance
            # mutate a bit
            self.value += delta
            # pay attention to limits
            if self.value < self.min:
                self.value -= delta*2
            elif self.value > self.max:
                self.value -= delta*2
            if self.type == geneTypes.INTEGER:
                self.value = int(self.value)
        return self

    def __gt__(self, gene: Gene):
        "Return True if dominant over gene"
        if self.dominant and not gene.dominant:
            return True
        return False

    def __lt__(self, gene: Gene):
        "Return True if recessive over gene"
        if not self.dominant and gene.dominant:
            return True
        return False

    def __eq__(self, gene: Gene):
        "Return True if genes are equally dominant"
        return self.dominant == gene.dominant

    def copy(self) -> Gene:
        return copy.deepcopy(self)

    def __repr__(self):
        if self.type == geneTypes.VALUE:
            return f"Gene(uname='{self.uname}', type={self.type}, value='{self.value}', dominant={self.dominant}, rateOfMutation={self.rate}, availableOptions={self.options})"
        else:
            return f"Gene(uname='{self.uname}', type={self.type}, value={self.value}, dominant={self.dominant}, rateOfMutation={self.rate}, min={self.min}, max={self.max})"


class Individual:
    """Declaration"""
    pass


class Individual(dict):
    def __init__(self, genome={}):
        super().__init__(genome)
        self["__score__"] = 0

    def __iadd__(self, gene):
        self[gene.uname] = gene
        return self

    def appendGene(self, gene):
        self.__iadd__(gene)

    @property
    def genes(self):
        return [value for (key, value) in self.items() if not key.startswith("__")]

    @property
    def score(self):
        return self.get("__score__")

    def __matmul__(self, individual):
        """Perform uniform crossover with other individual"""
        offspring = Individual()
        for key in self.keys():
            if not key.startswith("__"):
                gA = self.get(key)
                gB = individual.get(key)
                if gA == gB:
                    offspring[key] = np.random.choice([gA, gB]).copy()
                elif gA > gB:
                    offspring[key] = gA.copy()
                else:
                    offspring[key] = gB.copy()

        return offspring

    def crossover(self, individual):
        self.__matmul__(individual)

    def __repr__(self):
        sRep = {key: value for (key, value) in self.items()}
        return f"Individual(genome={sRep})"

    def __str__(self):
        return f"Score: {self['__score__']}"

    def mutate(self, chance: float) -> Individual:
        mutated = self.copy()
        for key in mutated.keys():
            if not key.startswith("__"):
                mutated[key].mutate(chance)

        return mutated

    def copy(self):
        return Individual(copy.deepcopy(self))


class Population(list):
    def __init__(self, species: Individual, size: int, *, chanceOfMutationStart: float = 0.1, chanceOfMutationStop: float = 0.01, randomSeed: bool = True):
        self.species = species
        self.mutRateStart = chanceOfMutationStart
        self.mutRateStop = chanceOfMutationStop
        if randomSeed:
            super().__init__([self.species.mutate(chanceOfMutationStart) for i in range(size)])
        else:
            super().__init__([self.species.mutate(chanceOfMutationStart) for i in range(size)])
        self.test()
        self.order()
        print([i.score for i in self])

    def test(self):
        for individual in self:
            # evaluate each individual according to fitness function
            individual["__score__"] = self.fitness(individual)

    def evolve(
            self,
            *,
            allowCrossover: bool = True,
            timeout: float = 0,
            generations: int = 0,
            verbose: bool = False,
            terminatingChange: float = 0,
            terminateAfter: int = 0):

        # TODO: Timeout
        chanceOfMutation = self.mutRateStart

        if not generations:
            generations = math.inf
            decCoeff = (self.mutRateStart / self.mutRateStop) ** 0.1
        else:
            decCoeff = (self.mutRateStart / self.mutRateStop) ** (1.0/generations)
        generationsWithoutImprovement = 0
        if timeout:
            startTime = time.time()

        j = 0
        while j < generations:
            lastFittest = self[-1]
            lenOfPop = len(self)
            # remove tail of population
            del self[:int(lenOfPop/2)]

            for i in range(0, int(lenOfPop/2), 2):
                if allowCrossover:
                    # crossover those motherfuckers an mutate
                    offspring = (self[i]@self[i+1]).mutate(chanceOfMutation)
                    self.append(offspring)
                    # mutate few of survivors
                    self.append(random.choice(self).mutate(chanceOfMutation))
                else:
                    # mutate few of survivors
                    self.append(random.choice(self).mutate(chanceOfMutation))
                    self.append(random.choice(self).mutate(chanceOfMutation))
            chanceOfMutation /= decCoeff
            self.test()
            self.order()

            improvement = self[-1].score - lastFittest.score
            if improvement <= terminatingChange:
                generationsWithoutImprovement += 1
            else:
                generationsWithoutImprovement = 0

            if terminateAfter and generationsWithoutImprovement >= terminateAfter:
                break
            if time.time()-startTime > float(timeout):
                break

            if verbose:
                print(f"Top score in generation {j} is {self[-1].score}")

            j += 1

    def order(self):
        # sort population according to fitness score
        self.sort(key=lambda individual: individual["__score__"])

    def fitness(self, individual):
        """Override this function with your fitness function"""
        raise NotImplementedError("You must override fitness method in order to evolve")

    def __str__(self):
        return str([(i.get("eye_color").value, i.get("height").value) for i in self])

    @property
    def fittest(self):
        return self[-1]
