from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):
    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        if row1 < len(self.planes) and row2 < len(self.planes):
            temp = self.planes[row1]
            self.planes[row1] = self.planes[row2]
            self.planes[row2] = temp

    def multiply_coefficient_and_row(self, coefficient, row):
        if row < len(self.planes):
            new_normal_vector = self.planes[row].normal_vector.times_scalar(coefficient)
            new_constant_term = self.planes[row].constant_term * coefficient
            self.planes[row] = Plane(new_normal_vector, new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        if row_to_add < len(self.planes) and row_to_be_added_to < len(self.planes):
            plane1 = self.planes[row_to_be_added_to]
            plane2 = self.planes[row_to_add]
            vector_to_add = plane2.normal_vector.times_scalar(coefficient)
            new_normal_vector = plane1.normal_vector.plus(vector_to_add)
            new_constant_term = plane1.constant_term + plane2.constant_term * coefficient
            self.planes[row_to_be_added_to] = Plane(new_normal_vector, new_constant_term)

    def compute_triangular_form(self):
        system = deepcopy(self)
        coefficient_index = 0
        for row in range(0, len(system)):
            while coefficient_index < system.dimension:
                if system[row].normal_vector[coefficient_index] == 0:
                    searched_index = system.search_row_with_nonzero_coefficient(row + 1, coefficient_index)
                    if searched_index != -1:
                        system.swap_rows(row, searched_index)
                    else:
                        coefficient_index += 1
                        continue
                for cleaned_row in range(row + 1, len(system)):
                    current_coefficient = system[cleaned_row].normal_vector[coefficient_index]
                    if current_coefficient != 0:
                        add_coefficient = -1 * current_coefficient / system[row].normal_vector[coefficient_index]
                        system.add_multiple_times_row_to_row(add_coefficient, row, cleaned_row)
                coefficient_index += 1
                break
        return system

    def search_row_with_nonzero_coefficient(self, row_from, coefficient_index):
        searched_index = -1
        for row in range(row_from, len(self)):
            if self[row].normal_vector[coefficient_index] != 0:
                searched_index = row
                break
        return searched_index

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i + 1, p) for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


if __name__ == "__main__":
    #Quiz : Coding Raw Operations
    p0 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=1)
    p1 = Plane(normal_vector=Vector([0, 1, 0]), constant_term=2)
    p2 = Plane(normal_vector=Vector([1, 1, -1]), constant_term=3)
    p3 = Plane(normal_vector=Vector([1, 0, -2]), constant_term=2)

    s = LinearSystem([p0, p1, p2, p3])

    s.swap_rows(0, 1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print('test case 1 failed')

    s.swap_rows(1, 3)
    if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
        print('test case 2 failed')

    s.swap_rows(3, 1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print('test case 3 failed')

    s.multiply_coefficient_and_row(1, 0)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print('test case 4 failed')

    s.multiply_coefficient_and_row(-1, 2)
    if not (s[0] == p1 and
                    s[1] == p0 and
                    s[2] == Plane(normal_vector=Vector([-1, -1, 1]), constant_term=-3) and
                    s[3] == p3):
        print('test case 5 failed')

    s.multiply_coefficient_and_row(10, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector([10, 10, 10]), constant_term=10) and
                    s[2] == Plane(normal_vector=Vector([-1, -1, 1]), constant_term=-3) and
                    s[3] == p3):
        print('test case 6 failed')

    s.add_multiple_times_row_to_row(0, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector([10, 10, 10]), constant_term=10) and
                    s[2] == Plane(normal_vector=Vector([-1, -1, 1]), constant_term=-3) and
                    s[3] == p3):
        print('test case 7 failed')

    s.add_multiple_times_row_to_row(1, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector([10, 11, 10]), constant_term=12) and
                    s[2] == Plane(normal_vector=Vector([-1, -1, 1]), constant_term=-3) and
                    s[3] == p3):
        print('test case 8 failed')

    s.add_multiple_times_row_to_row(-1, 1, 0)
    if not (s[0] == Plane(normal_vector=Vector([-10, -10, -10]), constant_term=-10) and
                    s[1] == Plane(normal_vector=Vector([10, 11, 10]), constant_term=12) and
                    s[2] == Plane(normal_vector=Vector([-1, -1, 1]), constant_term=-3) and
                    s[3] == p3):
        print('test case 9 failed')

    #Quiz : Coding Triangular Form
    p1 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([0, 1, 1]), constant_term=2)
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and t[1] == p2):
        print('test case 1 failed')

    p1 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=2)
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and t[1] == Plane(constant_term=1)):
        print('test case 2 failed')

    p1 = Plane(normal_vector=Vector([1, 1, 1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([0, 1, 0]), constant_term=2)
    p3 = Plane(normal_vector=Vector([1, 1, -1]), constant_term=3)
    p4 = Plane(normal_vector=Vector([1, 0, -2]), constant_term=2)
    s = LinearSystem([p1, p2, p3, p4])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
                    t[1] == p2 and
                    t[2] == Plane(normal_vector=Vector([0, 0, -2]), constant_term=2) and
                    t[3] == Plane()):
        print('test case 3 failed')

    p1 = Plane(normal_vector=Vector([0, 1, 1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([1, -1, 1]), constant_term=2)
    p3 = Plane(normal_vector=Vector([1, 2, -5]), constant_term=3)
    s = LinearSystem([p1, p2, p3])
    t = s.compute_triangular_form()
    if not (t[0] == Plane(normal_vector=Vector([1, -1, 1]), constant_term=2) and
                    t[1] == Plane(normal_vector=Vector([0, 1, 1]), constant_term=1) and
                    t[2] == Plane(normal_vector=Vector([0, 0, -9]), constant_term=-2)):
        print('test case 4 failed')

