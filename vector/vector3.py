from vector.base import VectorBase


class Vector3(VectorBase):
    x: float
    y: float
    z: float
    dimensions = ['x', 'y', 'z']

    @classmethod
    def unit_x(cls):
        return cls(1, 0, 0)

    @classmethod
    def unit_y(cls):
        return cls(0, 1, 0)

    @classmethod
    def unit_z(cls):
        return cls(0, 0, 1)

    @staticmethod
    def cross(vector1, vector2):
        return Vector3(
            vector1.y * vector2.z - vector1.z * vector2.y,
            vector1.z * vector2.x - vector1.x * vector2.z,
            vector1.x * vector2.y - vector1.y * vector2.x
        )
