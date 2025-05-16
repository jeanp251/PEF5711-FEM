import numpy as np
import math

def assemble_tangent_stiffness(ENL, element_list, node_list, material_properties):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    number_elements = np.size(element_list, 0)
    nodes_per_elemet = np.size(element_list, 1)

    St = np.zeros([number_nodes * problem_dimension, number_nodes * problem_dimension])
    f = np.zeros(number_nodes * problem_dimension)

    # Iterating over each element
    for i in range(0, number_elements):
        E, A = material_properties[i, :]
        nodes = element_list[i, 0:problem_dimension]
        kt_contribution, F_contribution = __element_tangent_stiffness(nodes, ENL, E, A, problem_dimension)
        
        for j in range(0, nodes_per_elemet):
            for k in range(0, problem_dimension):
                for l in range(0, nodes_per_elemet):
                    for m in range(0, problem_dimension):
                        row = ENL[nodes[j] - 1, k + 3 * problem_dimension]
                        column = ENL[nodes[l] - 1, m + 3 * problem_dimension]
                        value = kt_contribution[j * problem_dimension + k, l * problem_dimension + m]
                        St[int(row) - 1, int(column) - 1] = St[int(row) - 1, int(column) - 1] + value
        
        # Iterating over each element's node:
        for j in range(0, nodes_per_elemet):
            global_dofs = ENL[nodes[j] - 1, 3 * problem_dimension:4 * problem_dimension]
            # Iterating over each dof's force
            for k in range(problem_dimension):
                dof = int(global_dofs[k]) - 1 # For 0-index
                f[dof] += F_contribution[2 * j + k]

    return St, f


def __element_tangent_stiffness(nodes, ENL, E, A, problem_dimension):

    # Reference Configuration
    # NODE i
    xri = ENL[nodes[0] - 1, 0]
    yri = ENL[nodes[0] - 1, 1]

    # NODE j
    xrj = ENL[nodes[1] - 1, 0]
    yrj = ENL[nodes[1] - 1, 1]

    L = math.sqrt((xrj - xri) ** 2 + (yrj - yri) ** 2)

    # Deformed Configuration
    # NODE i
    xi = xri + ENL[nodes[0] - 1, 4 * problem_dimension]
    yi = yri + ENL[nodes[0] - 1, 4 * problem_dimension + 1]

    # NODE j
    xj = xrj + ENL[nodes[1] - 1, 4 * problem_dimension]
    yj = yrj + ENL[nodes[1] - 1, 4 * problem_dimension + 1]

    Ld = math.sqrt((xj - xi) ** 2 + (yj - yi) ** 2)

    u = Ld - L

    Q = (E * A / L) * u

    cx = (xj - xi) / Ld
    cy = (yj - yi) / Ld
    
    k = (E * A) / L * np.array([[cx ** 2, cx * cy, -cx ** 2, -cx * cy],
                                [cx * cy, cy ** 2, -cx * cy, -cy ** 2],
                                [-cx ** 2, -cx * cy, cx ** 2, cx * cy],
                                [-cx * cy, -cy ** 2, cx * cy, cy ** 2]])
    
    g = (1 / Ld) * np.array([[-cy ** 2, cx * cy, cy ** 2, -cx * cy],
                             [cx * cy, -cx ** 2, -cx * cy, cx ** 2],
                             [cy ** 2, -cx * cy, -cy ** 2, cx * cy],
                             [-cx * cy, cx ** 2, cx * cy, -cx ** 2]])
    kt = k - Q  * g

    # Element Global Force Vector
    T = np.array([-cx, -cy, cx, cy])

    F = T * Q
    return kt, F