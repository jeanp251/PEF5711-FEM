import numpy as np
import matplotlib.pyplot as plt
import math

def plot_deformation_truss(ENL, node_list, element_list, scale_factor):
    
    problem_dimension = np.size(node_list, 1)
    number_elements = np.size(element_list, 0)

    label_fontsize = 15
    annotate_fontsize = 12

    # First we need to get a reference dimension to plot all the stuff in proportion to this
    x_min = np.min(node_list[:, 0])
    y_min = np.min(node_list[:, 1])
    x_max = np.max(node_list[:, 0])
    y_max = np.max(node_list[:, 1])

    # Proportional Dimension
    prop_dimension = math.sqrt((x_min - x_max) ** 2 + (y_min - y_max) ** 2)

    # Width of the Force Arrows
    arrow_width = 5.657e-3 * prop_dimension

    disp_scale = scale_factor

    # Getting the structure from the ENL
    number_nodes = node_list.shape[0]
    node_displacements = ENL[:, 4 * problem_dimension: 5 * problem_dimension]
    node_displacements_scaled = disp_scale * node_displacements

    node_constraints = ENL[:, problem_dimension: 2 * problem_dimension]
    node_forces = ENL[:, 5 * problem_dimension:6 * problem_dimension]

    # Nodal Coordinates
    x_ini = node_list[:, 0]
    y_ini = node_list[:, 1]

    # For visualization purposes
    # We are gonna plot the scaled deformed shape
    x_end = x_ini + node_displacements_scaled[:, 0]
    y_end = y_ini + node_displacements_scaled[:, 1]

    fig, ax = plt.subplots(figsize = (20, 8)) # Width, Height
    # fig, ax = plt.subplots(figsize = (8, 20)) # Width, Height For Buckling Example

    for i in range(number_elements):
        node_i = element_list[i, 0]
        node_j = element_list[i, 1]

        coords_ini_i = ENL[node_i - 1, 0:2]
        coords_ini_j = ENL[node_j - 1, 0:2]

        x_element_ini = [coords_ini_i[0], coords_ini_j[0]]
        y_element_ini = [coords_ini_i[1], coords_ini_j[1]]

        # Plotting undeformed structure        
        ax.plot(x_element_ini, y_element_ini, dashes = [4, 4], color = 'green')

        x_element_end = [x_end[node_i - 1], x_end[node_j - 1]]
        y_element_end = [y_end[node_i - 1], y_end[node_j - 1]]

        # Plotting deformed structure
        ax.plot(x_element_end, y_element_end, color = 'red')

    # Plotting Node Displacementes
    ax.scatter(x_end, y_end, s = 50, facecolor = 'k', edgecolor = 'k', linewidths = 1, zorder = 1)

    # Plotting Node Reactions
    for i in range(0,number_nodes):
        boundary_node_conditions = node_constraints[i, :]

        if np.any(boundary_node_conditions < 0):
            x_node = x_end[i]
            y_node = y_end[i]

            reactions = np.round(node_forces[i, :], decimals = 2)

            for j in range(0, problem_dimension):

                reaction = reactions[j]

                match j:
                    case 0: # Fx
                        if reaction > 0: # Positive Fx
                            ax.annotate(str(reaction) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node - 7.1e-2 * prop_dimension, y_node + 7e-3 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node - 7.1e-2 * prop_dimension,
                                     y_node, 
                                     6.36e-2 * prop_dimension,
                                     0,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                            
                        elif reaction < 0:
                            ax.annotate(str(abs(reaction)) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 7.1e-2 * prop_dimension, y_node + 7e-3 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node + 7.1e-2 * prop_dimension, 
                                     y_node,
                                     -6.36e-2 * prop_dimension,
                                     0,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                    case 1: # Fy
                        if reaction > 0: # Positive Fy
                            ax.annotate(str(reaction) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 7e-3 * prop_dimension, y_node - 7.1e-2 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node,
                                     y_node - 7.06e-2 * prop_dimension, 
                                     0, 
                                     5.66e-2 * prop_dimension,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                            
                        elif reaction < 0:
                            ax.annotate(str(abs(reaction)) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 7e-3 * prop_dimension, y_node - 7.1e-2 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node, 
                                     y_node - 7e-3 * prop_dimension, 
                                     0, 
                                     -5.66e-2 * prop_dimension,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)

    ax.set_xlabel("x [m]", fontsize = label_fontsize)
    ax.set_ylabel("y [m]", fontsize = label_fontsize)
    fig_save_name = "./Fig/deformation.pdf"
    plt.savefig(fig_save_name, bbox_inches = "tight")
    plt.show()