def worst_case_error(correct_vec, test_vec):
    """
    Computes the worst-case error between two vectors of the same length.

    Parameters:
        correct_vec (list): The correct vector.
        test_vec (list): The test vector.

    Returns:
        float: The worst-case error between the two vectors.
    """
    if len(correct_vec) != len(test_vec):
        raise ValueError("Vectors must be of the same length.")

    max_error = 0
    for i in range(len(correct_vec)):
        error = abs(correct_vec[i] - test_vec[i])
        if error > max_error:
            max_error = error
    
    return max_error

def max_bit_flip_error(correct_vec, test_vec, binary='00000'):
    """
    Computes the maximum bit flip error between two vectors of the same length.

    Parameters:
        correct_vec (list): The correct vector.
        test_vec (list): The test vector.

    Returns:
        int: The maximum number of bit flips between the two vectors in a single test.
    """
    if len(correct_vec) != len(test_vec):
        raise ValueError("Vectors must be of the same length.")

    num_bits = len(correct_vec)
    max_flips = 0
    for i in range(num_bits):
        bin_correct = bin(correct_vec[i])[2:].zfill(len(binary))
        bin_test = bin(test_vec[i])[2:].zfill(len(binary))
        flips = sum([bin_correct[j] != bin_test[j] for j in range(len(bin_correct))])
        max_flips = max(max_flips, flips)

    return max_flips


def error_rate(input_vector1, input_vector2, exact_result, approx_result):
    """
    Computes the error rate between two vectors of the same length.

    Parameters:
        input_vector1 (list): The first input vector.
        input_vector2 (list): The second input vector.
        exact_result (list): The exact results vector.
        approx_result (list): The approximate results vector.

    Returns:
        float: The error rate between the two result vectors, as a percentage.
    """
    if len(exact_result) != len(approx_result):
        raise ValueError("Exact result and approximate result vectors must be of the same length.")

    num_tests = len(exact_result)
    num_possible_values = 2 ** (len(input_vector1) + len(input_vector2))
    num_errors = num_tests # SAT solver give all inputs which produce a non matching output
    error_rate = (num_errors * 1.0 / num_possible_values) * 100

    return error_rate


def average_case_error(input_vector1, input_vector2, exact_result, approx_result):
    """
    Computes the average case error rate between two vectors of the same length.

    Parameters:
        input_vector1 (list): The first input vector.
        input_vector2 (list): The second input vector.
        exact_result (list): The exact results vector.
        approx_result (list): The approximate results vector.

    Returns:
        float: The average case error rate between the two result vectors, as a percentage.
    """
    if len(exact_result) != len(approx_result):
        raise ValueError("Exact result and approximate result vectors must be of the same length.")

    num_tests = len(exact_result)
    num_possible_values = 2 ** (len(input_vector1) + len(input_vector2))
    num_errors = 0
    for i in range(num_tests):
        num_errors += abs(exact_result[i]-approx_result[i])

    error_rate = num_errors * 1.0 / num_possible_values

    return error_rate
