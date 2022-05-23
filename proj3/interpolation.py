from functools import *
from utils import *
from utils.matrix import Matrix
from utils.solvers import lu_p


def _list_without(xs, i):
    xs_copy = xs.copy()
    xs_copy.remove(xs[i])
    return xs_copy


def _lagrange_base(xs, i):
    return lambda x: reduce(lambda a, b: a * b, map(lambda y: x - y, _list_without(xs, i)), 1) \
                     / reduce(lambda a, b: a * b, map(lambda y: xs[i] - y, _list_without(xs, i)), 1)


def lagrange(xs, ys):
    return lambda x: sum([_lagrange_base(xs, i)(x) * ys[i] for i in range(len(xs))])


def _spline(xs, a, x):
    for i in range(1, len(xs)):
        if x < xs[i]:
            return a[1 + 4 * (i - 1)] + a[2 + 4 * (i - 1)] * (x - xs[i - 1]) + a[3 + 4 * (i - 1)] * (
                        x - xs[i - 1]) ** 2 + a[
                       4 + 4 * (i - 1)] * (x - xs[i - 1]) ** 3


def spline(xs, ys):
    n = len(xs) - 1
    m = Matrix((n * 4, n * 4))
    r = Matrix((n * 4, 1))
    m.fill(0)
    r.fill(0)

    a = 1
    b = 2
    c = 3
    d = 4

    # Sj(xj)=f(xj)
    for j in range(0, n):  # j=<0,n-1>
        m[j + 1, a + j * 4] = 1  # a*1+...
        r[j + 1] = ys[j]

    # Sj(xj+1)=f(xj+1)
    off = n
    for j in range(0, n):
        m[j + 1 + off, a + j * 4] = 1  # a*1+...
        m[j + 1 + off, b + j * 4] = xs[j + 1] - xs[j]  # ...+b*(xj+1-xj)+...
        m[j + 1 + off, c + j * 4] = m[j + 1 + off, b + j * 4] ** 2  # ...+c*(xj+1-xj)^2+...
        m[j + 1 + off, d + j * 4] = m[j + 1 + off, b + j * 4] ** 3  # ...+d*(xj+1-xj)^3+...
        r[j + 1 + off] = ys[j + 1]

    # S'j-1(xj)=S'j(xj)
    off += n
    for j in range(1, n):
        m[j + off, b + (j - 1) * 4] = 1
        m[j + off, c + (j - 1) * 4] = 2 * (xs[j] - xs[j - 1])
        m[j + off, d + (j - 1) * 4] = 3 * (xs[j] - xs[j - 1]) ** 2
        m[j + off, b + j * 4] = -1
        r[j + off] = 0

    # S''j-1(xj)=S''j(xj)
    off += n - 1
    for j in range(1, n):
        m[j + off, c + (j - 1) * 4] = 2
        m[j + off, d + (j - 1) * 4] = 6 * (xs[j] - xs[j - 1])
        m[j + off, c + j * 4] = -2
        r[j + off] = 0

    off += n - 1
    # S''0(x0)=0
    m[1 + off, c] = 2
    r[1 + off] = 0

    # S''n-1(xn)=0
    m[2 + off, c + (n - 1) * 4] = 2
    m[2 + off, d + (n - 1) * 4] = 6 * (xs[n] - xs[n - 1])
    r[2 + off] = 0

    a = lu_p(m, r)
    return lambda x: _spline(xs, a, x)
