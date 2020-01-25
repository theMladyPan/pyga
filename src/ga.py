#!/usr/bin/env python3

import time
import math
import numpy as np
import copy

from enum import Enum


__all__ = [
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
            diff = self.max - self.min
            delta = diff * ((2 * random) - 1)
            self.value += delta
            if self.value < self.min:
                self.value = self.min
            elif self.value > self.max:
                self.value = self.max
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
            return f"Gene(uname={self.uname}, type={self.type}, value='{self.value}', dominant={self.dominant}, rateOfMutation={self.rate}, availableOptions={self.options})"
        else:
            return f"Gene(uname={self.uname}, type={self.type}, value={self.value}, dominant={self.dominant}, rateOfMutation={self.rate}, min={self.min}, max={self.max})"


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

    def mutate(self, chance: float) -> Individual:
        mutated = self.copy()
        for key in self.keys():
            if not key.startswith("__"):
                self[key].mutate(chance)

        return mutated

    def copy(self):
        return Individual(copy.deepcopy(self))


class Population(list):
    def __init__(self, individual: Individual, size: int, chanceOfMutation: float = 0.1):
        self.species = individual
        self.chanceOfMutation = chanceOfMutation
        super().__init__([self.species.mutate(chanceOfMutation) for i in range(size)])

    def evolve(self, *, timeout: float = 0, iterations: int = 1):
        # TODO: Timeout
        for i in range(iterations):
            for individual in self:
                # evaluate each individual according to fitness function
                individual["__score__"] = self.fitness(individual)

            # sort population according to fitness score
            self.sort(key=lambda individual: individual["__score__"])
            # remove tail of population
            del self[:int(len(self)/2)]
            for i in range(0, len(self), 2):
                # crossover those motherfuckers
                self.append(self[i]@self[i+1])
                self.append(self[i]@self[i+1])
            for individual in self:
                individual.mutate(self.chanceOfMutation)

    def fitness(self, individual):
        """Override this function with your fitness function"""
        return len(individual.get("eye_color").value) + individual.get("height").value
        # raise NotImplementedError("You must override fitness method in order to evolve")

    def __str__(self):
        return str([(i.get("eye_color").value, i.get("height").value) for i in self])
