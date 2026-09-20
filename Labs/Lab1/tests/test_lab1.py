import pytest

from src.lab1.functions import (
    string_in_keys,
    make_fiz_buzz,
    describe_price,
    is_unique,
    triangle_shape,
    usefulness,
)

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


class TestStringInKeys:
    def test_existing_key(self):
        assert string_in_keys({"a": 1, "b": 2}, "a") is None

    def test_missing_key(self):
        assert string_in_keys({"a": 1, "b": 2}, "z") == 123

    def test_empty_dictionary(self):
        assert string_in_keys({}, "a") == 123

    def test_single_key(self):
        assert string_in_keys({"a": 1}, "a") is None

    def test_key_with_none_value(self):
        assert string_in_keys({"a": None}, "a") is None

class TestMakeFizBuzz:
    def test_empty_list(self): assert make_fiz_buzz([]) == []
    def test_number_divisible_by_5_only(self): assert make_fiz_buzz([5]) == ["fiz"]
    def test_number_divisible_by_7_only(self): assert make_fiz_buzz([7]) == ["buz"]
    def test_number_divisible_by_5_and_7(self): assert make_fiz_buzz([35]) == ["fizbuz"]
    def test_number_divisible_by_neither(self): assert make_fiz_buzz([1]) == [0]
    def test_multiple_numbers(self): assert make_fiz_buzz([2, 5, 7, 35, 11]) == [ 0, "fiz", "buz", "fizbuz", 4, ]
    def test_zero(self): assert make_fiz_buzz([0]) == ["fizbuz"]
    def test_negative_numbers(self): assert make_fiz_buzz([-5, -7, -35, -1]) == [ "fiz", "buz", "fizbuz", 3, ]
    def test_original_index_is_returned(self): assert make_fiz_buzz([1, 2, 3]) == [0, 1, 2]


class TestUsefulness:
    def test_maths(self, capsys):
        result = usefulness("maths")

        captured = capsys.readouterr()

        assert result is None
        assert captured.out == "That is very useful!\n"

    def test_python(self, capsys):
        result = usefulness("python")

        captured = capsys.readouterr()

        assert result is None
        assert captured.out == "That is very useful!\n"

    def test_meditation(self, capsys):
        result = usefulness("meditation")

        captured = capsys.readouterr()

        assert result is None
        assert captured.out == "How nice\n"

    def test_magic(self, capsys):
        result = usefulness("magic")

        captured = capsys.readouterr()

        assert result is None
        assert captured.out == "You're not at Hogwarts\n"

    def test_unknown_course(self, capsys):
        result = usefulness("history")

        captured = capsys.readouterr()

        assert result is None
        assert captured.out == "What is this COURSE?\n"