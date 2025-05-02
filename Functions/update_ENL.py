import numpy as np

def update_ENL(node_list, boundary_conditions, displacements, external_loads):

    problem_dimension = np.size(node_list, 1)

    number_nodes = np.size(node_list, 0)

    ENL = np.zeros([number_nodes, 6 * problem_dimension])

    ENL[:, 0:problem_dimension] = node_list

    ENL[:, problem_dimension:2 * problem_dimension] = boundary_conditions

    ENL[:, 4 * problem_dimension : 5 * problem_dimension] = displacements[:, :]

    ENL[:, 5 * problem_dimension : 6 * problem_dimension] = external_loads[:, :]

    return ENL