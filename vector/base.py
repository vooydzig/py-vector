import math


def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


class VectorBase:
    dimensions = []

    def __init__(self, *args):
        values = args
        if not self.dimensions:
            raise ValueError('Dimensions must be specified')
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            values = args[0]
        elif len(args) != len(self.dimensions):
            raise ValueError(f'Invalid arguments count. Expected: ({len(self.dimensions)}), received: {len(args)}')
        for d, v in zip(self.dimensions, values):
            setattr(self, d, v)

    def __repr__(self):
        dimensions_repr = " ".join(f"{d}={getattr(self, d)} " for d in self.dimensions)
        return f'{self.__class__.__name__}({dimensions_repr})'

    @classmethod
    def zero(cls):
        return cls(*([0] * len(cls.dimensions)))

    @classmethod
    def one(cls):
        return cls(*([1] * len(cls.dimensions)))

    def __neg__(self):
        return self.__class__([-getattr(self, d) for d in self.dimensions])

    def __add__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError
        return self.__class__([getattr(self, d) + getattr(other, d) for d in self.dimensions])

    def __sub__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError
        return self.__class__([getattr(self, d) - getattr(other, d) for d in self.dimensions])

    def __mul__(self, scalar):
        return self.__class__([getattr(self, d) * scalar for d in self.dimensions])

    def __rmul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        return self.__class__([getattr(self, d) / scalar for d in self.dimensions])

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        if self.dimensions != other.dimensions:
            return False
        return all(getattr(self, d) == getattr(other, d) for d in self.dimensions)

    @staticmethod
    def barycentric(p1, p2, p3):
        raise NotImplementedError

    @staticmethod
    def catmull_rom(p0, p1, p2, p3, amount):
        if amount < 0 or amount > 1:
            raise ValueError
        a = p1 * 2
        b = p2 - p0
        c = p0 * 2 - p1 * 5 + p2 * 4 - p3
        d = -p0 + p1 * 3 - p2 * 3 + p3
        return (a + (b * amount) + (c * amount ** 2) + (d * amount ** 3)) / 2

    @classmethod
    def clamp(cls, vector, min, max):
        args = [
            clamp(getattr(vector, d), getattr(min, d), getattr(max, d))
            for d in vector.dimensions
        ]
        return cls(*args)

    @staticmethod
    def distance(point1, point2):
        return (point1 - point2).length()

    @staticmethod
    def distance_squared(point1, point2):
        return (point1 - point2).length_squared()

    @staticmethod
    def dot(vector1, vector2):
        return sum(getattr(vector1, d) * getattr(vector2, d) for d in vector1.dimensions)

    @staticmethod
    def hermite(point1, tangent1, point2, tangent2, amount):
        if amount < 0 or amount > 1:
            raise ValueError
        a = 2 * amount ** 3 - 3 * amount ** 2 + 1
        b = amount ** 3 - 2 * amount ** 2 + amount
        c = -2 * amount ** 3 + 3 * amount ** 2
        d = amount ** 3 - amount ** 2
        return point1 * a + tangent1 * b + point2 * c + tangent2 * d

    @staticmethod
    def lerp(vector1, vector2, amount):
        if amount < 0 or amount > 1:
            raise ValueError
        return vector1 + (vector2 - vector1) * amount

    @classmethod
    def max(cls, vector1, vector2):
        return cls([max(getattr(vector1, d), getattr(vector2, d)) for d in vector1.dimensions])

    @classmethod
    def min(cls, vector1, vector2):
        return cls([min(getattr(vector1, d), getattr(vector2, d)) for d in vector1.dimensions])

    @staticmethod
    def normalize(vector):
        """return new normalized vector"""
        return vector / vector.length()

    @staticmethod
    def reflect(vector, normal):
        n = vector.normalize(normal)
        dot = vector.dot(vector, n)
        return vector - n * 2 * dot

    @staticmethod
    def smooth_step(vector1, vector2, amount):
        raise NotImplementedError

    def angle(self, other):
        dot = self.dot(self, other) / (self.length() * other.length())
        dot = clamp(dot, -1, 1)
        return float(math.acos(dot))

    def length_squared(self):
        return sum(getattr(self, d) ** 2 for d in self.dimensions)

    def length(self):
        return math.sqrt(self.length_squared())

    def normalized(self):
        l = self.length()
        for d in self.dimensions:
            setattr(self, d, getattr(self, d) / l)
