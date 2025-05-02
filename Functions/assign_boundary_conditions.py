import numpy as np

def assign_boundary_conditions(node_list, ENL):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)

    DOFs = 0 # Free DOF
    DOCs = 0 # Restrained DOF

    for i in range(0, number_nodes):

        for j in range(0, problem_dimension):

            if ENL[i, problem_dimension + j] == -1:

                DOCs -= 1
                ENL[i, 2 * problem_dimension + j] = DOCs
            
            else:

                DOFs += 1
                ENL[i, 2 * problem_dimension + j] = DOFs

    for i in range(0, number_nodes):

        for j in range(0, problem_dimension):

            if ENL[i, 2 * problem_dimension + j] < 0:
                
                ENL[i, 3 * problem_dimension + j] = abs(ENL[i, 2 + problem_dimension + j]) + DOFs

            else:

                ENL[i, 3 * problem_dimension + j] = abs(ENL[i, 2 + problem_dimension + j])

    DOCs = abs(DOCs)

    return (ENL, DOFs, DOCs)