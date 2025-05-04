import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import math

def plot_deformation_colorbar_truss(ENL, node_list, element_list, scale_factor):

    problem_dimension = np.size(node_list, 1)
    number_elements = np.size(element_list, 0)

    disp_scale = scale_factor

    # Getting the structure from the ENL
    node_displacements = ENL[:, 4 * problem_dimension: 5 * problem_dimension]
    node_displacements_scaled = disp_scale * node_displacements

    # Nodal Coordinates
    x_ini = node_list[:, 0]
    y_ini = node_list[:, 1]

    # For visualization purposes
    # We are gonna plot the scaled deformed shape
    x_end = x_ini + node_displacements_scaled[:, 0]
    y_end = y_ini + node_displacements_scaled[:, 1]


    # Plotting Ux and Uy in the same figure
    fig, ax = plt.subplots(2, 1, figsize = (10, 12))

    x_scatter = []
    y_scatter = []
    color_x = []
    color_y = []
    scatter_value = 200

    for i in range(number_elements):
        node_i = element_list[i, 0]
        node_j = element_list[i, 1]

        # Reference Configuration
        coords_ini_i = node_list[node_i - 1, :]
        coords_ini_j = node_list[node_j - 1, :]

        x_element_ini = [coords_ini_i[0], coords_ini_j[0]]
        y_element_ini = [coords_ini_i[1], coords_ini_j[1]]

        # Plotting undeformed structure        
        ax[0].plot(x_element_ini, y_element_ini, dashes = [4, 4], color = 'green')
        ax[1].plot(x_element_ini, y_element_ini, dashes = [4, 4], color = 'green')

        # Deformed Configuration
        xi_end = x_end[node_i - 1]
        yi_end = y_end[node_i - 1]
        xj_end = x_end[node_j - 1]
        yj_end = y_end[node_j - 1]

        # The displacements are
        dispx_element = np.array([node_displacements[node_i - 1, 0],
                                  node_displacements[node_j - 1, 0]])
        
        dispy_element = np.array([node_displacements[node_i - 1, 1],
                                  node_displacements[node_j - 1, 1]])
        
        # Dividing the lines in points
        if xj_end == xi_end:
            x = np.linspace(xi_end, xj_end, scatter_value)
            y = np.linspace(yi_end, yj_end, scatter_value)
        else:
            m = (yj_end - yi_end) / (xj_end - xi_end)
            x = np.linspace(xi_end, xj_end, scatter_value)
            y = m * (x - xi_end) + yi_end
        
        x_scatter.append(x)
        y_scatter.append(y)

        color_x.append(np.linspace(np.abs(dispx_element[0]), 
                                   np.abs(dispx_element[1]),
                                   scatter_value))
        
        color_y.append(np.linspace(np.abs(dispy_element[0]), 
                                   np.abs(dispy_element[1]),
                                   scatter_value))
        
    x_scatter = np.vstack([x_scatter]).flatten()
    y_scatter = np.vstack([y_scatter]).flatten()
    color_x = np.vstack([color_x]).flatten()
    color_y = np.vstack([color_y]).flatten()

    cmap = plt.get_cmap('jet')

    # Ux Scattering    
    ax[0].scatter(x_scatter, 
                  y_scatter, 
                  c = color_x, 
                  cmap = cmap, 
                  s = 10, 
                  edgecolor = 'none')

    norm_x = Normalize(np.abs(node_displacements[:, 0].min()), 
                       np.abs(node_displacements[:, 0].max()))
    
    fig.colorbar(ScalarMappable(norm = norm_x, cmap = cmap),
                 ax = ax[0],
                 orientation = 'vertical')

    ax[0].set_xlabel("x [m]")
    ax[0].set_ylabel("y [m]")
    ax[0].set_title("Ux")

    # Uy Scattering
    cmap = plt.get_cmap('jet')
    ax[1].scatter(x_scatter, 
                  y_scatter, 
                  c = color_y, 
                  cmap = cmap, 
                  s = 10, 
                  edgecolor = 'none')

    norm_y = Normalize(np.abs(node_displacements[:, 1].max()), 
                       np.abs(node_displacements[:, 1].min()))
    
    fig.colorbar(ScalarMappable(norm = norm_y, cmap = cmap),
                 ax = ax[1],
                 orientation = 'vertical')

    ax[1].set_xlabel("x [m]")
    ax[1].set_ylabel("y [m]")
    ax[1].set_title("Uy")

    fig_save_name = "./Fig/deformation-colorbar.pdf"
    plt.savefig(fig_save_name, bbox_inches = "tight")
    plt.show()