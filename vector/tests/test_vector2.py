import math

import pytest

from vector.vector2 import Vector2


def test_can_create():
    v = Vector2(0, 0)
    assert v.x == 0
    assert v.y == 0


def test_can_create_from_collections():
    v = Vector2([0, 0])
    assert v.x == 0
    assert v.y == 0

    v = Vector2((0, 0))
    assert v.x == 0
    assert v.y == 0


def test_can_update_coordinates():
    v = Vector2(0, 0)
    v.x = 1
    v.y = 2

    assert v.x == 1
    assert v.y == 2


def test_can_compare_vectors():
    v1 = Vector2(0, 0)
    v2 = Vector2(0, 0)
    v3 = Vector2(1, 1)

    assert v1 == v1
    assert v3 == v3
    assert v1 == v2
    assert v2 != v3
    assert v1 != v3


def test_common_intializers():
    assert Vector2.zero() == Vector2(0, 0)
    assert Vector2.one() == Vector2(1, 1)
    assert Vector2.unit_x() == Vector2(1, 0)
    assert Vector2.unit_y() == Vector2(0, 1)


def test_can_invert_Vector2():
    v = Vector2.one()
    assert -v == Vector2(-1, -1)


def test_can_add_vectors():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 2)
    assert v1 + v2 == Vector2(v1.x + v2.x, v1.y + v2.y)


def test_can_substract_vectors():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 2)
    assert v1 - v2 == Vector2(v1.x - v2.x, v1.y - v2.y)


def test_can_multiply_by_number():
    v = Vector2(1, 2)
    assert v * 3 == Vector2(1 * 3, 2 * 3)
    assert 3 * v == Vector2(1 * 3, 2 * 3)


def test_can_divide_by_number():
    v = Vector2(1, 2)
    assert v / 3 == Vector2(1 / 3, 2 / 3)


def test_barycentric():
    pass


def test_catmull_rom():
    expected = {
        0: Vector2(0, 10),
        1: Vector2(10, 10),
        0.25: Vector2(2.03125, 10.9375),
        0.5: Vector2(5, 11.25),
        0.75: Vector2(7.96875, 10.9375),
    }
    for t, exp in expected.items():
        assert Vector2.catmull_rom(
            Vector2(0, 0), Vector2(0, 10), Vector2(10, 10), Vector2(10, 0), t
        ) == exp
    with pytest.raises(ValueError):
        Vector2.catmull_rom(
            Vector2(0, 0), Vector2(0, 10), Vector2(10, 10), Vector2(10, 0), -1)
        Vector2.catmull_rom(
            Vector2(0, 0), Vector2(0, 10), Vector2(10, 10), Vector2(10, 0), 2)


def test_clamp():
    assert Vector2.clamp(Vector2(1, 8), Vector2(3, 3), Vector2(5, 5)) == Vector2(3, 5)


def test_distance():
    p1 = Vector2(1, 3)
    p2 = Vector2(3, 1)
    assert Vector2.distance(p1, p2) == math.sqrt(8)


def test_distance_squared():
    p1 = Vector2(1, 3)
    p2 = Vector2(3, 1)
    assert Vector2.distance_squared(p1, p2) == 8


def test_dot_product():
    v1 = Vector2(1, 2)
    v2 = Vector2(1, 5)
    assert Vector2.dot(v1, v2) == 11


def test_hermite():
    expected = {
        0: Vector2(0.2, 0.2),
        1: Vector2(1, 1),
        0.25: Vector2(0.3671875, 0.353125),
        0.5: Vector2(0.5125, 0.625),
        0.75: Vector2(0.7015625, 0.884375)
    }
    for t, exp in expected.items():
        assert Vector2.hermite(
            Vector2(0.2, 0.2), Vector2(0.8, 0.2), Vector2(1, 1), Vector2(1.5, 0), t
        ) == exp, f"Failed for t={t}"
    with pytest.raises(ValueError):
        Vector2.hermite(
            Vector2(0, 0), Vector2(0, 10), Vector2(10, 10), Vector2(10, 0), -1)
        Vector2.hermite(
            Vector2(0, 0), Vector2(0, 10), Vector2(10, 10), Vector2(10, 0), 2)


def test_lerp():
    expected = {
        0: Vector2(0.0, 0.0),
        1: Vector2(1, 1),
        0.25: Vector2(0.25, 0.25),
        0.5: Vector2(0.5, 0.5),
        0.75: Vector2(0.75, 0.75)
    }
    for t, exp in expected.items():
        assert Vector2.lerp(Vector2(0, 0), Vector2(1, 1), t) == exp, f"Failed for t={t}"
    with pytest.raises(ValueError):
        Vector2.lerp(Vector2(0, 0), Vector2(0, 10), -1)
        Vector2.lerp(Vector2(0, 0), Vector2(0, 10), 2)


def test_max():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 2)
    assert Vector2.max(v1, v2) == Vector2(3, 2)


def test_min():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 2)
    assert Vector2.min(v1, v2) == Vector2(1, 2)


def test_normalize():
    assert Vector2.normalize(Vector2(1, 2)).length() == pytest.approx(1)


def test_reflect():
    v = Vector2(1, 1)
    n = -Vector2.unit_x()
    assert Vector2.reflect(v, n) == Vector2(-1, 1)


def test_smooth_step():
    pass


def test_length_squared():
    assert Vector2.zero().length_squared() == 0
    assert Vector2.unit_x().length_squared() == 1
    assert Vector2.unit_y().length_squared() == 1
    assert Vector2.one().length_squared() == 2
    assert Vector2(1, 2).length_squared() == 1 ** 1 + 2 ** 2


def test_length():
    assert Vector2.zero().length() == 0
    assert Vector2.unit_x().length() == 1
    assert Vector2.unit_y().length() == 1
    assert Vector2.one().length() == math.sqrt(2)
    assert Vector2(1, 2).length() == math.sqrt(1 ** 1 + 2 ** 2)


def test_can_normalize_in_place():
    v = Vector2(1, 2)
    v.normalized()
    assert v.length() == pytest.approx(1)
    assert v.x != 1
    assert v.y != 1
