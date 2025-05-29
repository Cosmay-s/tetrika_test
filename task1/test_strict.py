import pytest
from solution import strict


@strict
def accepts_bool(x: bool) -> bool:
    return x


@strict
def accepts_int(x: int) -> int:
    return x

@strict
def accepts_float(x: float) -> float:
    return x


@strict
def accepts_str(x: str) -> str:
    return x


@strict
def accepts_multiple(a: int, b: float, c: bool, d: str):
    return (a, b, c, d)


def test_accepts_bool_with_bool_passes():
    assert accepts_bool(True) is True
    assert accepts_bool(False) is False


def test_accepts_bool_with_wrong_type_raises():
    with pytest.raises(TypeError):
        accepts_bool(1)
    with pytest.raises(TypeError):
        accepts_bool("True")


def test_accepts_int_with_int_passes():
    assert accepts_int(42) == 42


def test_accepts_int_with_wrong_type_raises():
    with pytest.raises(TypeError):
        accepts_int(42.0)
    with pytest.raises(TypeError):
        accepts_int("42")


def test_accepts_float_with_float_passes():
    assert accepts_float(3.14) == 3.14


def test_accepts_float_with_wrong_type_raises():
    with pytest.raises(TypeError):
        accepts_float(3)
    with pytest.raises(TypeError):
        accepts_float("3.14")


def test_accepts_str_with_str_passes():
    assert accepts_str("hello") == "hello"


def test_accepts_str_with_wrong_type_raises():
    with pytest.raises(TypeError):
        accepts_str(123)
    with pytest.raises(TypeError):
        accepts_str(True)


def test_accepts_multiple_correct_types_positional():
    assert accepts_multiple(1, 2.5, True, "test") == (1, 2.5, True, "test")


def test_accepts_multiple_correct_types_named():
    assert accepts_multiple(a=10, b=5.5, c=False, d="abc") == (10, 5.5, False, "abc")


def test_accepts_multiple_mixed_args():
    assert accepts_multiple(7, b=8.8, c=True, d="xyz") == (7, 8.8, True, "xyz")


def test_accepts_multiple_wrong_types_raise():
    with pytest.raises(TypeError):
        accepts_multiple("1", 2.5, True, "test")
    with pytest.raises(TypeError):
        accepts_multiple(1, "2.5", True, "test")
    with pytest.raises(TypeError):
        accepts_multiple(1, 2.5, "True", "test")
        accepts_multiple(1, 2.5, True, 100)
