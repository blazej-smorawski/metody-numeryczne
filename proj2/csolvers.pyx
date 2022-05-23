import time
from cmath import sqrt

from matrix import *

def lu(m: Matrix, b: Matrix) -> Matrix:
    l, u = lu_factorization(m)
    y = forward_substitution(l, b)
    x = backward_substitution(u, y)

    return x

def jacobi(m: Matrix, b: Matrix) -> tuple[Matrix, list[float]]:
    # Data for timing out if necessary
    timeout: float = 3600
    start: float = time.time()

    # Algorithm
    ress = []
    r = Matrix(b.size)
    r.fill(1)
    D = diagonal_matrix(m.diagonal())
    L = m.lower_triangle() - D
    U = m.upper_triangle() - D

    while True:
        res = residuum(m, r, b)
        res_norm = norm(res)
        ress.append(res_norm)
        if res_norm <= pow(10, -9):
            break
        else:
            r = (forward_substitution(D, (L + U) * r) * -1) + forward_substitution(D, b)
        elapsed: float = time.time()
        if elapsed - start > timeout:
            raise TimeoutError()
    return r, ress

def gauss(m: Matrix, b: Matrix) -> tuple[Matrix, list[float]]:
    # Data for timing out if necessary
    timeout: float = 3600
    start: float = time.time()

    # Algorithm
    ress = []
    r = Matrix(b.size)
    r.fill(1)
    D = diagonal_matrix(m.diagonal())
    L = m.lower_triangle() - D
    U = m.upper_triangle() - D

    while True:
        res = residuum(m, r, b)
        res_norm = norm(res)
        ress.append(res_norm)
        if res_norm <= pow(10, -9):
            break
        else:
            r = (forward_substitution(D + L, U * r) * -1) + forward_substitution(D + L, b)
        elapsed: float = time.time()
        if elapsed - start > timeout:
            raise TimeoutError()
    return r, ress

def residuum(m: Matrix, r: Matrix, b: Matrix) -> Matrix:
    return m * r - b

def norm(v: Matrix) -> float:
    sum = 0
    for row in range(v.size[0]):
        sum += pow(v[row, 1], 2)
    return sqrt(sum).real

def lu_factorization(m: Matrix):
    u = m.copy()
    l = identity(m.size[0])
    for k in range(1, m.size[0]):
        for j in range(k + 1, m.size[0] + 1):
            l[j, k] = u[j, k] / u[k, k]
            for x in range(k, m.size[0] + 1):
                u[j, x] = u[j, x] - l[j, k] * u[k, x]
    return l, u

def forward_substitution(m: Matrix, b: Matrix) -> Matrix:
    x = b.create(b.size)  # xs vector has the same shape as b vector
    # Matrix MUST be a lower triangular
    x[1] = b[1] / m[1, 1]
    for row in range(2, m.size[0] + 1):
        # We start from the second row and go to the last one
        sum = b[row]
        for col in range(1, row):
            sum -= x[col] * m[row, col]
        x[row] = sum / m[row, row]
    return x

def backward_substitution(m: Matrix, b: Matrix) -> Matrix:
    x = b.create(b.size)  # xs vector has the same shape as b vector
    # Matrix MUST be a lower triangular
    x[m.size[0]] = b[m.size[0]] / m[m.size[0], m.size[0]]
    for row in range(m.size[0] - 1, 0, -1):
        # We start from the second row and go to the last one
        sum = b[row]
        for col in range(m.size[0], row, -1):
            sum -= x[col] * m[row, col]
        x[row] = sum / m[row, row]
    return x
