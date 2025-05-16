import numpy as np
import math

def get_nonlinear_results(ENL, element_list, node_list, material_properties):

    # Get final reaction configuration after the Newton-Raphson method

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    number_elements = np.size(element_list, 0)
    nodes_per_elemet = np.size(element_list, 1)

    f = np.zeros(number_nodes * problem_dimension)
    Q = np.zeros(number_elements)

    # Iterating over each element
    for i in range(0, number_elements):
        E, A = material_properties[i, :]
        nodes = element_list[i, :]
        F_contribution, Q[i] = __element_nonlinear_force(nodes, ENL, E, A, problem_dimension)

        # Iterating over each element's node:
        for j in range(nodes_per_elemet):
            global_dofs = ENL[nodes[j] - 1, 3 * problem_dimension:4 * problem_dimension]
            # Iterating over each dof's force
            for k in range(problem_dimension):
                dof = int(global_dofs[k]) - 1 # For 0-index
                f[dof] += F_contribution[2 * j + k]

    return f, Q

def __element_nonlinear_force(nodes, ENL, E, A, problem_dimension):

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

    # Element Global Force Vector
    T = np.array([-cx, -cy, cx, cy])

    F = T * Q

    return F, Q