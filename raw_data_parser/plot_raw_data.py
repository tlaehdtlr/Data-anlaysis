import numpy as np
import matplotlib.pyplot as plt


def get_data_from_txt():
    fname = 'raw_data_float.txt'
    file = open(fname, 'r')
    raw_data = file.readlines()

    raw_data_int = []
    for sam in raw_data:
        raw_data_int.append(list(map(float, sam.split(','))))

    np_data =  np.array(raw_data_int)
    np_data_ch1 = np_data[:,0]
    return np_data_ch1


def plot_data(data):
    Fs = 250
    sampling_time = data.size / Fs *1000
    print(data.size)
    x_axis = np.arange(0, sampling_time, 1000/Fs)
    plt.plot(x_axis, data)
    plt.grid(True)
    plt.show()


def main():
    plot_data(get_data_from_txt());

    return;


main()