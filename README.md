# pyga
Python implementation of Genetic Algorithm

## Installation

```shell
pip3 install pygenal
```

## Usage

```python
#!/usr/bin/env python3

# import required classes
from pygenal.ga import Population, Individual, Gene, geneTypes, Duration
import numpy as np
import time


# create population of your own, override fitness method to suit your needs.
# your system evaluation goes here, for sake of demonstration, use polynom
class Polynom(Population):
    def fitness(self, individual):
        x = individual.get("x").value
        y = individual.get("y").value
        color = individual.get("color").value

        # test against function with global maximum:
        # max{x + 3 x^2 - x^4 - y^6 + y/3 - y^3 4 - y - 5} ≈ 3.35864
        # at (x, y) ≈ (1.30084, -1.27413)
        # + favorize chocolate over shorter colors, just for demonstration
        return (x + 3*(x**2) - x**4 - y**6 + y/3.0 - (y**3)*4 - y - 5) + len(color)/10

# introduce non-number options such as color, good for selections
colors = ["brown", "green", "grey", "blue", "chocolate"]


if __name__ == '__main__':

    # spawn individual
    i1 = Individual()

    # construct "DNA"
    i1 += Gene("x", geneTypes.REAL, np.random.randint(-3, 3), min=-10, max=10)
    i1 += Gene("y", geneTypes.REAL, np.random.randint(-3, 3), min=-10, max=10)
    i1 += Gene("color", geneTypes.VALUE, np.random.choice(colors), availableOptions=colors, dominant=True)

    # create tribe with size of 100 individuals based on your first Individual
    population = Polynom(
            species=i1,
            size=100,
            chanceOfMutationStart=0.5,
            chanceOfMutationStop=0.01
        )

    tStart = time.time()

    # start evolution until:
    #   you didn't pass 1000 generations OR
    #   fittest didn't change for 200 generations OR
    #   2.5s didn't passes yet
    population.evolve(
            generations=1000,
            verbose=True,
            timeout=Duration(seconds=2, miliseconds=500),
            terminateAfter=200,
        )
    print(f"Evolved in {time.time()-tStart}s, precision: {(3.35864+len('chocolate')/10 - population.fittest.score)*100}%")
    print(f"Fittest: {population.fittest}, genes: {repr(population.fittest)}")

```
