import numpy as np
import matplotlib.pyplot as plt

### preprocess log data
fname = 'noise/13.txt'
# fname = 'imedisync/2mV_1Hz_open.txt'

test_signal = False

if test_signal:
    data = np.loadtxt(fname, usecols=[4,5]);
    data_ch1, data_ch2 = np.array(data[:,0], dtype='float'), np.array(data[:,1], dtype='float')
else:
    data = np.loadtxt(fname, usecols=[2,3]);
    # 이건 시그널 안 물린거 60Hz 오지게 나옴
    # data_ch1 =  np.array(data[:,1], dtype='float')
    # 장비 물린 채널 30Hz
    data_ch1 =  np.array(data[:,1], dtype='float')


'''
data 어떻게 얻었는지 확인 제대로 해야함
'''
# data sampling freq
freq_adc_get = 250
# frontend 증폭
frontend = 104
# gain 증폭
gain = 24
# app 처리
app_calc = 400
# micro 로 바꿔주기
convert_micro = 1000000

# data sampling total time
data_sensing_time = data_ch1.size * 1000 / freq_adc_get

### plot
print(plt.figure(figsize=(12,7)))
# fig, ax = plt.subplots(2,1, figsize=(12,7))

## ch1 time
plt.subplot(2,1,1)
plt.plot(np.arange(0, data_sensing_time, data_sensing_time/data_ch1.size), data_ch1/app_calc/frontend/gain*convert_micro)
plt.title('CH-1 (time domain)')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (uv)')
# plt.xlim(0,10000)
# plt.xlim(10000,20000)
# plt.ylim(-1500,1500)
plt.grid(True)


## ch1 freq
plt.subplot(2,1,2)
freq_data = np.fft.fft(data_ch1)
freq_data = abs(freq_data)
# freq_data = abs(freq_data)/np.max(abs(freq_data))

interval_sampling = data_sensing_time/data_ch1.size
freq = np.fft.fftfreq(data_ch1.size, interval_sampling/1000)
plt.plot(freq, freq_data)

plt.title('CH-1 (Frequency domain)')
plt.xlabel('freq (Hz)')
plt.ylabel('amplitude')

plt.xlim(0,150)
plt.grid(True)

plt.tight_layout()

plt.show()