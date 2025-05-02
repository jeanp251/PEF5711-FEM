import numpy as np

def solve_system(ENL, K, external_loads, displacements, node_list, DOFs, DOCs):

    displacements = displacements.flatten()

    external_loads = external_loads.flatten()

    Fp = assemble_forces(ENL, node_list)
    Up = assemble_displacements(ENL, node_list)

    K_UU = K[0:DOFs, 0:DOFs]
    K_UP = K[0:DOFs, DOFs:DOFs + DOCs]
    K_PU = K[DOFs:DOFs + DOCs, 0:DOFs]
    K_PP = K[DOFs:DOFs + DOCs, DOFs:DOFs + DOCs]

    F = Fp - np.matmul(K_UP, Up)
    U_u = np.linalg.solve(K_UU, F)
    
    F_u = np.matmul(K_PU, U_u) + np.matmul(K_PP, Up)

    return (F_u, U_u)

def assemble_forces(ENL, node_list):
    # Estblishing the prescribed forces
    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    DoF = 0

    Fp = []

    for i in range(0, number_nodes):
        for j in range(0, problem_dimension):
            if ENL[i, problem_dimension + j] == 1:
                DoF += 1
                Fp.append(ENL[i, 5 * problem_dimension + j])

    Fp = np.vstack([Fp]).reshape(-1, 1)

    return Fp

def assemble_displacements(ENL, node_list):
    # Establishing the prescribed displacements

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    DoC = 0

    Up = []

    for i in range(0, number_nodes):
        for j in range(0, problem_dimension):
            if ENL[i, problem_dimension + j] == -1:
                DoC += 1
                Up.append(ENL[i, 4 * problem_dimension + j])

    Up = np.vstack([Up]).reshape(-1, 1)

    return Up