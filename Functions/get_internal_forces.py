import numpy as np
import math

def get_internal_forces(ENL, node_list, element_list, material_properties):

    number_elements = np.size(element_list, 0)
    problem_dimension = np.size(node_list, 1)
    
    node_displacements = ENL[:, 4 * problem_dimension:5 * problem_dimension]

    node_list_end = node_list + node_displacements

    internal_forces = np.zeros(number_elements)

    # Iterating over each element
    for i in range(number_elements):
        
        E, A = material_properties[i, :]

        node_i = element_list[i, 0]
        node_j = element_list[i, 1]
        # Reference Configuration
        # Node i
        xi = node_list[node_i - 1, 0]
        yi = node_list[node_i - 1, 1]
        # Node j
        xj = node_list[node_j - 1, 0]
        yj = node_list[node_j - 1, 1]

        L = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

        # Deformed configuration
        # Node i
        x_end_i = node_list_end[node_i - 1, 0]
        y_end_i = node_list_end[node_i - 1, 1]
        # Node j
        x_end_j = node_list_end[node_j - 1, 0]
        y_end_j = node_list_end[node_j - 1, 1]

        L_end = math.sqrt((x_end_i - x_end_j) ** 2 + (y_end_i - y_end_j) ** 2)
        dL = L_end - L
        
        k = E * A / L

        internal_forces[i] = k * dL


    return internal_forces