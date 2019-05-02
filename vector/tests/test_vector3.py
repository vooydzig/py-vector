import math

import pytest

from vector.vector3 import Vector3


def test_can_create():
    v = Vector3(0, 0, 0)
    assert v.x == 0
    assert v.y == 0
    assert v.z == 0


def test_can_create_from_collections():
    v = Vector3([0, 0, 0])
    assert v.x == 0
    assert v.y == 0
    assert v.z == 0

    v = Vector3((0, 0, 0))
    assert v.x == 0
    assert v.y == 0
    assert v.z == 0


def test_can_update_coordinates():
    v = Vector3(0, 0, 0)
    v.x = 1
    v.y = 2
    v.z = 3

    assert v.x == 1
    assert v.y == 2
    assert v.z == 3


def test_can_compare_vectors():
    v1 = Vector3(0, 0, 0)
    v2 = Vector3(0, 0, 0)
    v3 = Vector3(1, 1, 1)

    assert v1 == v1
    assert v3 == v3
    assert v1 == v2
    assert v2 != v3
    assert v1 != v3


def test_common_intializers():
    assert Vector3.zero() == Vector3(0, 0, 0)
    assert Vector3.one() == Vector3(1, 1, 1)
    assert Vector3.unit_x() == Vector3(1, 0, 0)
    assert Vector3.unit_y() == Vector3(0, 1, 0)
    assert Vector3.unit_z() == Vector3(0, 0, 1)


def test_can_invert_vector3():
    v = Vector3.one()
    assert -v == Vector3(-1, -1, -1)


def test_can_add_vectors():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(3, 2, 1)
    assert v1 + v2 == Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)


def test_can_substract_vectors():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(3, 2, 1)
    assert v1 - v2 == Vector3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)


def test_can_multiply_by_number():
    v = Vector3(1, 2, 3)
    assert v * 3 == Vector3(1 * 3, 2 * 3, 3 * 3)
    assert 3 * v == Vector3(1 * 3, 2 * 3, 3 * 3)


def test_can_divide_by_number():
    v = Vector3(1, 2, 3)
    assert v / 3 == Vector3(1 / 3, 2 / 3, 3 / 3)


def test_barycentric():
    pass


def test_catmull_rom():
    expected = {
        0: Vector3(0, 10, 0),
        1: Vector3(10, 10, 0),
        0.25: Vector3(2.03125, 10.9375, 0),
        0.5: Vector3(5, 11.25, 0),
        0.75: Vector3(7.96875, 10.9375, 0)
    }
    for t, exp in expected.items():
        assert Vector3.catmull_rom(
            Vector3(0, 0, 0), Vector3(0, 10, 0), Vector3(10, 10, 0), Vector3(10, 0, 0), t
        ) == exp
    with pytest.raises(ValueError):
        Vector3.catmull_rom(
            Vector3(0, 0, 0), Vector3(0, 10, 0), Vector3(10, 10, 0), Vector3(10, 0, 0), -1)
        Vector3.catmull_rom(
            Vector3(0, 0, 0), Vector3(0, 10, 0), Vector3(10, 10, 0), Vector3(10, 0, 0), 2)


def test_clamp():
    assert Vector3.clamp(Vector3(1, 2, 3), Vector3(0, 3, 0), Vector3(5, 5, 2)) == Vector3(1, 3, 2)


def test_cross():
    assert Vector3.cross(Vector3.unit_x(), Vector3.unit_y()) == Vector3.unit_z()
    assert Vector3.cross(Vector3(1, 0, 1), Vector3.unit_y()) == Vector3(-1, 0, 1)
    assert Vector3.cross(Vector3(1, 2, 3), Vector3(3, 2, 1)) == Vector3(-4, 8, -4)


def test_distance():
    p1 = Vector3(1, 2, 3)
    p2 = Vector3(3, 2, 1)
    assert Vector3.distance(p1, p2) == math.sqrt(8)


def test_distance_squared():
    p1 = Vector3(1, 2, 3)
    p2 = Vector3(3, 2, 1)
    assert Vector3.distance_squared(p1, p2) == 8


def test_dot_product():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(1, 5, 7)
    assert Vector3.dot(v1, v2) == 32


def test_hermite():
    expected = {
        0: Vector3(0.2, 0.2, 0),
        1: Vector3(1, 1, 0),
        0.25: Vector3(0.3671875, 0.353125, 0),
        0.5: Vector3(0.5125, 0.625, 0),
        0.75: Vector3(0.7015625, 0.884375, 0)
    }
    for t, exp in expected.items():
        assert Vector3.hermite(
            Vector3(0.2, 0.2, 0), Vector3(0.8, 0.2, 0), Vector3(1, 1, 0), Vector3(1.5, 0, 0), t
        ) == exp, f"Failed for t={t}"
    with pytest.raises(ValueError):
        Vector3.hermite(
            Vector3(0, 0, 0), Vector3(0, 10, 0), Vector3(10, 10, 0), Vector3(10, 0, 0), -1)
        Vector3.hermite(
            Vector3(0, 0, 0), Vector3(0, 10, 0), Vector3(10, 10, 0), Vector3(10, 0, 0), 2)


def test_lerp():
    expected = {
        0: Vector3(0.0, 0.0, 0),
        1: Vector3(1, 1, 0),
        0.25: Vector3(0.25, 0.25, 0),
        0.5: Vector3(0.5, 0.5, 0),
        0.75: Vector3(0.75, 0.75, 0)
    }
    for t, exp in expected.items():
        assert Vector3.lerp(Vector3(0, 0, 0), Vector3(1, 1, 0), t) == exp, f"Failed for t={t}"
    with pytest.raises(ValueError):
        Vector3.lerp(Vector3(0, 0, 0), Vector3(0, 10, 0), -1)
        Vector3.lerp(Vector3(0, 0, 0), Vector3(0, 10, 0), 2)


def test_max():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(3, 2, 1)
    assert Vector3.max(v1, v2) == Vector3(3, 2, 3)


def test_min():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(3, 2, 1)
    assert Vector3.min(v1, v2) == Vector3(1, 2, 1)


def test_normalize():
    assert Vector3.normalize(Vector3(1, 2, 3)).length() == pytest.approx(1)


def test_reflect():
    v = Vector3(1, 1, 0)
    n = -Vector3.unit_x()
    assert Vector3.reflect(v, n) == Vector3(-1, 1, 0)


def test_smooth_step():
    pass


def test_length_squared():
    assert Vector3.zero().length_squared() == 0
    assert Vector3.unit_x().length_squared() == 1
    assert Vector3.unit_y().length_squared() == 1
    assert Vector3.unit_z().length_squared() == 1
    assert Vector3.one().length_squared() == 3
    assert Vector3(1, 2, 3).length_squared() == 1 ** 1 + 2 ** 2 + 3 ** 2


def test_length():
    assert Vector3.zero().length() == 0
    assert Vector3.unit_x().length() == 1
    assert Vector3.unit_y().length() == 1
    assert Vector3.unit_z().length() == 1
    assert Vector3.one().length() == math.sqrt(3)
    assert Vector3(1, 2, 3).length() == math.sqrt(1 ** 1 + 2 ** 2 + 3 ** 2)


def test_can_normalize_in_place():
    v = Vector3(1, 2, 3)
    v.normalized()
    assert v.length() == pytest.approx(1)


def test_can_get_angle_between_two_vectors():
    v1 = Vector3.unit_x()
    v2 = Vector3.unit_y()
    assert v1.angle(v1) == 0
    assert v1.angle(v2) == pytest.approx(math.pi / 2)
