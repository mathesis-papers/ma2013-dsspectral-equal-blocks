import json
from fractions import Fraction
from itertools import combinations_with_replacement


def identity(order):
    return [[Fraction(row == column) for column in range(order)] for row in range(order)]


def block_matrix(sizes, eigenvalue):
    order = sum(sizes)
    result = [[Fraction(0) for column in range(order)] for row in range(order)]
    offset = 0
    for size in sizes:
        for row in range(offset, offset + size):
            for column in range(offset, offset + size):
                result[row][column] = (1 - eigenvalue) / size
                if row == column:
                    result[row][column] += eigenvalue
        offset += size
    return result


def linear(first, second, scale):
    return [[left + scale * right for left, right in zip(first_row, second_row)]
            for first_row, second_row in zip(first, second)]


def multiply(first, second):
    return [[sum(left * right for left, right in zip(row, column))
             for column in zip(*second)] for row in first]


def stochastic(matrix):
    order = len(matrix)
    assert all(value >= 0 for row in matrix for value in row)
    assert all(sum(row) == 1 for row in matrix)
    assert all(sum(column) == 1 for column in zip(*matrix))
    assert all(matrix[row][column] == matrix[column][row]
               for row in range(order) for column in range(order))


def trace(matrix):
    return sum(matrix[index][index] for index in range(len(matrix)))


def determinant(matrix):
    remaining = [row[:] for row in matrix]
    result = Fraction(1)
    for column in range(len(remaining)):
        pivot = next((row for row in range(column, len(remaining))
                      if remaining[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            remaining[pivot], remaining[column] = remaining[column], remaining[pivot]
            result = -result
        value = remaining[column][column]
        result *= value
        for row in range(column + 1, len(remaining)):
            scale = remaining[row][column] / value
            for index in range(column + 1, len(remaining)):
                remaining[row][index] -= scale * remaining[column][index]
    return result


def cycle(order):
    result = [[Fraction(0) for column in range(order)] for row in range(order)]
    for row, column, sign in [(0, 1, 1), (2, 3, 1), (1, 2, -1), (3, 0, -1)]:
        result[row][column] = result[column][row] = Fraction(sign)
    assert all(sum(row) == 0 for row in result)
    return result


def nonextreme(matrix, direction, scale):
    positive = linear(matrix, direction, scale)
    negative = linear(matrix, direction, -scale)
    stochastic(positive)
    stochastic(negative)
    assert positive != negative
    assert [[(left + right) / 2 for left, right in zip(positive_row, negative_row)]
            for positive_row, negative_row in zip(positive, negative)] == matrix


def sorted_partitions(total, parts, minimum=1):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total // parts + 1):
        for tail in sorted_partitions(total - first, parts - 1, first):
            yield (first,) + tail


def partition_count_dynamic(total, parts, maximum):
    counts = [[0] * (total + 1) for count in range(parts + 1)]
    counts[0][0] = 1
    for size in range(1, maximum + 1):
        for count in range(1, parts + 1):
            for subtotal in range(size, total + 1):
                counts[count][subtotal] += counts[count - 1][subtotal - size]
    return counts[parts][total]


def check_two_eigenvalue_corollaries():
    spectral_cases = 0
    admitted_partitions = 0
    zero_trace_cases = 0
    for order in range(2, 13):
        for copies in range(1, order):
            partitions = list(sorted_partitions(order, copies))
            for eigenvalue in (Fraction(-1), Fraction(-2, 3), Fraction(-1, 2),
                               Fraction(-1, 3), Fraction(0), Fraction(1, 4), Fraction(3, 4)):
                admitted = [parts for parts in partitions
                            if all(1 + (size - 1) * eigenvalue >= 0 for size in parts)]
                maximum = min(order, int(1 - 1 / eigenvalue)) if eigenvalue < 0 else order
                assert len(admitted) == partition_count_dynamic(order, copies, maximum)
                if eigenvalue >= 0:
                    assert (len(admitted) == 1) == (copies == 1 or copies == order - 1)
                for parts in admitted:
                    matrix = block_matrix(parts, eigenvalue)
                    stochastic(matrix)
                    assert trace(matrix) == copies + (order - copies) * eigenvalue
                    assert len(parts) == copies and sum(parts) == order
                spectral_cases += 1
                admitted_partitions += len(admitted)
            eigenvalue = Fraction(-copies, order - copies)
            if eigenvalue < -1:
                continue
            admitted = [parts for parts in partitions
                        if all(1 + (size - 1) * eigenvalue >= 0 for size in parts)]
            expected = [(order // copies,) * copies] if order % copies == 0 else []
            assert admitted == expected
            for parts in admitted:
                assert trace(block_matrix(parts, eigenvalue)) == 0
            zero_trace_cases += 1
    return {'spectral_parameter_cases': spectral_cases,
            'admitted_partition_instances': admitted_partitions,
            'zero_trace_parameter_cases': zero_trace_cases,
            'order_range': '2..12', 'multiplicity_range': '1..n-1',
            'eigenvalues': ['-1', '-2/3', '-1/2', '-1/3', '0', '1/4', '3/4'],
            'independent_count': 'recursive sorted partitions compared with generating-function dynamic programming',
            'zero_trace_eigenvalue': '-r/(n-r), restricted to [-1,0)'}


def main():
    inside_count = 0
    outside_count = 0
    cycle_count = 0
    partition_count = 0
    for size in range(2, 9):
        for copies in (2, 3):
            order = size * copies
            unit = identity(order)
            zero = [[Fraction(0) for column in range(order)] for row in range(order)]
            for parameter in (Fraction(0), Fraction(1, 4 * size * size),
                              Fraction(1, 2 * size * size), Fraction(3, 4 * size * size)):
                eigenvalue = (size * parameter - 1) / (size - 1)
                matrix = block_matrix([size] * copies, eigenvalue)
                stochastic(matrix)
                assert trace(matrix) == order * parameter
                assert multiply(linear(matrix, unit, -1),
                                linear(matrix, unit, -eigenvalue)) == zero
                projection = [[value / (1 - eigenvalue) for value in row]
                              for row in linear(matrix, unit, -eigenvalue)]
                assert multiply(projection, projection) == projection
                assert projection == block_matrix([size] * copies, Fraction(0))
                assert trace(projection) == copies
                admissible = []
                for parts in combinations_with_replacement(range(1, order + 1), copies):
                    if sum(parts) != order:
                        continue
                    partition_count += 1
                    if all(1 + (part - 1) * eigenvalue >= 0 for part in parts):
                        admissible.append(parts)
                assert admissible == [(size,) * copies]
                if size >= 4:
                    direction = cycle(order)
                    nonextreme(matrix, direction, matrix[0][1] / 2)
                    cycle_count += 1
                    for segment_parameter in (1 - parameter, 1 - parameter / 2, Fraction(1)):
                        vertex = [[value / segment_parameter for value in row]
                                  for row in linear(matrix, unit, -(1 - segment_parameter))]
                        stochastic(vertex)
                        nonextreme(vertex, direction, vertex[0][1] / 2)
                        cycle_count += 1
                inside_count += 1
            for parameter in (Fraction(1, size * size), Fraction(1, size),
                              Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)):
                eigenvalue = (size * parameter - 1) / (size - 1)
                matrix = block_matrix([size] * copies, eigenvalue)
                parts = [size - 1, size + 1] + [size] * (copies - 2)
                mate = block_matrix(parts, eigenvalue)
                stochastic(matrix)
                stochastic(mate)
                assert trace(matrix) == trace(mate)
                assert mate[0][0] != parameter
                assert sum(parts) == order and len(parts) == copies
                for spectral_parameter in range(5):
                    assert determinant(linear(unit, matrix, Fraction(-1, 10 + spectral_parameter))) == determinant(
                        linear(unit, mate, Fraction(-1, 10 + spectral_parameter)))
                outside_count += 1
            assert block_matrix([size] * copies, Fraction(1)) == unit
    size, copies, parameter = 4, 2, Fraction(1, 40)
    eigenvalue = (size * parameter - 1) / (size - 1)
    witness = block_matrix([size] * copies, eigenvalue)
    assert eigenvalue == Fraction(-3, 10)
    assert witness[0][0] == Fraction(1, 40)
    assert witness[0][1] == Fraction(13, 40)
    assert witness[0][4] == 0 and trace(witness) == Fraction(1, 5)
    for spectral_parameter in range(9):
        unit = identity(8)
        shifted = linear([[spectral_parameter * value for value in row] for row in unit],
                         witness, Fraction(-1))
        assert determinant(shifted) == (spectral_parameter - 1) ** 2 * (
            spectral_parameter + Fraction(3, 10)) ** 6
    result = {
        'arithmetic': 'Python fractions.Fraction; exact rational arithmetic throughout',
        'parameter_ranges': {'k': '2..8', 'r': [2, 3],
                             'determined': ['0', '1/(4k^2)', '1/(2k^2)', '3/(4k^2)'],
                             'cospectral_mates': ['1/k^2', '1/k', '1/2', '3/4', '99/100']},
        'determined_instances': inside_count,
        'cospectral_mate_instances': outside_count,
        'cospectral_mate_determinant_evaluations': 'det(I-A/(10+s)) = det(I-B/(10+s)), s=0..4; the common complete spectrum follows from the block formulas',
        'sorted_component_partitions_examined': partition_count,
        'nonextremality_witnesses': cycle_count,
        'identity_endpoints': 14,
        'order_eight_characteristic_polynomial': '(x-1)^2 (x+3/10)^6',
        'characteristic_polynomial_evaluation_points': 'integers 0..8 (degree 8)',
        'two_eigenvalue_corollaries': check_two_eigenvalue_corollaries(),
        'coverage': 'Finite rational checks of matrix identities, component partitions, cospectral mates and perturbations; the parameter classification and universal segment exclusions have written proofs in note.tex.',
        'status': 'ALL_CHECKS_OK'
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
