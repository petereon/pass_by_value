import os
from expycted import expect  # type: ignore
import pytest

from pass_by_value import pass_by_value


class Example:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3


@pytest.fixture
def example_object():
    return Example()


@pytest.fixture
def example_file():
    with open("example.txt", "w") as f:
        f.write("a")
        yield f

    os.remove("example.txt")


def test_mutation_list():
    original: list = [1, 2, 3, 4, 5]

    @pass_by_value
    def mutate(original: list):
        original[2] = "a"

    mutate(original=original)

    expect(original).to.equal([1, 2, 3, 4, 5])


def test_mutation_dict():
    original = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

    @pass_by_value
    def mutate(original: dict):
        original["a"] = "a"
        del original["b"]

    mutate(original)

    expect(original).to.equal({"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})


def test_mutation_set():
    original = {"a", "b", "c", "d", "e"}

    @pass_by_value
    def mutate(original: set):
        original.add("f")
        original.remove("b")

    mutate(original)

    expect(original).to.equal({"a", "b", "c", "d", "e"})


def test_mutation_object(example_object):
    @pass_by_value
    def mutate(example_object: Example):
        example_object.a = "12"
        del example_object.b

    mutate(example_object)

    assert example_object.a == 1
    assert example_object.b == 2
    assert example_object.c == 3


def test_passing_file_handle(example_file):
    @pass_by_value
    def mutate(file):
        file.write("a")

    with pytest.warns(
        UserWarning,
        match="can't be copied, passing by object-reference",
    ):
        mutate(example_file)
