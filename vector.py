import math
from decimal import *
class Vector(object):
    CANNOT_COMPUTE_ANGLE_WITH_ZERO_VECTOR_MSG = 'Cannot compute an angle with the zero vector'
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two of three dims'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)
            self.current_index = 0
        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        self.current_index = 0
        return self

    def __getitem__(self, item):
        return self.coordinates[item]

    def __next__(self):
        if self.current_index >= len(self.coordinates):
            raise StopIteration
        else:
            current_value = self.coordinates[self.current_index]
            self.current_index += 1
            return current_value

    def plus(self, v):
        new_coordinate = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinate)

    def minus(self, v):
        new_coordinate = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinate)

    def times_scalar(self, c):
        new_coordinate = [c * x for x in self.coordinates]
        return Vector(new_coordinate)

    def magnitude(self):
        return math.sqrt(sum([x ** 2 for x in self.coordinates]))

    def normalized(self):
        try:
            magnitude_inverse = 1 / self.magnitude()
            new_coordinate = [magnitude_inverse * x for x in self.coordinates]
            return Vector(new_coordinate)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return round(sum([x * y for x, y in zip(self.coordinates, v.coordinates)]), 10)

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = math.acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian = 180./ math.pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except ZeroDivisionError:
            raise Exception(self.CANNOT_COMPUTE_ANGLE_WITH_ZERO_VECTOR_MSG)

    def is_parallel(self, v):
        if self.magnitude() == 0 or v.magnitude() == 0:
            return True
        angle = self.angle_with(v)
        return angle == 0 or angle == Decimal(math.pi)

    def is_orthogonal(self, v):
        #print("is_orthogonal dot : ", self.dot(v), " Decimal : ", Decimal(self.dot(v)))
        return Decimal(self.dot(v)) == 0

    def component_parallel_to(self, basis):
        try:
            ub = basis.normalized()
            return ub.times_scalar(self.dot(ub))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            self_wrap = self
            if len(self.coordinates) == 2:
                new_coordinates = list(self.coordinates)
                new_coordinates.append(0)
                self_wrap = Vector(new_coordinates)
            if len(v.coordinates) == 2:
                new_coordinates = list(v.coordinates)
                new_coordinates.append(0)
                v = Vector(new_coordinates)
            x_1, y_1, z_1 = self_wrap.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1 * z_2 - y_2 * z_1, -(x_1 * z_2 - x_2 * z_1), x_1 * y_2 - x_2 * y_1]
            return Vector(new_coordinates)
        except ValueError:
            raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def area_of_triangle_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude() / 2

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

if __name__ == "__main__":
    print(getcontext().prec)
    # Quiz 1
    v1 = Vector([8.218, -9.341])
    v2 = Vector([-1.129, 2.111])
    print(v1, "+", v2, "=", v1.plus(v2))

    v1 = Vector([7.119, 8.215])
    v2 = Vector([-8.223, 0.878])
    print(v1, "-", v2, "=", v1.minus(v2))

    v3 = Vector([1.671, -1.012, -0.318])
    c = 7.41
    print(c, v3, "=", v3.times_scalar(c))

    # Quiz 2
    v1 = Vector([-0.221, 7.437])
    v2 = Vector([8.813, -1.331, -6.247])
    print("magnitude of ", v1, "=",v1.magnitude())
    print("magnitude of ", v2, "=", v2.magnitude())

    v3 = Vector([5.581, -2.136])
    v4 = Vector([1.996, 3.108, -4.554])
    print("normalization of ", v3, "=", v3.normalized())
    print("normalization of ", v4, "=", v4.normalized())

    # Quiz 3
    v1 = Vector([7.887, 4.138])
    v2 = Vector([-8.802, 6.776])
    print(v1, " dot ", v2, "=", v1.dot(v2))

    v3 = Vector([3.183, -7.627])
    v4 = Vector([-2.668, 5.319])
    print("angle of ", v3, " and ", v4, "=", v3.angle_with(v4))
    print("angle of ", v3, " and ", v4, "=", v3.angle_with(v4, True))

    # Quiz 4
    v = Vector([-7.579, -7.88])
    w = Vector([22.737, 23.64])
    v1 = Vector([-2.029, 9.97, 4.172])
    w1 = Vector([-9.231, -6.629, -7.245])
    v2 = Vector([-2.328, -7.284, -1.214])
    w2 = Vector([-1.821, 1.072, -2.94])
    v3 = Vector([2.118, 4.827])
    w3 = Vector([0, 0])
    print(v, ",", w, " parallel : ", v.is_parallel(w) ," orthogonal : ", v.is_orthogonal(w))
    print(v1, ",", w1, " parallel : ", v1.is_parallel(w1), " orthogonal : ", v1.is_orthogonal(w1))
    print(v2, ",", w2, " parallel : ", v2.is_parallel(w2), " orthogonal : ", v2.is_orthogonal(w2))
    print(v3, ",", w3, " parallel : ", v3.is_parallel(w3), " orthogonal : ", v3.is_orthogonal(w3))

    # Quiz 5
    v = Vector([3.039, 1.879])
    b = Vector([0.825, 2.036])
    v1 = Vector([-9.88, -3.264, -8.159])
    b1 = Vector([-2.155, -9.353, -9.473])
    v2 = Vector([3.009, -6.172, 3.692, -2.51])
    b2 = Vector([6.404, -9.144, 2.759, 8.718])
    print(v, " component_parallel_to ", b, " is : ", v.component_parallel_to(b))
    print(v1, " component_orthogonal_to ", b1, " is : ", v1.component_orthogonal_to(b1))
    print(v2, " component_parallel_to ", b2, " is : ", v2.component_parallel_to(b2))

    # Quiz 6
    v = Vector([8.462, 7.893])
    b = Vector([6.984, -5.975])
    v1 = Vector([-8.987, -9.838, 5.031])
    b1 = Vector([-4.268, -1.861, -8.866])
    v2 = Vector([1.5, 9.547, 3.691])
    b2 = Vector([-6.007, 0.124, 5.772])
    print(v, " cross ", b, " is : ", v.cross(b))
    print(v1, " area_of_parallelogram_with ", b1, " is : ", v1.area_of_parallelogram_with(b1))
    print(v2, " area_of_triangle_with ", b2, " is : ", v2.area_of_triangle_with(b2))
