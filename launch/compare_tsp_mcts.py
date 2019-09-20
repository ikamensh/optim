from problems import TspProblem
from algorithms.document import PlotProgress
from algorithms import RandomSearch
from algorithms import GeneticAlgorithm
from algorithms.specific.genetic_algorithm_mcts import GeneticAlgorithmMcts
from algorithms.solver import Solver
from concurrent import futures


def solve_n_times(solver: Solver, n: int, n_steps: int):
    metrics = []

    for i in range(n):
        solver.reset()
        m = solver.solve(n_steps)
        print(solver, i)
        metrics.append(m)

    return sum(metrics)


problem = TspProblem.random_problem(n_dim=5, cities=200)

# for popsize in [10, 50]:
popsize = 30
docu = PlotProgress(problem)

style = {}
style['dashes'] = [1, 3, 7, 13, 7, 3, 1]
solvers = [ GeneticAlgorithmMcts(problem, popsize, plot_kwargs=style) ]

solvers.append(RandomSearch(problem))
for elite_size, color in zip({1, popsize//10}, ['purple', 'teal', 'brown']):
    for mr, linewidth in zip([5e-4, 5e-3, 0.01], [0.5, 1.1, 1.8]):
        for heavy in [True, False]:
            style = {}
            if heavy:
                style['dashes'] = [2, 2, 10, 2]
            style['linewidth'] = linewidth
            style['color'] = color
            ga = GeneticAlgorithm(problem, popsize, mr, elite_size, heavy_tail_mutation=heavy,
                                  plot_kwargs=style)
            solvers.append(ga)


best_score_metrics = {}

n_steps = int(1e6)
n_trials = 5

pool = futures.ProcessPoolExecutor()


def maping(solver):
    try:
        return solve_n_times(solver, n=n_trials, n_steps=n_steps)
    except Exception as e:
        print(e,'In mapping')
        return None

if __name__ == "__main__":
    metrics = pool.map(maping, solvers)

    for solver, result in zip(solvers, metrics):
        if result:
            best_score_metrics[str(solver)] = result

    # for solver in solvers:
    #     best_score_metrics[str(solver)] = solve_n_times(solver, n = n_trials, n_steps=n_steps)

    docu.generate_report(best_score_metrics)
