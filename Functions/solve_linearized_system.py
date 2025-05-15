import numpy as np

def solve_linearized_system(St, delta_U, DOFs):
    # Solve the linearized system
    # d[U] = [St] d[d]
    delta_d = np.linalg.solve(St[0:DOFs, 0:DOFs], delta_U[0:DOFs])

    return delta_d