import numpy as np
import matplotlib.pyplot as plt

### preprocess log data
data = np.loadtxt("stm_log/100uV_x1_modified_cal.txt", dtype='str', delimiter='\t', skiprows=8)
time, data_ch1 = np.array(data[:,1], dtype='float'), np.array(data[:,2], dtype='float')
# time, data_ch1 = np.array(data[:,1]), np.array(data[:,2])

### plot
print(plt.figure(figsize=(12,7)))
# fig, ax = plt.subplots(2,1, figsize=(12,7))

## time
plt.subplot(2,1,1)
plt.plot(time, data_ch1)
plt.title('Time domain')
plt.xlabel('time (ms)')
plt.ylabel('amplitude (mv)')
plt.grid(True)


## freq
plt.subplot(2,1,2)
freq_data = np.fft.fft(data_ch1)
freq_data = abs(freq_data)

data_sample = abs(np.mean(time[:-1] - time[1:]))
# data_sample = np.mean(np.subtract(time[:-1], time[1:]))
freq = np.fft.fftfreq(time.size, data_sample/1000)
plt.plot(freq, freq_data)

plt.title('Frequency domain')
plt.xlabel('freq (Hz)')
plt.ylabel('amplitude')


plt.xlim(0,60)
plt.grid(True)

plt.tight_layout()

plt.show()