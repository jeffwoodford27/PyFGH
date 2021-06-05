from scipy import linalg
import numpy as np

intarrayA = [15.99491, 1.00782, 1.00782]
intarrayD = [0, -1.4249788189, 1.4249788189]
intarrayF = [-0.121268999, 0.9623132614, 0.9623132614]
a_matrix = [[2, 1, 0], [1, 4, 1], [0, 1, 2]]
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
    updated_y_array = [3*(y_array[1]-y_array[0]), 3*(y_array[2]-y_array[0]), 3*(y_array[2]-y_array[1])]
    print("The original y array is: " + str(y_array))
    print("The updated y array is: " + str(updated_y_array))
    k_array = np.matmul(inv_a_matrix, updated_y_array)
    return k_array


print("the dot product of array A and array D is: " + str(dot_product(intarrayA, intarrayD)))
# The result should be 0
print("the dot product of array A and array F is: " + str(dot_product(intarrayA, intarrayF)))
# The result should be -5e-7
print("the cross product of A, D, and F is: " + str(cross_product(intarrayA, intarrayD, intarrayF)))
print("The cross product of T1,T2,and T3 is: " + str(cross_product(T1, T2, T3)))
# The result should be -24
print("The K vector of the y array [1, 2, 3] (Linear) is: " + str(k_vector([1, 2, 3])))
# The result should be [1, 1, 1]
print("The K vector of the y array [1, 4, 9] (Quadratic) is: " + str(k_vector([1, 4, 9])))
# I'm honestly not sure what the result of this should be, but it outputs [2.5, 4, 5.5]
