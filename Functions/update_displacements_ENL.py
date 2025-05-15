import numpy as np

def update_displacements_ENL(ENL, d, node_list):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)

    DOFs = 0 # Free dofs
    # Iterating over each node
    for i in range(number_nodes):
        for j in range(problem_dimension):
            if ENL[i, problem_dimension + j] == 1:
                DOFs += 1
                ENL[i, 4 * problem_dimension + j] = d[DOFs - 1]

    return ENL