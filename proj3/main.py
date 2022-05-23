import random

import numpy as np
from scipy import stats
from matplotlib import rcParams

rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = ['Computer Modern']
from matplotlib import pyplot as plt
from interpolation import *


def get_elevation(name):
    return np.loadtxt("elevation/" + name + ".csv", delimiter=',')


def get_even_samples(arr, n):
    idx = np.round(np.linspace(0, len(arr) - 1, n)).astype(int)
    return arr[idx].tolist()


def main():
    gda = get_elevation("SpacerniakGdansk")
    eve = get_elevation("MountEverest")
    kol = get_elevation("WielkiKanionKolorado")
    elevation_data = [gda, eve, kol]
    names = ["Spacerniak Gdansk", "Mount Everest", "Wielki Kanion Kolorado"]

    # plot_interpolation(elevation_data, names, lagrange, "Lagrange")
    # plot_interpolation(elevation_data, names, spline, "spline")

    plot_distribution(kol, spline, "spline", [linear_dist, norm_dist, beta_dist],
                      ["Rozkład liniowy", "Rozkład normalny", "Rozkład beta (beta=alfa=0.5)"])
    plot_distribution(kol, lagrange, "Lagrange", [linear_dist, norm_dist, beta_dist],
                      ["Rozkład liniowy", "Rozkład normalny", "Rozkład beta (beta=alfa=0.5)"])


def plot_interpolation(elevation_data, names, interp, interp_name):
    # Zależność od N
    for index in range(len(elevation_data)):
        fig, axs = plt.subplots(5, 1, sharex='col')
        fig.subplots_adjust(hspace=.2, wspace=.1)
        fig.set_size_inches(8, 11.5)
        axs = axs.ravel()
        for n in range(5):
            xs = get_even_samples(elevation_data[index][:, 0], 2 ** (n + 1))
            ys = get_even_samples(elevation_data[index][:, 1], 2 ** (n + 1))

            xsn = np.linspace(min(xs), max(xs), 10000)
            i = interp(xs, ys)
            print(f"n: {n}")
            axs[n].scatter(xs, ys, s=4)
            axs[n].plot(xsn, [i(x) for x in xsn], label="Interpolacja " + interp_name, alpha=1)
            axs[n].plot(elevation_data[index][:, 0], elevation_data[index][:, 1], label="Funkcja interpolowana",
                        alpha=0.5)
            axs[n].grid()
            axs[n].autoscale()
            axs[n].set_title(f"N={len(xs)}")
            axs[n].set_ylabel("Y[m]")
            if n == 4:
                axs[n].set_xlabel("X[m]")
        plt.legend()
        plt.savefig("plots/n/" + names[index] + " " + interp_name + ".png", dpi=600)


def linear_dist(arr, n):
    return np.round(np.linspace(0, len(arr) - 1, n)).astype(int)


def beta_dist(arr, n):
    distribution = stats.beta(loc=0, scale=512, a=0.5, b=0.5)
    bounds_for_range = distribution.cdf([0, len(arr)])
    pp = np.linspace(*bounds_for_range, num=n)

    return [int(max(min(x, len(arr) - 1), 0)) for x in distribution.ppf(pp)]


def norm_dist(arr, n):
    distribution = stats.norm(loc=int(len(arr) / 2), scale=100)
    bounds_for_range = distribution.cdf([0, len(arr)])
    pp = np.linspace(*bounds_for_range, num=n)

    return [int(max(min(x, len(arr) - 1), 0)) for x in distribution.ppf(pp)]


def plot_distribution(elevation, interp, interp_name, distributions, distributions_names):
    # Zależność od rozkładu

    fig, axs = plt.subplots(3, 1, sharex='col')
    fig.subplots_adjust(hspace=.2, wspace=.1)
    fig.set_size_inches(8, 11.5 * 3 / 5)
    axs = axs.ravel()
    for n in range(3):
        idx = distributions[n](elevation[:, 0], 32)
        xs = elevation[:, 0][idx].tolist()
        ys = elevation[:, 1][idx].tolist()

        xsn = np.linspace(min(xs), max(xs), 10000)
        i = interp(xs, ys)
        print(f"n: {n}")
        axs[n].scatter(xs, ys, s=6)
        axs[n].plot(xsn, [i(x) for x in xsn], label="Interpolacja " + interp_name, alpha=1)
        axs[n].plot(elevation[:, 0], elevation[:, 1], label="Funkcja interpolowana",
                    alpha=0.5)
        axs[n].grid()
        axs[n].autoscale()
        axs[n].set_title(distributions_names[n])
        axs[n].set_ylabel("Y[m]")
        if n == 4:
            axs[n].set_xlabel("X[m]")
    plt.legend()
    plt.savefig("plots/" + "Dist " + interp_name + ".png", dpi=600)


def plot_err(elevation, interp, interp_name, errs):
    # Zależność od błędu

    fig, axs = plt.subplots(3, 1, sharex='col')
    fig.subplots_adjust(hspace=.2, wspace=.1)
    fig.set_size_inches(8, 11.5 * 3 / 5)
    axs = axs.ravel()
    for n in range(3):
        xs = [x + random.uniform(0, errs[n]) for x in elevation[:, 0][idx].tolist()]
        ys = elevation[:, 1][idx].tolist()

        xsn = np.linspace(min(xs), max(xs), 10000)
        i = interp(xs, ys)
        print(f"n: {n}")
        axs[n].scatter(xs, ys, s=6)
        axs[n].plot(xsn, [i(x) for x in xsn], label="Interpolacja " + interp_name, alpha=1)
        axs[n].plot(elevation[:, 0], elevation[:, 1], label="Funkcja interpolowana",
                    alpha=0.5)
        axs[n].grid()
        axs[n].autoscale()
        axs[n].set_title(distributions_names[n])
        axs[n].set_ylabel("Y[m]")
        if n == 4:
            axs[n].set_xlabel("X[m]")
    plt.legend()
    plt.savefig("plots/" + "Dist " + interp_name + ".png", dpi=600)


if __name__ == "__main__":
    main()
