import numpy as np
import Preprocess
import Functions
import Posprocess

if __name__ == "__main__":

    # INPUT DATA
    # problem = "example-1"

    E = 10**6 # MPa
    A = 0.01 # m^2

    node_list = np.array([[0, 0], 
                        [1, 0],
                        [0.5, 1]])

    element_list = np.array([[1, 2], 
                            [2, 3], 
                            [3, 1]])
    
    # -1: Fixed
    # +1: Free
    boundary_conditions = np.array([[-1, -1],
                                    [1, -1],
                                    [1, 1]])

    external_loads = np.array([[0, 0], 
                            [0, 0], 
                            [0, -20.0]])

    displacements = np.array([[0, 0], 
                            [0, 0],
                            [0, 0]])

    Preprocess.pre_process(node_list, boundary_conditions, element_list, external_loads)
    
    # Extended Node List [ENL]

    ENL = Functions.update_ENL(node_list, boundary_conditions, displacements, external_loads)

    (ENL, DOFs, DOCs) = Functions.assign_boundary_conditions(node_list, ENL)

    K = Functions.assemble_stiffness(ENL, element_list, node_list, E, A)

    (F_u, U_u) = Functions.solve_system(ENL, K, external_loads, displacements, node_list, DOFs, DOCs)

    ENL = Functions.update_results_ENL(ENL, U_u, F_u, node_list)

    np.set_printoptions(precision = 3, suppress = True)
    print(ENL)
    print(U_u)
    print(F_u)
    print(ENL[:, 8:10])

    scale_factor = 1
    Posprocess.pos_process.plot_deformation_truss(ENL, node_list, scale_factor)