import math


def clamp_value(a, min, max):
    if a < min:
        return min
    if a > max:
        return max
    return a


class VectorBase:
    dimensions = []

    def __init__(self, *args):
        if not self.dimensions:
            raise ValueError('Dimensions must be specified')
        if len(args) != len(self.dimensions):
            raise ValueError(f'Invalid arguments count. Expected: ({len(self.dimensions)}), received: {len(args)}')
        for d, v in zip(self.dimensions, args):
            setattr(self, d, v)

    def __repr__(self):
        dimensions = " ".join(f"{d}={getattr(self, d)} " for d in self.dimensions)
        return f'{self.__class__.__name__}({dimensions})'

    @classmethod
    def zero(cls):
        return cls(*([0] * len(cls.dimensions)))

    @classmethod
    def one(cls):
        return cls(*([1] * len(cls.dimensions)))

    def __neg__(self):
        return self.__class__(*[-getattr(self, d) for d in self.dimensions])

    def __add__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError
        return self.__class__(*[getattr(self, d) + getattr(other, d) for d in self.dimensions])

    def __sub__(self, other):
        if self.dimensions != other.dimensions:
            raise ValueError
        return self.__class__(*[getattr(self, d) - getattr(other, d) for d in self.dimensions])

    def __mul__(self, other):
        return self.__class__(*[getattr(self, d) * other for d in self.dimensions])

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self.__class__(*[getattr(self, d) / other for d in self.dimensions])

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
    def catmull_rom(p0, p1, p2, p3, t):
        if t < 0 or t > 1:
            raise ValueError
        a = p1 * 2
        b = p2 - p0
        c = p0 * 2 - p1 * 5 + p2 * 4 - p3
        d = -p0 + p1 * 3 - p2 * 3 + p3
        return (a + (b * t) + (c * t ** 2) + (d * t ** 3)) / 2

    @classmethod
    def clamp(cls, v, v_min, v_max):
        args = [
            clamp_value(getattr(v, d), getattr(v_min, d), getattr(v_max, d))
            for d in v.dimensions
        ]
        return cls(*args)

    @staticmethod
    def distance(p1, p2):
        return (p1 - p2).length()

    @staticmethod
    def distance_squared(p1, p2):
        return (p1 - p2).length_squared()

    @staticmethod
    def dot(v1, v2):
        return sum(getattr(v1, d) * getattr(v2, d) for d in v1.dimensions)

    @staticmethod
    def hermite(p1, m1, p2, m2, t):
        if t < 0 or t > 1:
            raise ValueError
        a = 2 * t ** 3 - 3 * t ** 2 + 1
        b = t ** 3 - 2 * t ** 2 + t
        c = -2 * t ** 3 + 3 * t ** 2
        d = t ** 3 - t ** 2
        return p1 * a + m1 * b + p2 * c + m2 * d

    @staticmethod
    def lerp(v1, v2, t):
        if t < 0 or t > 1:
            raise ValueError
        return v1 + (v2 - v1) * t

    @classmethod
    def max(cls, v1, v2):
        args = [max(getattr(v1, d), getattr(v2, d)) for d in v1.dimensions]
        return cls(*args)

    @classmethod
    def min(cls, v1, v2):
        args = [min(getattr(v1, d), getattr(v2, d)) for d in v1.dimensions]
        return cls(*args)

    @staticmethod
    def normalize(v):
        """return new normalized vector"""
        return v / v.length()

    @staticmethod
    def reflect(vector, normal):
        n = vector.normalize(normal)
        dot = vector.dot(vector, n)
        return vector - n * 2 * dot

    @staticmethod
    def smooth_step(v1, v2, amount):
        raise NotImplementedError

    def angle(self, other):
        dot = self.dot(self, other) / (self.length() * other.length())
        dot = clamp_value(dot, -1, 1)
        return float(math.acos(dot))

    def length_squared(self):
        return sum(getattr(self, d) ** 2 for d in self.dimensions)

    def length(self):
        return math.sqrt(self.length_squared())

    def normalized(self):
        la = self.length()
        for d in self.dimensions:
            setattr(self, d, getattr(self, d) / la)
