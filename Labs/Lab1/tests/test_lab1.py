"""Tests unitaires des fonctions du Lab 1."""

import pytest

from lab1.functions import is_unique, triangle_shape


@pytest.mark.parametrize(
    "x, expected",
    [
        ([], True),
        ([1], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 2, 3, 4, 1], False),
        ([0, 0], False),
        (["a", "b", "a"], False),
        ([1, 1.0], False),  # 1 == 1.0 : doublon au sens de l'égalité
    ],
)
def test_is_unique(x, expected):
    assert is_unique(x) is expected


def test_is_unique_unhashable():
    with pytest.raises(TypeError):
        is_unique([[1, 2], [1, 2]])


def test_triangle_shape_zero():
    assert triangle_shape(0) == ""


def test_triangle_shape_one():
    assert triangle_shape(1) == "x"


def test_triangle_shape_three():
    expected = "\n".join(["  x  ", " xxx ", "xxxxx"])
    assert triangle_shape(3) == expected


@pytest.mark.parametrize("height", [1, 2, 3, 4, 5, 6])
def test_triangle_shape_geometry(height):
    lines = triangle_shape(height).split("\n")
    # une ligne par niveau, toutes de même longueur
    assert len(lines) == height
    assert all(len(line) == 2 * height - 1 for line in lines)
    # nombre de "x" croissant impair, et triangle centré
    for i, line in enumerate(lines):
        assert line.count("x") == 2 * i + 1
        assert line == line.strip().center(2 * height - 1)
