import numpy as np
import Preprocess
import Functions
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    problem = "example-2"

    (node_list, boundary_conditions, element_list, external_loads, displacements, material_properties) = Preprocess.get_nonlinear_input_data(problem)
    
    n = 30
    incremental_loads = np.linspace(0.1, 1200000, n)
    displacement_vector = np.zeros(n)

    index = 0

    for incremental_load in incremental_loads:

        # Update external loads
        external_loads[21, 1] = incremental_load # Specific for this example

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

        # Store load and displacement
        displacement_vector[index] = ENL[21, 9]
        index += 1

print(displacement_vector)

fig, ax = plt.subplots(figsize = (8, 8))
ax.plot(displacement_vector * 100, incremental_loads / 1000, linewidth = 3)
ax.scatter(displacement_vector * 100, incremental_loads / 1000, marker = "s", linewidths = 3)
ax.set_xlabel("uy [cm]", fontsize = 15)
ax.set_ylabel("P [kN]", fontsize = 15)
plt.xlim(0, displacement_vector[-1] * 100)
plt.ylim(0, 1200)
plt.savefig("./Fig/cantilever-incremental.pdf", bbox_inches = 'tight')
plt.show()