import numpy as np

def get_nonlinear_input_data(problem):
    path = "./Examples/Nonlinear/"
    # ----------------------------------------------------------------------------
    # NODE LIST
    # ----------------------------------------------------------------------------
    # [x,y]
    node_list_txt = path + problem + "_node_list.txt"
    node_list = np.loadtxt(node_list_txt, delimiter = ",")

    # ----------------------------------------------------------------------------
    # ELEMENT LIST
    # ----------------------------------------------------------------------------
    element_list_txt = path + problem + "_element_list.txt"
    element_list = np.loadtxt(element_list_txt, dtype = int, delimiter = ",")

    # ----------------------------------------------------------------------------
    # NODE RESTRAINTS
    # ----------------------------------------------------------------------------
    # -1: Fixed
    # +1: Free
    # [x,y]
    # ----------------------------------------------------------------------------
    boundary_conditions_txt = path + problem + "_boundary_conditions.txt"
    boundary_conditions = np.loadtxt(boundary_conditions_txt, delimiter = ",")

    # ----------------------------------------------------------------------------
    # NODE FORCES Fu
    # ----------------------------------------------------------------------------
    # [Fx, Fy]
    external_loads_txt = path + problem + "_external_loads.txt"
    external_loads = np.loadtxt(external_loads_txt, delimiter = ",")

    # ----------------------------------------------------------------------------
    # DISPLACEMENTS [U_u]
    # ----------------------------------------------------------------------------
    # Initially zeros
    node_displacements_txt = path + problem + "_displacements.txt"
    displacements = np.loadtxt(node_displacements_txt, delimiter = ",")

    return (node_list, boundary_conditions, element_list, external_loads, displacements)