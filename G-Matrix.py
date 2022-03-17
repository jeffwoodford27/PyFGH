from scipy import linalg
import numpy as np

a_matrix = [[2, 1, 0, 0, 0], [1, 4, 1, 0, 0], [0, 1, 4, 1, 0], [0, 0, 1, 4, 1], [0, 0, 0, 1, 2]]
inv_a_matrix = linalg.inv(a_matrix)

""" The first three indices of the arrays are xyz of oxygen, 4-6 are xyz of H1, 7-9 are xyz of H2 the first
line is the equilibrium, the other seven arrays are the displacements that correspond to the q1-q6 with equilibrium
in the middle (Array 5 in the matrix)"""

x_1 = [
    [-.017283, -.121171, 0, -1.2884569406, .8571139503, 0, 1.5627573484, 1.0659580057, 0],
    [-.011525, -.121225, 0, -1.3338037756, .892380982, 0, 1.5167153394, 1.0315493426, 0],
    [-.005763, -.121258, 0, -1.3793145864, .927443659, 0, 1.47078387, .9970084632, 0],
    [0, -.121268, 0, -1.4249788189, .9623132614, 0, 1.4249788189, .962313264, 0],
    [0.005763, -.121258, 0, -1.47078387, .9970084632, 0, 1.3793145864, .927443659, 0],
    [.011525, -.121225, 0, -1.5167153394, 1.0315493426, 0, 1.3338037756, .8923820982, 0],
    [.017283, -.121171, 0, -1.5627573484, 1.0659580057, 0, 1.2884569406, .8571139503, 0]]

x_2 = [[0, -.1339309737, 0, -1.5721113516, 1.0627905986, 0, 1.5721113516, 1.0627905986, 0],
       [0, -.129708459, 0, -1.5230798617, 1.0292834213, 0, 1.5230798617, 1.0292834213, 0],
       [0, -.1254868723, 0, -1.4740420244, .9957836074, 0, 1.4740420244, .9957836074, 0],
       [0, -.121268999, 0, -1.4249788189, .9623132614, 0, 1.4249788189, .9623132614, 0],
       [0, -.1170511258, 0, -1.3759156133, .9288429154, 0, 1.3759156133, .9288429154, 0],
       [0, -.112836967, 0, -1.3268270507, .8954020451, 0, 1.3268270507, .8954020451, 0],
       [0, -.1086237375, 0, -1.2777321565, .8619685487, 0, 1.2777321565, .8619685487, 0]]

x_3 = [[0, -.1459500579, 0, -1.2474739211, 1.1581663686, 0, 1.2474739211, 1.1581663686, 0],
       [0, -.1380544583, 0, -1.310641939, 1.0955119368, 0, 1.310641939, 1.0955119368, 0],
       [0, -.1298184459, 0, -1.3698634177, 1.0301562071, 0, 1.3698634177, 1.0301562071, 0],
       [0, -.121268999, 0, -1.4249788189, .9623132614, 0, 1.4249788189, .9623132614, 0],
       [0, -.1124308662, 0, -1.4758618995, .8921794888, 0, 1.4758618995, .8921794888, 0],
       [0, -.1033301966, 0, -1.5223938936, .8199623921, 0, -1.5223938936, .8199623921, 0],
       [0, -.0939931564, 0, -1.5644716791, .7458696088, 0, 1.5644716791, .7458696088, 0]]

x_matrix_array = [x_1, x_2, x_3]
grid_length_array = [.434322, .4330676, .7347963]
q_vector_1 = [-.18614, -.124092, -.062046, 0, .062046, .124092, .18614]
q_vector_2 = [.1856005, .1237337, .0618668, 0, -.0618668, -.1237337, -.1856005]
q_vector_3 = [-.3149137, -.2099527, -.1049717, 0, .10497097, .2099404, .3149143]
atom_mass_vector = [16, 16, 16, 1.008, 1.008, 1.008, 1.008, 1.008, 1.008]


def dot_product(first_array, second_array):
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
    for i in range(n_atoms):
        total_mass += mass_vector[i]
    for i in range(n_atoms):
        r_vector[0] += mass_vector[i]*position_matrix[i][0]
        r_vector[1] += mass_vector[i]*position_matrix[i][1]
        r_vector[2] += mass_vector[i]*position_matrix[i][2]
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
    # rotate the displacement matrix to the appropriate position. disp matrix [i][j] = i(atom) j(coordinate)
    # need to update if statement to have a cutoff point that is close to zero to catch if denominator is relatively
    # zero
    numerator = 0
    denominator = 0
    for i in range(n_atoms):
        numerator += (mass_vector[i]*((dis_matrix[i][0]*eq_matrix[i][1])-(eq_matrix[i][0])*dis_matrix[i][1]))
        denominator += (mass_vector[i]*((eq_matrix[i][0]*dis_matrix[i][0])+(eq_matrix[i][1]*dis_matrix[i][1])))
    if denominator == 0:
        return dis_matrix
    angle_theta = np.arctan2(numerator, denominator)
    cos_theta = np.cos(angle_theta)
    sin_theta = np.sin(angle_theta)
    rotation_matrix = [[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0],
                       [0, 0, 1]]
    updated_dis_matrix = np.matmul(rotation_matrix, dis_matrix)
    return updated_dis_matrix


def calc_g(first_x, second_x, mass_vector, num_atoms, num_points_1, num_points_2, len_grid_1, len_grid_2):
    # calc_g finds the 7x7 matrix that will be each index in the larger G matrix
    # the derivative matrix will contain all the partial derivatives of every coordinate from the position matrix
    # delta_q = len_grid/num_points, delta_q_1 = .062046, delta_q_2 = .0618668, delta_q_3 = .1049709
    # the grid length for delta q 1 is: .434322, grid length for delta q 2 .4330676,
    # grid length for delta q 3 = .7347963, num points 1 and 2 determine the length of the inner matrices of the g
    # matrix, mass vector is a vector with nine components however they are three values in triplicate. first and
    # second x are arrays from their respective matrices that will be used to compute derivatives which will then
    # be used to calculate the g values for the inner g matrix. num atoms is the number of atoms the function is meant
    # to consider so for our test purposes this value will always be three, however when this program is meant to
    # deal with bigger molecules this number could scale accordingly to meet the number of atoms for the bigger molecule
    delta_q_1 = len_grid_1/num_points_1
    delta_q_2 = len_grid_2/num_points_2
    print("delta q 1 is: ", delta_q_1)
    print("delta q 2 is: ", delta_q_2)
    inner_g_matrix = np.zeros((num_points_1, num_points_2))
    d_x_1 = []
    d_x_2 = []
    for j in range(3*num_atoms):
        set_up_vector = []
        for i in range(len(first_x)):
            set_up_vector.append(first_x[i][j])
        d_x_1.append(arbitrary_k_vector(set_up_vector)/delta_q_1)
    for j in range(3*num_atoms):
        set_up_vector = []
        for i in range(len(second_x)):
            set_up_vector.append(second_x[i][j])
        d_x_2.append(arbitrary_k_vector(set_up_vector)/delta_q_2)
    for a in range(num_points_1):
        for b in range(num_points_2):
            g_sum = 0
            for i in range(3*num_atoms):
                g_sum += mass_vector[i]*(d_x_1[i][a]*d_x_2[i][b])
            inner_g_matrix[a][b] = g_sum

    return inner_g_matrix


def complete_g(x_array, mass_vector, num_atoms, num_points_1, num_points_2, grid_len):
    # x_array is actually an array of the position matrices of the three atoms that we are considering, grid_len
    # is actually an array of the different grid lengths that the calc g function will need to find the different
    # delta q values. complete g calls calc g passing its arguments to the calc g function. The complete g function is
    # basically a helper function that takes each of the values from the calc g function and puts them into a 3x3
    # matrix, called total_matrix in the function, and once the function has iterated through every point in the 3x3
    # matrix it returns the complete g matrix, called total_matrix in the function.
    total_matrix = np.zeros((3, 3), dtype=np.core.multiarray)
    for r in range(num_atoms):
        for s in range(r, num_atoms):
            total_matrix[r][s] = calc_g(x_array[r], x_array[s], mass_vector, num_atoms,
                                        num_points_1, num_points_2, grid_len[r], grid_len[s])
            total_matrix[s][r] = total_matrix[r][s]
    return total_matrix


def inverse_g(x_array, mass_vector, num_atoms, num_points_1, num_points_2, grid_len):
    # the inverted g function takes arguments that it passes to the complete g function which allows it to
    # get the original not inverted G matrix. We make a blank 3x3 matrix called inverted g, then we put a
    # blank 7x7 matrix at every index in the 3x3 matrix. So we essentially have a blank G matrix. The nested for loops
    # iterate through the original g matrix and pull out the i, j position from all nine outer matrices. It adds that
    # to a blank 3x3 matrix, called blank_outer_matrix, then it inverts the blank_outer_matrix and we then put those
    # inverted values into the i, j position of the inverted g matrix at the same point in the outer matrix that we got
    # them from in the original g matrix, allowing us to construct the inverted g piece by piece. We then return the
    # complete inverted g matrix.
    blank_outer_matrix = np.zeros((3*num_atoms-6, 3*num_atoms-6))
    inverted_g = np.zeros((num_atoms, num_atoms), dtype=np.core.multiarray)
    original_g = complete_g(x_array, mass_vector, num_atoms, num_points_1, num_points_2,
                            grid_len)
    # This loop is to make a blank 3x3 matrix with blank 7x7 matrices at every index
    for i in range(len(inverted_g)):
        for j in range(len(inverted_g)):
            inverted_g[i][j] = np.zeros((num_points_1, num_points_2), dtype=np.core.multiarray)
    # This loop goes through every point in the inner matrices
    for i in range(num_points_1):
        for j in range(num_points_2):
            for k in range(len(original_g)):
                for l in range(len(original_g)):
                    blank_inner_matrix = original_g[k][l]
                    blank_outer_matrix[k][l] = blank_inner_matrix[i][j]
            inverted_outer_matrix = linalg.inv(blank_outer_matrix)
            for m in range(len(original_g)):
                for n in range(len(original_g)):
                    inverted_g[m][n][i][j] = inverted_outer_matrix[m][n]

    return "inverted g is: ", inverted_g


print("test run: ", complete_g(x_matrix_array, atom_mass_vector, 3, 7, 7,
                               grid_length_array))

print("test run for inverse g: ", inverse_g(x_matrix_array, atom_mass_vector, 3, 7, 7, grid_length_array))
