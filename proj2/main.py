from cmath import sin

from solvers import *


def main():
    # Zadanie A
    # 1 8 4 7 5 6
    # a1 = 5 + 7
    # a2 = -1
    # a3 = a2
    # N = 956
    a1 = 3
    a2 = -1
    a3 = a2
    N = 10
    m = string_matrix(N, [a1, a2, a3])
    # We start from 0 so sin(n+1)
    b = Matrix([[sin(n * (4 + 1)).real] for n in range(1, N + 1)])

    # Jacobi
    start = time.time()
    x, ress = jacobi(m, b)
    print(f"jacobi: iterations:{len(ress)} time:{time.time() - start}")

    start = time.time()
    x = lu(m, b)
    print(f"LU: time:{time.time() - start}")


if __name__ == '__main__':
    main()
