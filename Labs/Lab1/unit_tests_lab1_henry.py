import pytest
# ─────────────────────────────────────────────
# Fonctions extraites du notebook
# ─────────────────────────────────────────────

def string_in_keys(d: dict, s: str):
    if s not in d.keys():
        return 123


def make_fiz_buzz(L: list) -> list:
    fizbee = []
    for i in range(len(L)):
        if L[i] % 5 == 0 and L[i] % 7 == 0:
            fizbee.append("fizbuz")
        elif L[i] % 5 == 0:
            fizbee.append("fiz")
        elif L[i] % 7 == 0:
            fizbee.append("buz")
        else:
            fizbee.append(i)
    return fizbee


def describe_price(fruit: str, quantity: int, price: float) -> str:
    fruit_name = fruit if quantity == 1 else f"{fruit}s"
    verb = "costs" if quantity == 1 else "cost"
    return f"{quantity} {fruit_name} {verb} ${price:.2f}"


def is_unique(x: list) -> bool:
    return len(x) == len(set(x))


def triangle_shape(height: int) -> str:
    if height == 0:
        return ""
    triangle = ""
    for i in range(height):
        stair = " " * (height - i - 1) + "x" * (2 * i + 1) + " " * (height - i - 1) + "\n"
        triangle += stair
    return triangle

# ─────────────────────────────────────────────
# Tests : fonctions
# ─────────────────────────────────────────────

class TestDescribePrice:
    def test_singular(self):
        assert describe_price("avocado", 1, 1.50) == "1 avocado costs $1.50"

    def test_plural(self):
        assert describe_price("avocado", 2, 18912.392) == "2 avocados cost $18912.39"

    def test_rounding(self):
        # arrondi au centime le plus proche
        assert describe_price("mango", 3, 1.999) == "3 mangos cost $2.00"

    def test_notebook_example(self):
        result = describe_price("avocado", 2, 1.8912392e4)
        assert result == "2 avocados cost $18912.39"

    def test_zero_quantity(self):
        # Comportement limite : 0 n'est pas 1, donc pluriel
        result = describe_price("apple", 0, 1.0)
        assert "apples" in result and "cost" in result


class TestIsUnique:
    def test_unique_list(self):
        assert is_unique([1, 2, 3, 4, 5]) is True

    def test_duplicate_list(self):
        assert is_unique([1, 2, 3, 3]) is False

    def test_empty_list(self):
        assert is_unique([]) is True

    def test_single_element(self):
        assert is_unique([42]) is True

    def test_all_same(self):
        assert is_unique([7, 7, 7]) is False

    def test_strings(self):
        assert is_unique(["a", "b", "c"]) is True
        assert is_unique(["a", "b", "a"]) is False


class TestTriangleShape:
    def test_height_0(self):
        assert triangle_shape(0) == ""

    def test_height_1(self):
        assert triangle_shape(1) == "x\n"

    def test_height_2(self):
        expected = " x \nxxx\n"
        assert triangle_shape(2) == expected

    def test_height_3(self):
        expected = "  x  \n xxx \nxxxxx\n"
        assert triangle_shape(3) == expected

    def test_width_grows_correctly(self):
        # Pour une hauteur h, la ligne i a (2i+1) 'x'
        for h in range(1, 6):
            lines = triangle_shape(h).splitlines()
            assert len(lines) == h
            for i, line in enumerate(lines):
                assert line.count("x") == 2 * i + 1

    def test_symmetry(self):
        # Chaque ligne doit être symétrique
        for h in range(1, 6):
            for line in triangle_shape(h).splitlines():
                assert line == line[::-1]

    def test_line_length_constant(self):
        # Toutes les lignes d'un triangle de hauteur h ont la même longueur
        for h in range(1, 6):
            lines = triangle_shape(h).splitlines()
            lengths = [len(l) for l in lines]
            assert len(set(lengths)) == 1
