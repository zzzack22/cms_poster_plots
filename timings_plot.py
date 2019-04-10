"""
Plot of timings for Unsold-W12 old implementation vs new implementation
"""

import read_file
import numpy as np
import matplotlib.pyplot as plt


def timings_plot(headings, data_array, y_min = None, y_max = None, scale="linear",
                 output="timings.pdf"):
    """
    Scatter plot for each column of data, with first column giving x vales
    :param headings: list of column headings for data titles
    :param data_array: Array in format ( x, y1, y2, ... )
    :param dp: number of decimal places for y axis limits
    """

    n_cols = data_array.shape[0]

    x = data_array[0]
    fig, ax = plt.subplots(figsize=(read_file.cm(28), read_file.cm(20)))
    ax.set_xlim(x[0], x[len(x) - 1])
    if scale == "linear":
        ax.set_ylim(y_min, y_max)
    ax.set_xlabel('n ($C_n H_{2n+2}$)')
    ax.set_ylabel('Time per SCF step / $s$')
    ax.tick_params(axis='both', which='major', labelsize=22, pad=10)
    ax.set_yscale(scale)

    for i in range(1, n_cols):
        y = data_array[i]

        if scale == "linear":
            # get polynomial line fit
            fit = np.polyfit(x, y, 4)
            f = np.poly1d(fit)
            xnew = np.linspace(x[0], x[-1], num=200, endpoint=True)
            ynew = f(xnew)
            ax.plot(x, y, 'o')
            ax.plot(xnew, ynew, label=headings[i], linewidth=2)
        elif scale =="log":
            ax.plot(x, y, 'o', label=headings[i])

    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)

    ax.legend(ncol=2, frameon=False, fontsize=20)
    plt.show()
    fig.savefig(output)


if __name__ == '__main__':
    titles, data = read_file.get_data("timings")
    data = data.astype(float)

    data = np.transpose(data)
    timings_plot(titles, data, y_min=0, y_max=700, output="timings_smallscale.pdf")
    timings_plot(titles, data, y_min=0, y_max=3500, output="timings_largescale.pdf")
    timings_plot(titles, data, scale="log", output="timings_log.pdf")
