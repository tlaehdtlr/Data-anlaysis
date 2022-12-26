# from tokenize import String
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

hex2decimal = {
    '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9,
    'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15
}
def get_raw_data():
    file_path = '2022-10-21T01_13_26.900Z-log.txt'
    # file_path = 'nrf_connect_raw_data/nrf_183f_2min_5.txt'
    # file_path = 'nrf_connect_raw_data/nrf_c693_distance.txt'
    print(file_path)
    file = open(file_path, 'r')
    raw_data = file.readlines()

    raw_data_arr = []
    cnt = 0;
    lost = 0
    for line in raw_data:
        # line[81:783] : 1 packet data
        # print(len(line))
        # print(line[92:])
        # nrf mobile
        '''
        if 'Notification received' in line:
            packet = list(map(lambda x : hex2decimal[x[0]]*16 + hex2decimal[x[1]], line[92:].split('-')))
            for sam in range(4):
                raw_data_arr.append(packet[sam*57: sam*57 + 57])
            if (cnt + 1 != ((packet[-3]<<16) + (packet[-2]<<8) + packet[-1])):
                lost+=1
            cnt = (packet[-3]<<16) + (packet[-2]<<8) + packet[-1]
        '''
        # nrf desktop
        '''
        '''
        if 'handle: 0x0D, value' in line:
            packet = list(map(lambda x : hex2decimal[x[0]]*16 + hex2decimal[x[1]], line[81:].split('-')))
            for sam in range(4):
                raw_data_arr.append(packet[sam*57: sam*57 + 57])
            if (cnt + 1 != ((packet[-3]<<16) + (packet[-2]<<8) + packet[-1])):
                lost+=1
            cnt = (packet[-3]<<16) + (packet[-2]<<8) + packet[-1]



    file.close()

    return raw_data_arr, cnt, lost


twos_complement = 128<<16   # MSB 1000 0000
def convert_twos_comple(value):
    if value&twos_complement:
        # negative
        value = -(2**24 - value)

    return value


gain = 24
lsb_size = 2*(2.048 -  (-2.5)) / gain / (2**24 - 1) # scale : V
def dac_data(dac_arr, packet_decimal):
    data = []
    for ch in range(19):
        val = packet_decimal[ch*3]<<16 | packet_decimal[ch*3+1]<<8 | packet_decimal[ch*3+2]
        val = convert_twos_comple(val)
        val = val * lsb_size * gain * 10**6
        data.append(val)
    dac_arr.append(data)
    return ;


def notch_filter(data, fs, f0, Q=30):
    w0 = f0/(fs/2) # normalization
    b, a = signal.iirnotch(w0, Q)
    data = signal.lfilter(b, a, data)
    return data


def visualize(np_data):
    # plt.plot(np_data[:,0])

    Fs = 250    # sampling rate
    Ts = 1/Fs   # sampling interval

    # # Create/view notch filter
    # samp_freq = 250  # Sample frequency (Hz)
    # notch_freq = 60.0  # Frequency to be removed from signal (Hz)
    # quality_factor = 30.0  # Quality factor
    # b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    # # freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)

    # # for ch in range(19):
    #     # y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
    # y_notched = signal.filtfilt(b_notch, a_notch, np_data[:,0])

    # y_notched = notch_pass_filter(np_data, 60, 20, np_data.)

    y_notched = notch_filter(np_data[:,0], Fs, 60, 30)
    print(y_notched, y_notched.size)

    data_sensing_time = np_data[:,0].size * 1000 / Fs
    # x = np.arange(0, data_sensing_time, data_sensing_time/np_data[:,0].size)
    freq = np.fft.fftfreq(np_data[:,0].size, Ts)
    # x_freq = np.fft.rfftfreq(np_data[:,0].size, Ts)[:-1]
    # x_freq = np.fft.rfftfreq(np_data[:,0].size, Ts)
    # y_fft = np.fft.rfft(eeg_data) / data_size
    # y_fft = np.fft.rfft(np_data[:,0])
    # y_fft = abs(y_fft[:-1]*2)
    y_fft = np.fft.rfft(y_notched)
    y_fft = abs(y_notched*2)


    # plt.plot(y_notched)
    plt.plot(freq, y_fft)
    plt.grid(True)
    plt.show()
    return ;


def save_txt(data):
    ouput_filename = "nrf_cnt_processed.txt"
    np.savetxt('ouput_filename.txt', data, delimiter=',', newline='\n')
    return ;


def main():
    print('\n================== nRF connect APP log analysis ========================\n')
    cnt = 0;
    raw_data_arr, cnt, lost = get_raw_data();
    # for data in raw_data_arr:
    #     dac_data()
    dac_arr = []
    for packet in raw_data_arr:
        dac_data(dac_arr, packet)

    np_data = np.array(dac_arr)
    print(np_data.shape)
    print(np_data[:,0].shape)
    print("cnt : ", cnt, "lost : ", lost)
    # visualize(np_data)
    for i in range(19):
        plt.plot(np_data[:,i])
        plt.grid(True)
        plt.show()

    # save_txt(np_data)

main()