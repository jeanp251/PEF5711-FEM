import numpy as np

def tangent_stiffness(E, A, L, Q, Ld, cx, cy):

    k = (E * A) / L * np.array([[cx ** 2, cx * cy, -cx ** 2, -cx * cy],
                                [cx * cy, cy ** 2, -cx * cy, -cy ** 2],
                                [-cx ** 2, -cx * cy, cx ** 2, cx * cy],
                                [-cx * cy, -cy ** 2, cx * cy, cy ** 2]])
    
    g = (1 / Ld) * np.array([[-cy ** 2, cx * cy, cy ** 2, -cx * cy],
                             [cx * cy, -cx ** 2, -cx * cy, cx ** 2],
                             [cy ** 2, -cx * cy, -cy ** 2, cx * cy],
                             [-cx * cy, cx ** 2, cx * cy, -cx ** 2]])
    kt = k - Q  * g
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

def obtain_deformed():
    
    return Ld, cx, cy, u, Q

E = 70e9 # [GPa]
A = 645.2e-6 # [mm^2]
P = np.array([0, -2000, 0])

# Linear Analysis
# Member 1:
cx = 4 / 5
cy = 3 / 5
L1 = 5
Q = 0

kt1 = tangent_stiffness(E, A, L1, Q, L1, cx, cy) / 1000

print("k1")
print(kt1)

# Member 2:
cx = -4 / 5
cy = 3 / 5
L2 = 5
Q = 0

kt2 = tangent_stiffness(E, A, L2, Q, L1, cx, cy) / 1000
print("k2")
print(kt2)

# Member 3:
cx = 1
cy = 0
L3 = 8
Q = 0

kt3 = tangent_stiffness(E, A, L3, Q, L3, cx, cy) / 1000
print("k3")
print(kt3)

K = assemble_stiffness(kt1, kt2, kt3)
print("Global Stiffness")
print(K)

d1 = np.linalg.solve(K, P)
print("d1")
print(d1)



Ld, cx, cy, u, Q = obtain_deformed()