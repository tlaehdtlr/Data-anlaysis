# from tokenize import String
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

hex2decimal = {
    '0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9,
    'A' : 10, 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15
}
def get_raw_data():
    raw_data_cnt = []
    lost = 0
    '''
    device
        0 - Dongle
        1 - Tablet
        2 - phone
    '''
    device = 1

    if device == 0:
        # file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_version_cnt.txt'
        file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_connect_dongle_3.txt'
        print(file_path)
        file = open(file_path, 'r')
        raw_data = file.readlines()
        for line in raw_data:
            # print(line[92:])
            if 'handle: 0x0D, value' in line:
                packet = list(map(lambda x : hex2decimal[x[0]]*16 + hex2decimal[x[1]], line[-9:].split('-')))
                raw_data_cnt.append((packet[0]<<16) + (packet[1]<<8) + packet[2])
        file.close()
    elif device == 1:
        # file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_connect_tablet_A_3.txt'
        file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_connect_tablet_S_3.txt'
        print(file_path)
        file = open(file_path, 'r')
        raw_data = file.readlines()
        for line in raw_data:
            if 'from 53011701' in line:
                packet = list(map(lambda x : hex2decimal[x[0]]*16 + hex2decimal[x[1]], line[-9:].split('-')))
                raw_data_cnt.append((packet[0]<<16) + (packet[1]<<8) + packet[2])
        file.close()
    elif device == 2:
        file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_connect_phone.txt'
        # file_path = 'nrf_connect_raw_data/nrf_connect_input/nrf_version_mobile.txt'
        print(file_path)
        file = open(file_path, 'r')
        raw_data = file.readlines()
        for line in raw_data:
            if 'Notification received from' in line:
                packet = list(map(lambda x : hex2decimal[x[0]]*16 + hex2decimal[x[1]], line[-9:].split('-')))
                raw_data_cnt.append((packet[0]<<16) + (packet[1]<<8) + packet[2])
        file.close()

    print("raw_data_cnt : ", raw_data_cnt)
    temp_st = 1
    print("==============lost start==================")
    for i in range(len(raw_data_cnt)-1):
        if (temp_st != raw_data_cnt[i+1] - 1):
            print("{} - {} /".format(temp_st+1, raw_data_cnt[i+1]-1), end=" ")
            lost += raw_data_cnt[i+1] - temp_st - 1
        temp_st = raw_data_cnt[i+1]
    print("\n==============lost end==================")
    print("cnt : {} \nlost : {}".format(raw_data_cnt[-1], lost))


def main():
    print('\n================== compare cnt to cnt of packet in nRF connect APP log  ========================\n')
    get_raw_data();

main()