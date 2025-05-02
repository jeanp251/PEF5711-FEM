import numpy as np
import matplotlib.pyplot as plt
import math

def pre_process(node_list, boundary_conditions, element_list, external_loads):

    problem_dimension = np.size(node_list, 1)
    number_nodes = np.size(node_list, 0)
    number_elements = np.size(element_list, 0)

    # FIRST WE NEED TO GET A REFERENCE DIMENSION TO PLOT ALL THE STUFF IN
    # PROPORTION TO THIS MEASURE
    x_min = np.min(node_list[:, 0])
    y_min = np.min(node_list[:, 1])
    x_max = np.max(node_list[:, 0])
    y_max = np.max(node_list[:, 1])

    prop_dimension = math.sqrt((x_min - x_max) ** 2 + (y_min - y_max) ** 2)

    # Width of the Force Arrows
    arrow_width = 5.657e-3 * prop_dimension

    fig, ax = plt.subplots(figsize = (10, 10))

    # PLOT NODES
    for i in range(number_nodes):
        x_node = node_list[i, 0]
        y_node = node_list[i, 1]
        
        # PLOT NODES INFO
        ax.scatter(x_node, 
                   y_node, 
                   s = 50, 
                   facecolor = 'k', 
                   edgecolor = 'k',
                   linewidths = 3, 
                   zorder = 1)
        
        ax.annotate(str(i + 1), 
                    xy = (x_node, y_node),
                    xytext = (x_node + 7e-3 * prop_dimension, y_node + 7e-3 * prop_dimension))
    
        # PLOT NODAL FORCES
        for j in range(problem_dimension):
            nodal_force = external_loads[i, j]
            node_constraint = boundary_conditions[i, :]

            if nodal_force != 0:
                match j:
                    case 0: # Fx
                        if nodal_force > 0: # Positive Fx
                            ax.annotate(str(nodal_force) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node - 7.1e-2 * prop_dimension, y_node + 7e-3 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node - 7.1e-2 * prop_dimension, 
                                     y_node, 6.36e-2 * prop_dimension, 
                                     0,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                            
                        else: # Negative Fx
                            ax.annotate(str(abs(nodal_force)) + "N",
                                        xy = (x_node, y_node),
                                        xytext ="" (x_node + 7.1e-2 * prop_dimension, y_node + 7e-3 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node + 7.1e-2 * prop_dimension, 
                                     y_node, -6.36e-2 * prop_dimension,
                                     0,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                    case 1: # Fy
                        if nodal_force > 0: # Positive Fy
                            ax.annotate(str(nodal_force) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 7e-3 * prop_dimension, y_node + 7.1e-2 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node, y_node + 7e-3 * prop_dimension, 0, 6.36e-2 * prop_dimension,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True)
                        else: # Negative Fy
                            ax.annotate(str(abs(nodal_force)) + "N",
                                        xy = (x_node, y_node),
                                        xytext = (x_node + 7e-3 * prop_dimension, y_node + 7.1e-2 * prop_dimension),
                                        color = 'red')
                            ax.arrow(x_node, y_node + 6.36e-2 * prop_dimension, 0, -6.36e-2 * prop_dimension,
                                     width = arrow_width,
                                     color = 'red',
                                     length_includes_head = True) 
                            
        # PLOT NODE CONSTRAINTS
        if np.any(node_constraint < 0):
            delta_x = 3.5355e-2 * prop_dimension
            delta_y = delta_x
            delta_x_text = delta_x
            delta_y_text = 6.3639e-2 * prop_dimension
            restraint_x = np.array([x_node, 
                                    x_node + delta_x,
                                    x_node - delta_x,
                                    x_node])
            restraint_y = np.array([y_node,
                                    y_node - delta_y,
                                    y_node - delta_y,
                                    y_node])
            ax.plot(restraint_x, restraint_y, lw = 2, color = 'red')

            # Setting the info

            if node_constraint[0] < 0:
                ux = "Ux"
            else:
                ux = ""

            if node_constraint[1] < 0:
                uy = "Uy"
            else:
                uy = ""

            constraint_info = ux + uy

            ax.text(x_node - delta_x_text,
                    y_node - delta_y_text,
                    constraint_info,
                    color = 'red',
                    bbox = dict(facecolor = 'white', edgecolor = 'red')) 

    # PLOT ELEMENTS
    # Iterating over each element
    for i in range(number_elements):
        coord_ini = element_list[i, 0]
        coord_end = element_list[i, 1]

        # Initial Coordinates
        xi = node_list[coord_ini - 1, 0]
        yi = node_list[coord_ini - 1, 1]

        # End Coordinates
        xj = node_list[coord_end - 1, 0]
        yj = node_list[coord_end - 1, 1]

        # Centroid Coordinates
        xg = (xi + xj) / 2
        yg = (yi + yj) / 2

        x_element = np.array([xi, xj])
        y_element = np.array([yi, yj])

        ax.plot(x_element, y_element, lw = 2, color = 'blue', zorder = 0)
        ax.text(xg, 
                yg, 
                str(i + 1), 
                color = 'blue', 
                bbox = dict(facecolor = 'white', edgecolor = 'blue'))
        
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    fig_save_name = "./Fig/pre_process.pdf"
    plt.savefig(fig_save_name, bbox_inches = 'tight')
    plt.show()