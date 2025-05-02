import numpy as np
import math

def assemble_stiffness(ENL, element_list, node_list, E, A):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    number_elements = np.size(element_list, 0)
    nodes_per_elemet = np.size(element_list, 1)

    K = np.zeros([number_nodes * problem_dimension, number_nodes * problem_dimension])

    for i in range(0, number_elements):

        nodes = element_list[i, 0:problem_dimension]
        k_contribution = __element_stiffness(nodes, ENL, E, A)
        
        for j in range(0, nodes_per_elemet):
            for k in range(0, problem_dimension):
                for l in range(0, nodes_per_elemet):
                    for m in range(0, problem_dimension):
                        row = ENL[nodes[j] - 1, k + 3 * problem_dimension]
                        column = ENL[nodes[l] - 1, m + 3 * problem_dimension]
                        value = k_contribution[j * problem_dimension + k, l * problem_dimension + m]
                        K[int(row) - 1, int(column) - 1] = K[int(row) - 1, int(column) - 1] + value

    return K


def __element_stiffness(nodes, ENL, E, A):

    # NODE i
    xi = ENL[nodes[0] - 1, 0]
    yi = ENL[nodes[0] - 1, 1]

    # NODE j
    xj = ENL[nodes[1] - 1, 0]
    yj = ENL[nodes[1] - 1, 1]

    L = math.sqrt((xj - xi) ** 2 + (yj - yi) ** 2)
    c = (xj - xi) / L
    s = (yj - yi) / L
    
    k = (E * A / L) * np.array([[c ** 2, c * s, - c ** 2, - c * s], 
                                [c * s, s ** 2, - c * s, - s ** 2],
                                [- c ** 2, - c * s, c ** 2, c * s],
                                [- c * s, - s ** 2, c * s, s ** 2]])
    
    return k