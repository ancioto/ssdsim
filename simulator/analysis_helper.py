# This file is part of the WAF-Simulator by Nicholas Fiorentini (2015)
# and is released under Creative Common Attribution 4.0 International (CC BY 4.0)
# see README.txt or LICENSE.txt for details

"""
This file contains helper function for simulation data analysis and plotting, to be used in a iPython notebook.
"""

# IMPORTS
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy import stats


# LOAD DATA
def load_data(sim_names, path_string):
    """ Load the csv with the data and execute some conversions """
    data = dict()
    base_path = Path(path_string)
    for d in sim_names:
        fp = base_path.joinpath("raw_data_{}.csv".format(d))
        data[d] = dict()
        for i in range(0, 11):
            data[d][i] = np.genfromtxt(str(fp), dtype=None, skip_header=2, delimiter=',', usecols=[i, ])

    # convert all times in seconds
    for n in sim_names:
        data[n][0] = np.array(data[n][0] / 10 ** 6)

    return data


# FINAL STATS
def generate_final_stats(sim_names, data):
    """ Some handful results """
    for n in sim_names:
        print("\n\n{:<15}{:<15}{:<15}{:<15}".format(n, 'Min', 'Max', 'Mean'))

        for i, key in list(enumerate(['time',
                                      'iops',
                                      'bandwidth',
                                      'amplification',
                                      'host write',
                                      'host read',
                                      'disk write',
                                      'disk read',
                                      'block erased',
                                      'failures',
                                      'dirty pages'])):
            r = stats.describe(data[n][i])
            print("{:<15}{:<15}{:<15}{:,.2f} ± {:,.2f}".format(key, r.minmax[0], r.minmax[1],
                                                              r.mean, np.sqrt(r.variance)))


# PLOT HELPER
def inline_plot(sim_names, data, yid, xlabel, ylabel, xid=4, xlog=False, ylog=False,
                title="Random writes of pages (4 KiB each)", show=True):
    """ Plot helper common to all plots """
    for n in sim_names:
        plt.plot(data[n][xid], data[n][yid], linestyle='-', label=n)

    if xlog:
        plt.yscale('log')
    if ylog:
        plt.xscale('log')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.grid(True)

    if show:
        plt.show()


# COMMON PLOTS
def plot_disk_writes(sim_names, data):
    """ plot the random writes host vs disk """
    inline_plot(sim_names, data, yid=6, xlog=True, ylog=True,
                xlabel="Host write [log pages]",
                ylabel="Disk write [log pages]")


def plot_disk_write_time(sim_names, data):
    """ plot host write time """
    inline_plot(sim_names, data, xid=0, yid=4,
                xlabel="Elapsed time [seconds]",
                ylabel="Host write [pages]")


def plot_iops(sim_names, data):
    """ plot the IOPS """
    inline_plot(sim_names, data, yid=1,
                xlabel="Host write [pages]",
                ylabel="Host IOPS")


def plot_disk_af(sim_names, data):
    """ plot the Amplification factor """
    inline_plot(sim_names, data, yid=3,
                xlabel="Host write [pages]",
                ylabel="Write amplification")


def plot_bandwidth(sim_names, data):
    """ plot the bandwidth """
    inline_plot(sim_names, data, yid=2,
                xlabel="Host write [pages]",
                ylabel="Bandwidth [MiB\s]")


def plot_dirty_pages(sim_names, data):
    """ plot the dirty pages """
    inline_plot(sim_names, data, yid=10,
                xlabel="Host write [pages]",
                ylabel="Dirty [pages]")


def plot_write_faiures(sim_names, data):
    """ plot the failures """
    inline_plot(sim_names, data, yid=9,
                xlabel="Host write [pages]",
                ylabel="Write failed [pages]")
