import numpy as np
import matplotlib.pyplot as plt
import math

def plot_deformation_truss(ENL, node_list, scale_factor):
    
    problem_dimension = np.size(node_list, 1)

    # First we need to get a reference dimension to plot all the stuff in proportion to this
    x_min = np.min(node_list[:, 0])
    y_min = np.min(node_list[:, 1])
    x_max = np.max(node_list[:, 0])
    y_max = np.max(node_list[:, 1])

    # Proportional Dimension
    prop_dimension = math.sqrt((x_min - x_max) ** 2 + (y_min - y_max) ** 2)
    disp_scale = prop_dimension / 7.0711 * scale_factor

    # Getting the structure into from the ENL
    number_nodes = node_list.shape[0]
    node_displacements = ENL[:, 4 * problem_dimension: 5 * problem_dimension]

    node_displacement_max = np.max(node_displacements)
    node_displacements_scaled = (1 / node_displacement_max) * disp_scale * node_displacements

    node_constraints = ENL[:, problem_dimension: 2 * problem_dimension]
    node_forces = ENL[:, 5 * problem_dimension:6 * problem_dimension]

    # Nodal Coordinates
    x_ini = node_list[:, 0]
    y_ini = node_list[:, 1]

    # For visualization purposes
    # We are gonna plot the scaled deformed shape

    x_end = x_ini + node_displacements_scaled[:, 0]
    y_end = y_ini + node_displacements_scaled[:, 1]

    fig, ax = plt.subplots(figsize = (10, 10))

    # Plotting Node Displacementes
    ax.scatter(x_end, y_end, s = 50, facecolor = 'k', edgecolor = 'k', linewidths = 1, zorder = 1)
    # Plotting undeformed structure
    ax.plot(x_ini, y_ini, dashes = [4, 4], color = 'green')
    # Plotting deformed structure
    ax.plot(x_end, y_end, color = 'red')

    # Plotting Node Reactions
    for i in range(0,number_nodes):
        boundary_node_conditions = node_constraints[i, :]
        if np.any(boundary_node_conditions < 0):
            x_node = node_list[i, 0]
            y_node = node_list[i, 1]
            reactions = np.round(node_forces[i, :], decimals = 2)

            for j in range(0, problem_dimension):
                reaction = reactions[j]
                match j:
                    case 0: # Fx
                        if reaction > 0: # Positive Fx
                            ax.annotate(str(reaction) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node - 0.5, y_node + 0.05),
                                        color = 'red')
                            ax.arrow(x_node - 0.5, y_node, 0.45, 0,
                                     width = 0.04,
                                     color = 'red',
                                     length_includes_head = True)
                            
                        else:
                            ax.annotate(str(abs(reaction)) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node - 0.5, y_node + 0.05),
                                        color = 'red')
                            ax.arrow(x_node - 0.05, y_node, -0.45, 0,
                                     width = 0.04,
                                     color = 'red',
                                     length_includes_head = True)
                    case 1: # Fy
                        if reaction > 0: # Positive Fy
                            ax.annotate(str(reaction) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 0.005, y_node - 0.5),
                                        color = 'red')
                            ax.arrow(x_node, y_node - 0.5, 0, 0.45,
                                     width = 0.04,
                                     color = 'red',
                                     length_includes_head = True)
                        else:
                            ax.annotate(str(abs(reaction)) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 0.05, y_node - 0.5),
                                        color = 'red')
                            ax.arrow(x_node, y_node - 0.05, 0, -0.45,
                                     width = 0.04,
                                     color = 'red',
                                     length_includes_head = True)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    fig_save_name = "./Fig/deformation.pdf"
    plt.savefig(fig_save_name, bbox_inches = "tight")
    plt.show()