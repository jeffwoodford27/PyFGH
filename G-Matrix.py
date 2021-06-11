from scipy import linalg
import numpy as np
import math

intarrayA = [15.99491, 1.00782, 1.00782]
intarrayD = [0, -1.4249788189, 1.4249788189]
intarrayF = [-0.121268999, 0.9623132614, 0.9623132614]
a_matrix = [[2, 1, 0, 0, 0], [1, 4, 1, 0, 0], [0, 1, 4, 1, 0], [0, 0, 1, 4, 1], [0, 0, 0, 1, 2]]
inv_a_matrix = linalg.inv(a_matrix)
print("The original matrix is: " + str(a_matrix))
print("The inverted matrix is: " + str(linalg.inv(a_matrix)))

T1 = [1, 2, 3]
T2 = [4, 5, 6]
T3 = [7, 8, 9]


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
    dummy_index = (y_length, y_length)
    empty_matrix = np.zeros(dummy_index)
    empty_matrix[0][0] = 2
    empty_matrix[0][1] = 1
    empty_matrix[y_length-1][y_length-1] = 2
    empty_matrix[y_length-1][y_length-2] = 1
    for i in range(y_length-2):
        empty_matrix[i+1][i] = 1
        empty_matrix[i+1][i+1] = 4
        empty_matrix[i+1][i+2] = 1
    inv_emp_matrix = linalg.inv(empty_matrix)
    for i in range(y_length):
        if i == 0:
            iterated_y_array.append(3*(y_array[i+1]-y_array[i]))
            iterated_y_array.append(3*(y_array[i+2]-y_array[i]))
        elif 0 < i < y_length-2:
            iterated_y_array.append(3*(y_array[i+2]-y_array[i]))
        elif i == y_length-2:
            iterated_y_array.append(3*(y_array[i+1]-y_array[i]))
    k_array = np.matmul(inv_emp_matrix, iterated_y_array)
    return k_array


"""
def derivative(y_array):
    This function looks at all the points given to it and determines if the slope is
    linear or quadratic based on the point before it, if each of the slopes are linear it
    outputs linear, if the square root of each of the slopes is linear it outputs Quadratic
    y_linear = 0
    y_quad = 0
    first_der_array = []
    for i in range(len(y_array)-1):
        if y_array[i+1] - y_array[i] == 1:
            y_linear += 1
            if y_linear == len(y_array)-1:
                slope = "Linear"
                first_der = 1
                second_der = 0
                return slope, first_der, second_der
        elif math.sqrt(y_array[i+1]) - math.sqrt(y_array[i]) == 1:
            y_quad += 1
            if y_quad == len(y_array)-1:
                slope = "Quadratic"
                for j in range(len(y_array)):
                    first_der_array.append(2*math.sqrt(y_array[j]))
                second_der = 2
                return slope, first_der_array, second_der
        else:
            return "Something went wrong"

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
