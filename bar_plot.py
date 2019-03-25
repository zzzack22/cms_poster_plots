"""
Generates a stacked bar plot designed for mean and absolute mean errors
"""
import read_file

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def stacked_bar_graphs(headings, labels, data_array1, data_array2,
                       outputfilename, ymin=-6, ymax=6, sep=1.5, end=1.5):
    """
    Creates a bar graph from an array of data
    :param headings: column headings for each set of data
    :param labels: list of labels for each set of data
    :param data_array1: data array of the form (names, y1, y2, ...)
    :param data_array2: second data array of same shape
    :param outputfilename: name of output plot
    :param ymin: minimum y value
    :param ymax: maximum y value
    """

    fig, ax = plt.subplots(figsize=(read_file.cm(24), read_file.cm(20)))

    data_values1 = data_array1[1:].astype(float)
    data_values2 = data_array2[1:].astype(float)

    n_bars = data_values1.shape[1]
    n_functionals = data_values1.shape[0]
    # set width of bar
    barWidth = 0.1

    # Set position of bar on X axis
    bar_positions = np.arange(n_bars)
    for i in range(n_functionals):
        ax.bar(bar_positions, data_values2[i], width=barWidth, label=headings[i+1])
        ax.bar(bar_positions, data_values1[i], width=0.01, color='k')
        bar_positions = np.array([x + sep * barWidth for x in bar_positions])

    # Add xticks on the middle of the group bars
    plt.hlines(0, -2, 2, linewidth=1)
    plt.xticks([r + (sep + 1) * barWidth for r in range(n_bars)], labels)

    ax.set_xlim(- barWidth, 2 - end * barWidth)
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel('Errors / $eV$')

    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)
    ax.tick_params(axis='both', which='major', labelsize=20, pad=10)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # Create legend & Show graphic
    plt.legend(fontsize=20, loc=4, ncol=2, frameon=False, columnspacing=0.2, borderaxespad=-0.2)
    plt.show()
    fig.savefig(outputfilename)


if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    titles1, data1 = read_file.get_data(filename1)
    titles2, data2 = read_file.get_data(filename2)
    data_labels = ['Barrier Heights', 'Reaction Energies']

    mean_errors = np.column_stack((data1[0], data2[0]))
    mae = np.column_stack((data1[1], data2[1]))

    stacked_bar_graphs(titles1, data_labels, mean_errors, mae, "reactions.pdf")
