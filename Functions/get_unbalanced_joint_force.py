import numpy as np

def get_unbalanced_joint_force(node_list, ENL, f):
    
    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)

    P = np.zeros(number_nodes * problem_dimension)

    # Iterating over each node
    for i in range(number_nodes):
        # Iterating over each nodal force
        for j in range(problem_dimension):
            dof = int(ENL[i, 3 * problem_dimension + j] - 1)
            P[dof] = ENL[i, int(5 * problem_dimension + j)]

    # Unbalanced joint force
    delta_U = P - f

    return delta_U