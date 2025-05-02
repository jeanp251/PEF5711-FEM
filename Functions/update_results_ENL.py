import numpy as np

def update_results_ENL(ENL, U_u, F_u, node_list):
    
    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)

    DOFs = 0 # Free dofs
    DOCs = 0 # Constrained dofs

    for i in range(0, number_nodes):
        for j in range(0, problem_dimension):
            if ENL[i, problem_dimension + j] == 1:
                DOFs += 1
                ENL[i, 4 * problem_dimension + j] = U_u[DOFs - 1]
            else:
                DOCs += 1
                ENL[i, 5 * problem_dimension + j] = F_u[DOCs - 1]
    
    return ENL