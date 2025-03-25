import cvxpy as cp
import numpy as np


def egalitarian_division(matrix):
    # Input: matrix (n x m) where matrix[i][j] is the value agent i assigns to resource j
    n, m = matrix.shape  # n = number of agents, m = number of resources

    # Decision variables: x[i][j] = fraction of resource j allocated to agent i
    x = cp.Variable((n, m), nonneg=True)

    # Constraints:
    # 1. Each resource is fully allocated: sum(x[:, j]) == 1 for all j
    # constraints = [cast(Constraint, cp.sum(x[:, j]) == 1) for j in range(m)]
    constraints = [cp.constraints.Zero(cp.sum(x[:, j]) - 1) for j in range(m)]

    # 2. Each agent's utility is the sum of their allocations weighted by their valuations
    utilities = [cp.sum(cp.multiply(matrix[i], x[i])) for i in range(n)]

    # Combine utilities into a single vector
    utilities_vector = cp.hstack(utilities)

    # Objective: Maximize the minimum utility (egalitarian)
    objective = cp.Maximize(cp.min(utilities_vector))

    # Solve the problem
    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Print the allocation
    for i in range(n):
        allocation = [f"{x[i, j].value:.2f}" for j in range(m)]
        print(f"Agent #{i + 1} gets {', '.join([f'{allocation[j]} of resource #{j + 1}' for j in range(m)])}")


if __name__ == "__main__":
    # egalitarian_division(np.array([
    #     [50, 30, 20],
    #     [40, 40, 20],
    #     [10, 30, 60],
    # ]))

    egalitarian_division(np.array([
        [81, 19, 1],
        [70, 1, 29]],
    ))
