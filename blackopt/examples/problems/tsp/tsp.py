from __future__ import annotations
from typing import List
import random
import math

from blackopt.abc import Problem, Solution
from blackopt.examples.problems.tsp.city import City


class TspProblem(Problem):
    name = "Tsp"

    def __init__(self, cities: List[City]):
        self.cities = cities
        self.n_dim = len(cities[0].coordinates)
        self.eval_count = 0
        self.max_dist = len(self.cities) * math.sqrt(self.n_dim)

    @staticmethod
    def random_problem(n_dim: int, cities: int):
        cities = [City(n_dim) for _ in range(cities)]
        return TspProblem(cities)

    def evaluate(self, s: TspSolution):
        self.eval_count += 1
        return self.max_dist - self.route_distance(s.route)

    @staticmethod
    def route_distance(route: List[City]):
        pathDistance = 0
        path = route + [route[0]]
        for i in range(0, len(path) - 1):
            pathDistance += path[i].distance(path[i + 1])
        return pathDistance

    def __str__(self):
        return f"Tsp {len(self.cities)} cities & {self.n_dim} dim"


class TspSolution(Solution):
    def __init__(self, route: List[City]):
        self.route = route
        assert set(route) == set(self.problem.cities)

    @staticmethod
    def random_solution() -> TspSolution:
        cpy = list(TspSolution.problem.cities)
        random.shuffle(cpy)
        return TspSolution(cpy)

    def mutate(self, mutationRate: float) -> TspSolution:
        route = list(self.route)

        for i in range(len(route)):
            if random.random() < mutationRate:
                j = int(random.random() * len(route))
                route[i], route[j] = route[j], route[i]

        return TspSolution(route)

    def crossover(self, other: TspSolution):
        crossover_point = random.randint(1, len(self.route) - 1)

        child_left = self.route[:crossover_point]
        check = {city.uid for city in child_left}
        child_right = [city for city in other.route if city.uid not in check]

        return [TspSolution(child_left + child_right)]
