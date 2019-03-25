"""
Read data table from file
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def readfile(file):
    """
    Reads data from file
    :param file: Filename
    :return: Filedata
    """
    f = open(file, 'r')
    columns = []
    headings = f.readline().split()
    for line in f:
        line = line.strip()
        column = line.split()
        columns.append(column)
    f.close()
    return headings, columns

def cm(length):
    return length /2.54

def fractional_plot(headings, data_array, y_min, y_max):
    """
    Scatter plot for each column of data, with first column giving x vales
    :param headings: list of column headings for data titles
    :param data_array: Array in format ( x, y1, y2, ... )
    :param dp: number of decimal places for y axis limits
    """

    n_cols = data_array.shape[0]

    x = data_array[0]
    yData = []
    fig, ax = plt.subplots(figsize=(cm(28), cm(20)))
    lines = []
    ax.set_xlim(x[0], x[len(x) - 1])
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Electron Number')
    ax.set_ylabel('Energy Difference / $eV$')
    ax.tick_params(axis='both', which='major', labelsize=22, pad=10)

    for i in range(1, n_cols):
        y = data_array[i]
        yData.append(y)
        f1 = interp1d(x[0:11], y[0:11], kind='cubic')
        f2 = interp1d(x[10:], y[10:], kind='cubic')
        xnew = np.linspace(x[0], x[len(x) - 1], num=401, endpoint=True)
        ynew1 = f1(xnew[0:201])
        ynew2 = f2(xnew[201:])
        ynew = np.concatenate((ynew1, ynew2))
        line = ax.plot(xnew, ynew, label=headings[i], linewidth=2)
        lines.append(line)

    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)

    plt.hlines(0, 9, 11, linestyle=':', linewidth=1)
    ax.legend(fontsize=20, loc=4, ncol=2, frameon=False, columnspacing=0.2, borderaxespad=-0.2)
    plt.show()
    fig.savefig("frac.pdf")


def get_data(file):
    """
    Reads data from file and sorts into a numpy array
    :param file: name of file
    :return: column headings and sorted data array
    """
    titles, data = readfile(file)
    data = np.array(data)
    return titles, data

if __name__ == '__main__':
    # Take filename from input
    filename = sys.argv[1]
    titles, data = get_data(filename)
    data = data.astype(float)
    data = data[data[:,0].argsort()]

    data = np.transpose(data)
    fractional_plot(titles, data, y_min=-1.25, y_max=0.75)
