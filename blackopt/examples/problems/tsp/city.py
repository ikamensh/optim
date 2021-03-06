import numpy as np
from functools import lru_cache

np.random.seed(1)


class City:

    n_cities = 0

    def __init__(self, ndim):
        self.uid = City.n_cities
        City.n_cities += 1
        self.coordinates = np.random.random(size=[ndim])

    @lru_cache(maxsize=int(2**20))
    def distance(self, city: 'City'):
        return np.linalg.norm(self.coordinates - city.coordinates)

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return self.uid

    def __repr__(self):
        return f"City {self.uid}"
