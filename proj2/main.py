from cmath import sin

import numpy as np
from matplotlib import cm

from csolvers import *
import matplotlib.pyplot as plt


def main():
    print(f"{8 * '-'}{6 * '='}Zad B{6 * '='}{8 * '-'}")
    zadB()
    print(f"{8 * '-'}{6 * '='}Zad C{6 * '='}{8 * '-'}")
    zadC()
    print(f"{8 * '-'}{6 * '='}Zad D{6 * '='}{8 * '-'}")
    zadD()
    print(f"{8 * '-'}{6 * '='}Zad E{6 * '='}{8 * '-'}")
    zadE()


def zadB():
    # Zadanie A-B
    # 1 8 4 7 5 6
    a1 = 5 + 7
    a2 = -1
    a3 = a2
    N = 956
    m = string_matrix(N, [a1, a2, a3])
    b = Matrix([[sin(n * (4 + 1)).real] for n in range(1, N + 1)])

    # Jacobi
    start = time.time()
    x, ress = jacobi(m, b)
    print(f"Jacobi:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")

    # Gauss-Seidel
    start = time.time()
    x, ress = gauss(m, b)
    print(f"Gauss-Seidel:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")


def zadC():
    # Zadanie C
    a1 = 3
    a2 = -1
    a3 = a2
    N = 956
    m = string_matrix(N, [a1, a2, a3])
    b = Matrix([[sin(n * (4 + 1)).real] for n in range(1, N + 1)])

    # Jacobi
    start = time.time()
    try:
        x, ress = jacobi(m, b)
        print(f"Jacobi:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")
    except (TimeoutError, OverflowError):
        print("Could not solve using Jacobi method!")

    # Gauss-Seidel
    start = time.time()
    try:
        x, ress = gauss(m, b)
        print(f"Gauss-Seidel:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")
    except (TimeoutError, OverflowError):
        print("Could not solve using Gauss-Seidel method!")


def zadD():
    # Zadanie C
    a1 = 3
    a2 = -1
    a3 = a2
    N = 95
    m = string_matrix(N, [a1, a2, a3])
    b = Matrix([[sin(n * (4 + 1)).real] for n in range(1, N + 1)])

    # LU
    start = time.time()
    try:
        x = lu(m, b)
        print(f"LU: \n\ttime: {time.time() - start}\n\tresiduum norm: {norm(residuum(m, x, b))}")
    except (TimeoutError, OverflowError):
        print("Could not solve using LU method!")


def zadE():
    jacobi_data = ([], [])
    gauss_data = ([], [])
    lu_data = ([], [])
    Ns = [100, 500, 1000, 2000, 3000]

    a1 = 5 + 7
    a2 = -1
    a3 = a2
    for N in Ns:
        m = string_matrix(N, [a1, a2, a3])
        b = Matrix([[sin(n * (4 + 1)).real] for n in range(1, N + 1)])

        # Jacobi
        start = time.time()
        x, ress = jacobi(m, b)
        jacobi_data[0].append(time.time() - start)
        jacobi_data[1].append(ress)
        print(f"Jacobi:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")

        # Gauss-Seidel
        start = time.time()
        x, ress = gauss(m, b)
        gauss_data[0].append(time.time() - start)
        gauss_data[1].append(ress)
        print(f"Gauss-Seidel:\n\titerations: {len(ress)} \n\ttime: {time.time() - start}")

        # LU
        start = time.time()
        x = lu(m, b)
        lu_data[0].append(time.time() - start)
        print(f"LU:\n\ttime: {time.time() - start}")

    # Plots
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(Ns, jacobi_data[0], label="Jacobi")
    ax.plot(Ns, gauss_data[0], label="Gauss-Seidel")
    ax.plot(Ns, lu_data[0], label="LU")
    ax.legend()
    ax.set_xlabel("N")
    ax.set_ylabel("Czas [s]")
    ax.grid()
    fig.savefig('time.png', dpi=300)

    # Compare Jacobi and Gauss
    l_max = len(max(jacobi_data[1], key=len))
    ress_arr_j = [[l[min(x, len(l) - 1)] for x in range(l_max)] for l in jacobi_data[1]]
    ress_arr_g = [[l[min(x, len(l) - 1)] for x in range(l_max)] for l in gauss_data[1]]
    x, y = np.meshgrid(np.arange(l_max), Ns)

    fig = plt.figure(figsize=plt.figaspect(0.5))

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(x, y, np.array(ress_arr_j), rstride=1, cstride=1, cmap=cm.coolwarm,
                     linewidth=0, antialiased=True)
    ax1.set_xlabel("Iteracje")
    ax1.set_ylabel("N")
    ax1.set_zlabel("Norma residuum")
    ax1.set_title("Metoda Jacobiego")

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot_surface(x, y, np.array(ress_arr_g), rstride=1, cstride=1, cmap=cm.coolwarm,
                     linewidth=0, antialiased=True)
    ax2.set_xlabel("Iteracje")
    ax2.set_ylabel("N")
    ax2.set_zlabel("Norma residuum")
    ax2.set_title("Metoda Gaussa-Seidla")

    fig.show()
    fig.savefig('ress.png', dpi=300)


if __name__ == '__main__':
    main()
