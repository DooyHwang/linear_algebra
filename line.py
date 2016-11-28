from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 10


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = 0
        self.constant_term = constant_term

        self.set_basepoint()

    def is_parallel(self, l):
        return self.normal_vector.is_parallel(l.normal_vector)

    def intersect_with(self, l):
        if self == l:
            return self
        elif self.is_parallel(l):
            return None
        a, b = self.normal_vector
        c, d = l.normal_vector
        k1 = self.constant_term
        k2 = l.constant_term
        return Vector([round((d*k1 - b*k2) / (a*d - b*c), 3), round((a*k2 - c*k1) / (a*d - b*c), 3)])

    def get_parallel_vector(self):
        a, b = self.normal_vector
        return Vector([b, -a])

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            print("initial_coefficient : ", initial_coefficient)
            print("base coords : ", basepoint_coords[initial_index])
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __eq__(self, other):
        if self.normal_vector.magnitude() == 0:
            return other.normal_vector.magnitude() == 0
        elif other.normal_vector.magnitude() == 0:
            return False

        if not self.is_parallel(other):
            return False
        base_point_diff = self.basepoint.minus(other.basepoint)
        return base_point_diff.is_orthogonal(self.normal_vector)

    def __str__(self):
        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

if __name__ == "__main__":
    print(getcontext().prec)
    # Quiz 1
    l1 = Line(Vector([4.046, 2.836]), 1.21)
    l2 = Line(Vector([10.115, 7.09]), 3.025)
    l3 = Line(Vector([7.204, 3.182]), 8.68)
    l4 = Line(Vector([8.172, 4.114]), 9.883)
    l5 = Line(Vector([1.182, 5.562]), 6.744)
    l6 = Line(Vector([1.773, 8.343]), 9.525)
    print(l1, " and ", l2, " intersection : ", l1.intersect_with(l2))
    print(l3, " and ", l4, " intersection : ", l3.intersect_with(l4))
    print(l5, " and ", l6, " intersection : ", l5.intersect_with(l6))
