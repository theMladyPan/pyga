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
    def __init__(self, uname: str, type: geneTypes, value: object, *, dominant: bool = False, rateOfMutation: float = 1, availableOptions: list, max: object = math.inf, min: object = -math.inf):
        super().__init__()
        self.uname = uname
        self.type = type
        self.dominant = bool(dominant)
        self.rate = rateOfMutation
        self.value = value
        if type == geneTypes.VALUE:
            self.options = availableOptions
        else:
            self.min = min
            self.max = max

    def mutate(self, chance: float = 0):
        if self.type == geneTypes.VALUE:
            chance = chance*self.rate

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
            return f"Gene(uname={self.uname}, type={self.type}, value={self.value}, dominant={self.dominant}, rateOfMutation={self.rate}, availableOptions={self.options})"
        else:
            return f"Gene(uname={self.uname}, type={self.type}, value={self.value}, dominant={self.dominant}, rateOfMutation={self.rate}, min={self.min}, max={self.max})"


class Individual(dict):
    def __init__(self, genome={}):
        super().__init__(genome)

    def __iadd__(self, gene):
        self[gene.uname] = gene
        return self

    def appendGene(self, gene):
        self.__iadd__(gene)

    def __matmul__(self, individual):
        """Perform uniform crossover with other individual"""
        offspring = Individual()
        for key in self.keys():
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

    def mutate(self):
        return Individual(self)

    def copy(self):
        return Individual(copy.deepcopy(self))


class Population(list):
    def __init__(self, individual: Individual, size: int):
        self.species = individual
        super().__init__([individual.mutate() for i in range(size)])

    def evolve(self, *, timeout: float = 0, iterations: int = 1):
        if timeout:
            startTime = time.time()
        for i in range(iterations):
            pass
            # TODO:

    def fitness(self):
        """Override this function with your fitness function"""
        raise NotImplementedError("You must override fitness method in order to evolve")
