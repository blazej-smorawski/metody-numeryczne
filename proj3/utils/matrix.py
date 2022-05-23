from __future__ import annotations

import random
import copy


class DimensionError(RuntimeError):
    def __init__(self, message="Dimensions of matrices do not match!"):
        self.message = message
        super().__init__(self.message)


class NonSquareError(RuntimeError):
    def __init__(self, message="Matrix is not square!"):
        self.message = message
        super().__init__(self.message)


class Matrix:
    size: tuple[int, int]
    data: list[list]

    def __init__(self, arg):
        if type(arg) is tuple:
            # allocate an empty matrix by size
            self.size = arg
            # allocation of an array with an appropriate size
            self.data = [[None] * self.size[1] for i in range(self.size[0])]
        elif type(arg) is list:
            # create array using list of rows
            self.size = (len(arg), len(arg[0]))
            self.data = arg

    def __str__(self) -> str:
        horizontal_lines = True  # draw horizontal lines after each row
        cell_size: int = 9  # includes all characters in a cell
        output: str = "┌" + ("─" * (cell_size - 1) + "┬") * (self.size[1] - 1) + ("─" * (cell_size - 1) + "┐") + "\n"
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                output += "│" + f"{self.data[row][col]: .1E}"
            output += "│\n"
            if horizontal_lines and row != self.size[0] - 1:
                output += "├" + ("─" * (cell_size - 1) + "┼") * (self.size[1] - 1) + (
                        "─" * (cell_size - 1) + "┤") + "\n"
        output += "└" + ("─" * (cell_size - 1) + "┴") * (self.size[1] - 1) + ("─" * (cell_size - 1) + "┘")
        return output

    def __getitem__(self, index):
        if type(index) is tuple:
            row, col = index
            return self.data[row - 1][col - 1]
        elif type(index) is int:
            return self.data[index - 1][0]  # We expect vertical vectors

    def __setitem__(self, index, value) -> Matrix:
        if type(index) is tuple:
            row, col = index
            self.data[row - 1][col - 1] = value
        elif type(index) is int:
            self.data[index - 1][0] = value
        return self

    def row(self, index: int) -> list:
        return self.data[index - 1].copy()

    def column(self, index: int) -> list:
        return [self.data[row][index - 1] for row in range(self.size[0])]

    def diagonal(self) -> list:
        if self.size[0] != self.size[1]:
            raise NonSquareError
        return [self.data[index][index] for index in range(self.size[0])]

    def lower_triangle(self) -> Matrix:
        result = Matrix(self.size)
        result.fill(0)
        for row in range(result.size[0]):
            for col in range(row + 1):
                result.data[row][col] = self.data[row][col]
        return result

    def upper_triangle(self) -> Matrix:
        result = Matrix(self.size)
        result.fill(0)
        for row in range(result.size[0]):
            for col in range(row, result.size[1]):
                result.data[row][col] = self.data[row][col]
        return result

    def create(self, size: tuple[int, int]) -> Matrix:
        """
        Method for creating another instance of the Matrix
        created, so solvers can create new matrices without
        any knowledge of the instance of matrix they are using.
        It might be a bad way to do it, but I dunno :)
        """
        return Matrix(size)

    def copy(self) -> Matrix:
        result = Matrix(self.size)
        result.data = copy.deepcopy(self.data)
        return result

    def __add__(self, other) -> Matrix:
        if self.size != other.size:
            raise DimensionError()

        result = Matrix((self.size[0], self.size[1]))

        for row in range(self.size[0]):
            for col in range(self.size[1]):
                result.data[row][col] = self.data[row][col] + other.data[row][col]
        return result

    def __sub__(self, other):
        if self.size != other.size:
            raise DimensionError()

        result = Matrix((self.size[0], self.size[1]))

        for row in range(self.size[0]):
            for col in range(self.size[1]):
                result.data[row][col] = self.data[row][col] - other.data[row][col]
        return result

    def __mul__(self, other) -> Matrix:
        # Multiply number * matrix
        if type(other) is float or type(other) is int:
            result = self.copy()
            for row in range(result.size[0]):
                for col in range(result.size[1]):
                    result.data[row][col] *= other
            return result

        # Multiply matrix * matrix
        if self.size[1] != other.size[0]:
            raise DimensionError()

        result = Matrix((self.size[0], other.size[1]))

        for row in range(result.size[0]):
            for col in range(result.size[1]):
                result.data[row][col] = 0
                for x in range(self.size[1]):
                    # iterate over elements summing into result[col, row]
                    result.data[row][col] += self.data[row][x] * other.data[x][col]
        return result

    def fill(self, value) -> Matrix:
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                self.data[row][col] = value
        return self


def identity(size: int) -> Matrix:
    result = Matrix((size, size))
    result.fill(0)
    for index in range(size):
        result.data[index][index] = 1
    return result


def diagonal_matrix(diagonal: list) -> Matrix:
    result = Matrix((len(diagonal), len(diagonal)))
    result.fill(0)
    for index in range(result.size[0]):
        result.data[index][index] = diagonal[index]
    return result


def random_matrix(size: tuple[int, int], r: tuple[float, float] = (0, 1000000)) -> Matrix:
    result = Matrix(size)
    for row in range(result.size[0]):
        for col in range(result.size[1]):
            result.data[row][col] = random.uniform(float(r[0]), float(r[1]))
    return result


def string_matrix(size: int, elements: list) -> Matrix:
    result = Matrix((size, size))
    result.fill(0)
    for row in range(result.size[0]):
        # Go right
        for col in range(row, min(row + len(elements), result.size[1])):
            result.data[row][col] = elements[col - row]
        # Go left
        counter: int = 1
        col: int = row - 1
        while col >= 0 and counter < len(elements):
            result.data[row][col] = elements[counter]
            col -= 1
            counter += 1
    return result
