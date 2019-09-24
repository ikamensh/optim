from blackbox.algorithms import HillClimber, GeneticAlgorithm
from examples.problems import StepProblem, StepSolution
from blackbox.algorithms import RandomSearch
from blackbox.util.document import generate_report

from blackbox.compare import compare_solvers, SolverFactory


problems = [StepProblem.random_problem(n) for n in [250, 1000, 3000]]

sfs = []

n_steps = 50_000
trials = 10

for problem in problems:
    sfs += [SolverFactory(GeneticAlgorithm, problem, StepSolution, p, 1/problem.n_dim, e) for p in [10, 30] for e in [0, 1]]
    sfs += [SolverFactory(HillClimber,problem, StepSolution, mutation_rate=2/problem.n_dim)]
    # sfs.append(SolverFactory(RandomSearch, problem, StepSolution))

    ms = compare_solvers(trials, n_steps, sfs)
    generate_report(problem, ms)
