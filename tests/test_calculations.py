from app.calculation import add, BankAccount
import pytest


@pytest.mark.parametrize(
    "num1, num2, expected", [(1, 2, 3), (100008, 100009, 200017), (-1, -1, -2)]
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected
