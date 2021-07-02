from scipy import linalg
import numpy as np
import math

intarrayA = [15.99491, 1.00782, 1.00782]
intarrayD = [0, -1.4249788189, 1.4249788189]
intarrayF = [-0.121268999, 0.9623132614, 0.9623132614]
a_matrix = [[2, 1, 0, 0, 0], [1, 4, 1, 0, 0], [0, 1, 4, 1, 0], [0, 0, 1, 4, 1], [0, 0, 0, 1, 2]]
inv_a_matrix = linalg.inv(a_matrix)
# print("The original matrix is: " + str(a_matrix))
# print("The inverted matrix is: " + str(linalg.inv(a_matrix)))

T1 = [1, 2, 3]
T2 = [4, 5, 6]
T3 = [7, 8, 9]

print("Hello")


def dot_product(first_array, second_array):
    dot_sum = 0
    if len(first_array) == len(second_array):
        dot_array = (first_array[0]*second_array[0]) + (first_array[1]*second_array[1]) + (first_array[2]*second_array[2])
        dot_p = dot_array/sum(first_array)
        return dot_p
    else:
        return "The arrays need to be the same length"


def cross_product(first_array, second_array, third_array):
    if len(first_array) == 2:
        return (first_array[0]*second_array[1]) - (first_array[1]*second_array[0])
    elif len(first_array) == 3:
        return (first_array[0]*((second_array[1]*third_array[2])-(second_array[2]*third_array[1]))) - (first_array[1]*(
                (second_array[2]*third_array[0])-(second_array[0]*third_array[2]))) + \
               (first_array[2]*((second_array[0]*third_array[1])-(second_array[1]*third_array[0])))


def k_vector(y_array):
    updated_y_array = [3*(y_array[1]-y_array[0]), 3*(y_array[2]-y_array[0]), 3*(y_array[3]-y_array[1]),
                       3*(y_array[4]-y_array[2]), 3*(y_array[4]-y_array[3])]
    print("The original y array is: " + str(y_array))
    print("The updated y array is: " + str(updated_y_array))
    k_array = np.matmul(inv_a_matrix, updated_y_array)
    return k_array


def arbitrary_k_vector(y_array):
    y_length = len(y_array)
    iterated_y_array = []
    m_matrix = np.zeros((y_length, y_length))
    m_matrix[0][0] = 2
    m_matrix[0][1] = 1
    m_matrix[y_length-1][y_length-1] = 2
    m_matrix[y_length-1][y_length-2] = 1
    for i in range(y_length-2):
        m_matrix[i+1][i] = 1
        m_matrix[i+1][i+1] = 4
        m_matrix[i+1][i+2] = 1
    inv_m_matrix = linalg.inv(m_matrix)
    iterated_y_array.append(3 * (y_array[1] - y_array[0]))
    iterated_y_array.append(3 * (y_array[2] - y_array[0]))
    for i in range(1, y_length-2):
        iterated_y_array.append(3*(y_array[i+2]-y_array[i]))
    iterated_y_array.append(3*(y_array[y_length-1]-y_array[y_length-2]))
    k_array = np.matmul(inv_m_matrix, iterated_y_array)
    return k_array


def eckart_translation(position_matrix, mass_vector, n_atoms):
    # r_vector has rx, ry, and rz stored inside of it, we add all the masses calculate rx, ry, and rz then scale 
    # the entire r vector by dividing by the total mass. Then the position matrix is altered by the value of the r
    # vector for the corresponding position. This moves the center of mass of the molecule to the origin.
    total_mass = 0
    r_vector = np.zeros(n_atoms)
    for i in range(len(mass_vector)):
        total_mass += mass_vector[i]
    for i in range(n_atoms):
        r_vector[0] += position_matrix[i][0]
        r_vector[1] += position_matrix[i][1]
        r_vector[2] += position_matrix[i][2]
    r_vector = r_vector/total_mass
    for i in range(n_atoms):
        position_matrix[i][0] = position_matrix[i][0] - r_vector[0]
        position_matrix[i][1] = position_matrix[i][1] - r_vector[1]
        position_matrix[i][2] = position_matrix[i][2] - r_vector[2]
    return position_matrix


def eckart_rotation(n_atoms, eq_matrix, dis_matrix, mass_vector):
    # the upper and lower sums compare the equilibrium matrix and the displacement matrix, the comparison is scaled by
    # the mass of the molecule at that point. By diving the two values and taking the arc tangent we can get the angle
    # of the difference between the two matrices. Using the 3x3 rotation matrix and passing the angle to it we can then
    # rotate the displacement matrix to the appropriate position.
    upper_sum = 0
    lower_sum = 0
    for i in range(n_atoms):
        upper_sum += (mass_vector[i]*((dis_matrix[i][0]*eq_matrix[1][i])-(eq_matrix[i][0])*dis_matrix[1][i]))
        lower_sum += (mass_vector[i]*((eq_matrix[i][0]*dis_matrix[i][0])+(eq_matrix[1][i]*dis_matrix[1][i])))
    angle_theta = np.arctan(upper_sum/lower_sum)
    rotation_matrix = [[np.cos(angle_theta), -np.sin(angle_theta), 0], [np.sin(angle_theta), np.cos(angle_theta), 0],
                       [0, 0, 1]]
    updated_dis_matrix = np.matmul(rotation_matrix, dis_matrix)
    return updated_dis_matrix


"""
print("the dot product of array A and array D is: " + str(dot_product(intarrayA, intarrayD)))
# The result should be 0

print("the dot product of array A and array F is: " + str(dot_product(intarrayA, intarrayF)))
# The result should be -5e-7

print("the cross product of A, D, and F is: " + str(cross_product(intarrayA, intarrayD, intarrayF)))

print("The cross product of T1,T2,and T3 is: " + str(cross_product(T1, T2, T3)))
# The result should be -24

# print("The K vector of the y array [1, 2, 3] (Linear) is: " + str(k_vector([1, 2, 3])))
# The result should be [1, 1, 1]

print("The K vector of the y array [1, 4, 9, 16, 25] (Quadratic) is: " + str(k_vector([1, 4, 9, 16, 25])))
# I'm honestly not sure what the result of this should be, but it outputs [2.5, 4, 5.5]

# print(("The slope, first derivative, and second derivative of the array [1, 2, 3, 4, 5] is: ",
#      derivative([1, 2, 3, 4, 5])))
# The output should be 'Linear', first derivative of 1, second derivative of 0

# print("The slope, first derivative, and second derivative of the array [1, 4, 9, 16, 25] is: ",
#      derivative([1, 4, 9, 16, 25]))
# The output should be 'Quadratic, first derivative of [2, 4, 6, 8, 10], second derivative of 2
print("First derivative using arbitrary length (Linear): ", arbitrary_k_vector([1, 2, 3, 4, 5]))
print("First derivative using arbitrary length (Linear): ", arbitrary_k_vector([1, 2, 3, 4, 5, 6, 7]))
print("First derivative using arbitrary length (Quad): ", arbitrary_k_vector([1, 4, 9, 16, 25]))
print("First derivative using arbitrary length (Quad): ", arbitrary_k_vector([1, 4, 9, 16, 25, 36, 49]))
print("Second derivative using arbitrary length (Quad): ",
      arbitrary_k_vector(arbitrary_k_vector([1, 4, 9, 16, 25, 36, 49])))
"""


print("The center of mass is: ", eckart_translation([[0, 0, 0], [1, 0, 1], [1, 0, -1]], [16, 1.008, 1.008], 3))
print("Eckart rotation: \n", eckart_rotation(3, [[0, -.1216899, 0], [-1.4249788189, .9623132614, 0],
                                               [1.4249788189, .9623132614, 0]], [[-.0172834238, -.1211710472, 0],
                                                                                 [-1.2884569406, .8571139503, 0],
                                                                                 [1.5627573484, 1.0659580057, 0]],
                                           [16, 1.00782, 1.00782]))
