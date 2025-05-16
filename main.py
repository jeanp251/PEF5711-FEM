import Preprocess
import Functions
import Posprocess
import numpy as np

if __name__ == "__main__":

    # INPUT DATA
    problem = "example-3"

    (node_list, boundary_conditions, element_list, external_loads, displacements, material_properties) = Preprocess.get_input_data(problem)

    Preprocess.pre_process(node_list, boundary_conditions, element_list, external_loads)
    
    # Extended Node List [ENL]

    ENL = Functions.update_ENL(node_list, boundary_conditions, displacements, external_loads)

    (ENL, DOFs, DOCs) = Functions.assign_boundary_conditions(node_list, ENL)

    K = Functions.assemble_stiffness(ENL, element_list, node_list, material_properties)

    (F_u, U_u) = Functions.solve_system(ENL, K, external_loads, displacements, node_list, DOFs, DOCs)

    ENL = Functions.update_results_ENL(ENL, U_u, F_u, node_list)

    internal_forces = Functions.get_internal_forces(ENL, node_list, element_list, material_properties)

    np.set_printoptions(precision = 3, suppress = True)
    print("Internal Forces")
    print(internal_forces)
    
    scale_factor = 100
    Posprocess.plot_deformation_truss(ENL, node_list, element_list, scale_factor)
    Posprocess.plot_deformation_colorbar_truss(ENL, node_list, element_list, scale_factor)