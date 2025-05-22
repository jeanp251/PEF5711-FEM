import numpy as np
import Preprocess
import Functions
import Posprocess

if __name__ == "__main__":
    
    problem = "von-mises"
 
    (node_list, boundary_conditions, element_list, external_loads, displacements, material_properties) = Preprocess.get_nonlinear_input_data(problem)

    Preprocess.pre_process(node_list, boundary_conditions, element_list, external_loads)

    ENL = Functions.update_ENL(node_list, boundary_conditions, displacements, external_loads)

    (ENL, DOFs, DOCs) = Functions.assign_boundary_conditions(node_list, ENL)

    # Linear Approximation
    K = Functions.assemble_stiffness(ENL, element_list, node_list, material_properties)

    (F_u, U_u) = Functions.solve_system(ENL, K, external_loads, displacements, node_list, DOFs, DOCs)

    ENL = Functions.update_results_ENL(ENL, U_u, F_u, node_list)

    converged_error = 1000 # Arbitrary value
    max_iter = 50
    tolerance = 0.001
    counter = 1
    d = np.squeeze(U_u) # Removing unnecessary dimension

    while True:
        print("-" * 25)
        print(counter, "-th Iteration cycle")
        print("-" * 25)

        St, f = Functions.assemble_tangent_stiffness(ENL, element_list, node_list, material_properties)

        delta_U = Functions.get_unbalanced_joint_force(node_list, ENL, f)

        # Solving the linearized system of equations d[U] = [St] d[d]
        delta_d = Functions.solve_linearized_system(St, delta_U, DOFs)
        
        converged_error = np.linalg.norm(delta_d) / np.linalg.norm(d)
        print("e = ", converged_error)

        # Adding correction
        d += delta_d
        # Update Values
        ENL = Functions.update_displacements_ENL(ENL, d, node_list)

        if converged_error < tolerance:
            print("Converged!!!")
            break
        else:
            print("Not yet converged...")
            print("delta U:")
            print(delta_U)
            print("delta d:")
            print(delta_d)
            counter += 1

        if counter >= max_iter:
            print("Not convergerd! after ", max_iter, " iterations.")

    f, Q = Functions.get_nonlinear_results(ENL, element_list, node_list, material_properties)

    ENL = Functions.update_reactions_ENL(ENL, f[DOFs:DOFs + DOCs], node_list)

    scale_factor = 1
    Posprocess.plot_deformation_truss(ENL, node_list, element_list, scale_factor)
    Posprocess.plot_deformation_colorbar_truss(ENL, node_list, element_list, scale_factor)

    np.set_printoptions(precision = 3, suppress = True)
    print("Reactions")
    print(f[DOFs:DOFs + DOCs])
    print("Element Internal Forces")
    print(Q)
    print('Node Displacements [cm]')
    print(ENL[:, 8:10]*100)