import numpy as np
import math

def tangent_stiffness(E, A, L, Q, Ld, cx, cy):

    k = (E * A) / L * np.array([[cx ** 2, cx * cy, -cx ** 2, -cx * cy],
                                [cx * cy, cy ** 2, -cx * cy, -cy ** 2],
                                [-cx ** 2, -cx * cy, cx ** 2, cx * cy],
                                [-cx * cy, -cy ** 2, cx * cy, cy ** 2]])
    
    g = (1 / Ld) * np.array([[-cy ** 2, cx * cy, cy ** 2, -cx * cy],
                             [cx * cy, -cx ** 2, -cx * cy, cx ** 2],
                             [cy ** 2, -cx * cy, -cy ** 2, cx * cy],
                             [-cx * cy, cx ** 2, cx * cy, -cx ** 2]])
    kt = k + Q  * g
    return kt

def assemble_stiffness(kt1, kt2, kt3):
    # Assembling stiffness
    # In this case is manual, for the specific example
    # but we can use the linear algorythm to assemble the global
    # Stiffness Matrix [KG]
    K = np.array([[kt1[2, 2] + kt2[2, 2], kt1[2, 3] + kt2[2, 3], kt2[2, 0]],
                  [kt1[3, 2] + kt2[3, 2], kt1[3, 3] + kt2[3, 3], kt2[3, 0]],
                  [kt2[0, 2], kt2[0, 3], kt2[0, 0] + kt3[2, 2]]])
    
    return K

def assemble_external_load(F1, F2, F3):

    # In this case is manual, for the specific example
    f = np.array([F1[2] + F2[2], F1[3] + F2[3], F2[0] + F3[2]])

    return f

def obtain_deformed_element(coord_ini, coord_end, v, E, A):
    # Node i
    xi, yi = coord_ini
    # Node j
    xj, yj = coord_end

    L = math.sqrt((xj - xi) ** 2 + (yj - yi) ** 2)

    Ld = math.sqrt(((xj + v[2]) - (xi + v[0])) ** 2 + ((yj + v[3]) - (yi + v[1])) ** 2)

    u = L - Ld

    Q = (E * A / L) * u

    cx = ((xj + v[2]) - (xi + v[0])) / Ld
    cy = ((yj + v[3]) - (yi + v[1])) / Ld

    return Ld, cx, cy, u, Q

E = 70 # [GPa]
A = 645.2 # [mm^2]
P = np.array([0, -2000, 0])

# Linear Analysis
# Member 1:
cx = 4 / 5
cy = 3 / 5
L1 = 5
Q = 0

kt1 = tangent_stiffness(E, A, L1, Q, L1, cx, cy)

print("k1")
print(kt1)

# Member 2:
cx = -4 / 5
cy = 3 / 5
L2 = 5
Q = 0

kt2 = tangent_stiffness(E, A, L2, Q, L2, cx, cy)
print("k2")
print(kt2)

# Member 3:
cx = 1
cy = 0
L3 = 8
Q = 0

kt3 = tangent_stiffness(E, A, L3, Q, L3, cx, cy)
print("k3")
print(kt3)

K = assemble_stiffness(kt1, kt2, kt3)
print("Global Stiffness")
print(K)

# Linear Solution
d1 = np.linalg.solve(K, P)
print("Linear Approximation d1")
print(d1)

converged_error = 1000
tolerance = 0.001
count = 1

while converged_error > tolerance:
    # 1st Iteration
    # ----------------------------------------------------------------------------------------------
    print("-" * 25)
    print(count, "-th Iteration cycle")
    print("-" * 25)

    # Member1
    print("Member 1")
    # [xi, yi]
    coord_ini_1 = np.array([0, 0])
    coord_end_1 = np.array([4, 3])
    L1 = 5

    # Displacement Vector
    v1 = np.array([0, 0, d1[0], d1[1]])

    Ld1, cx1, cy1, u1, Q1 = obtain_deformed_element(coord_ini_1, coord_end_1, v1, E, A)

    kt1 = tangent_stiffness(E, A, L1, Q1, Ld1, cx1, cy1)

    T1 = np.array([cx1, cy1, -cx1, -cy1])

    F1 = T1 * Q1

    print("Ld1 = ", Ld1)
    print("cx1 = ", cx1)
    print("cy1 = ", cy1)
    print("u1 = ", u1)
    print("Q = ", Q1)
    print("Tangent Stiffness [KT-1]")
    print(kt1)
    print("Member load [F1]")
    print(F1)

    # Member2
    print("Member 2")
    # [xi, yi]
    coord_ini_2 = np.array([8, 0])
    coord_end_2 = np.array([4, 3])
    L2 = 5

    v2 = np.array([d1[2], 0, d1[0], d1[1]])

    Ld2, cx2, cy2, u2, Q2 = obtain_deformed_element(coord_ini_2, coord_end_2, v2, E, A)

    kt2 = tangent_stiffness(E, A, L2, Q2, Ld2, cx2, cy2)

    T2 = np.array([cx2, cy2, -cx2, -cy2])

    F2 = T2 * Q2

    print("Ld2 = ", Ld2)
    print("cx2 = ", cx2)
    print("cy2 = ", cy2)
    print("u2 = ", u2)
    print("Q2 = ", Q2)
    print("Tangent Stiffness [KT-2]")
    print(kt2)
    print("Member load [F2]")
    print(F2)

    # Member3
    print("Member 3")
    # [xi, yi]
    coord_ini_3 = np.array([0, 0])
    coord_end_3 = np.array([8, 0])
    L3 = 8

    v3 = np.array([0, 0, d1[2], 0])

    Ld3, cx3, cy3, u3, Q3 = obtain_deformed_element(coord_ini_3, coord_end_3, v3, E, A)

    kt3 = tangent_stiffness(E, A, L3, Q3, Ld3, cx3, cy3)

    T3 = np.array([cx3, cy3, -cx3, -cy3])

    F3 = T3 * Q3

    print("Ld3 = ", Ld3)
    print("cx3 = ", cx3)
    print("cy3 = ", cy3)
    print("u3 = ", u3)
    print("Q3 = ", Q3)
    print("Tangent Stiffness [KT-3]")
    print(kt3)
    print("Member load [F3]")
    print(F3)

    # Assemble external load vector from the internal forces
    f1 = assemble_external_load(F1, F2, F3)
    St1 = assemble_stiffness(kt1, kt2, kt3)
    dU1 = P - f1
    print("f1 = ", f1)
    print("Stiffness Matrix [St1]")
    print(St1)
    print("Unbalanced joint force vector [dU1]")
    print(dU1)

    # Solving the linearized system
    delta_d1 = np.linalg.solve(St1, dU1)
    print(delta_d1)

    converged_error = np.linalg.norm(delta_d1) / np.linalg.norm(d1)
    print("e = ", converged_error)

    d2 = d1 + delta_d1

    print(d2)
    # Refreshing for the next iteration
    d1 = d2
    # Counter
    count += 1


print("Final deformed configuartion [d]")
print(d1)