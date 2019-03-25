import bar_plot
import read_file
import numpy as np

if __name__ == '__main__':
    filename = "deltascf"
    titles, data = read_file.get_data(filename)
    data_labels = ['Singlets', 'Triplets']

    mean_errors = np.column_stack((data[0], data[2]))
    mae = np.column_stack((data[1], data[3]))

    bar_plot.stacked_bar_graphs(titles, data_labels, mean_errors, mae,
                                "deltascf.pdf", -0.4, 1, 2, 3)
