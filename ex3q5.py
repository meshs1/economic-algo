import cvxpy as cp
import numpy as np


def compute_allocation_fixed_prices(valuations, budgets, prices):
    n, m = valuations.shape  # n agents, m resources

    x = cp.Variable((n, m), nonneg=True)

    constraints = []

    # Resource supply constraint: each resource is fully allocated
    for j in range(m):
        constraints.append(cp.sum(x[:, j]) <= 1)

    # Budget constraint per agent
    for i in range(n):
        constraints.append(cp.sum(cp.multiply(prices, x[i])) <= budgets[i])

    # Each agent maximizes their own utility: sum of v[i][j] * x[i][j]
    utilities = [cp.sum(cp.multiply(valuations[i], x[i])) for i in range(n)]

    # Lexicographic multi-objective: sum all utilities (Pareto efficiency proxy)
    objective = cp.Maximize(cp.sum(cp.hstack(utilities)))

    problem = cp.Problem(objective, constraints)
    problem.solve()

    if problem.status != cp.OPTIMAL:
        raise Exception("Optimization failed")

    x_val = x.value
    for i in range(n):
        allocation = [f"{float(x_val[i][j]):.3f}" for j in range(m)]
        xi = x_val[i].ravel()
        cost = float(np.dot(prices, xi))
        value = float(np.dot(valuations[i], xi))
        print(f"Agent {i + 1} gets {allocation}, value = {value:.3f}, price = {cost:.3f}")


def lecture_example():
    valuations = np.array([
        [8, 4, 2],  # Avi
        [2, 6, 5]  # Batya
    ])
    budgets = [60, 40]
    prices = [52.2, 26.1, 21.7]  # apple, banana, clementine
    print("Lecture example:")
    compute_allocation_fixed_prices(valuations, budgets, prices)


def extreme_skew():
    valuations = np.array([
        [100, 1, 1],  # Agent 1 wants apples only
        [5, 5, 5],  # Agent 2 values everything equally
    ])
    budgets = [50, 50]
    prices = [80, 10, 10]
    print("Extreme skew:")
    compute_allocation_fixed_prices(valuations, budgets, prices)


def perfect_symmetry():
    valuations = np.array([
        [3, 2, 1],
        [3, 2, 1]
    ])
    budgets = [100, 100]
    prices = [30, 20, 10]
    print("Perfect symmetry:")
    compute_allocation_fixed_prices(valuations, budgets, prices)


def one_dominates():
    valuations = np.array([
        [4, 4, 2],
        [4, 4, 2]
    ])
    budgets = [90, 10]
    prices = [40, 40, 20]
    print("One dominates:")
    compute_allocation_fixed_prices(valuations, budgets, prices)


def one_agent():
    value_matrix = np.array([
        [10, 3, 0],
    ])
    budgets = np.array([10])
    prices = np.array([5, 5, 5])
    print("One agent:")
    compute_allocation_fixed_prices(value_matrix, budgets, prices)


def three_agents():
    value_matrix = np.array([
        [6, 3, 7],
        [4, 4, 5],
        [9, 2, 3]
    ])
    prices = np.array([12, 8, 15])
    budgets = np.array([25, 30, 35])

    print("Three agents market")
    compute_allocation_fixed_prices(value_matrix, budgets, prices)


def equal_preferences():
    value_matrix = np.array([
        [5, 3, 4],
        [5, 3, 4]
    ])
    prices = np.array([18, 12, 22])
    budgets = np.array([25, 45])

    print("Equal preferences scenario")
    compute_allocation_fixed_prices(value_matrix, budgets, prices)



if __name__ == "__main__":
    lecture_example()
    extreme_skew()
    perfect_symmetry()
    one_dominates()
    one_agent()
    three_agents()
    equal_preferences()