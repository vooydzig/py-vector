from vector.base import VectorBase


class Vector3(VectorBase):
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
    def cross(v1, v2):
        return Vector3(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )
