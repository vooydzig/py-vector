from vector.base import VectorBase


class Vector2(VectorBase):
    x: float
    y: float

    dimensions = ['x', 'y']

    @classmethod
    def unit_x(cls):
        return cls(1, 0)

    @classmethod
    def unit_y(cls):
        return cls(0, 1)
