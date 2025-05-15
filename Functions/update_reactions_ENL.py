import numpy as np

def update_reactions_ENL(ENL, f, node_list):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)

    DOCs = 0 # Constrained dofs

    # Iterating over each node
    for i in range(number_nodes):
        # Iterating over each nodal force
        for j in range(problem_dimension):
            if ENL[i, problem_dimension + j] == -1:
                DOCs += 1
                ENL[i, 5 * problem_dimension + j] = f[DOCs - 1]

    return ENL