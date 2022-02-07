import pyedflib
import numpy as np

# file_name = pyedflib.data.get_generator_filename()
file_name = "edf_data/1234_20220127_182356_EC.edf"
f = pyedflib.EdfReader(file_name)
# print(dir(pyedflib))
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i,:] = f.readSignal(i)
print(sigbufs.shape)
# print(sigbufs[0][0:1000])
print("==========="*10)
print(sigbufs[0].dtype)

loss = 0
for i in range(sigbufs[0].size):
    if sigbufs[0][i] == sigbufs[0][-1]:
        loss += 1
print(sigbufs[0][-1])
print("loss : ", loss)
# print(np.where(sigbufs == 0.00433432))
# print(sigbufs[0][26000:27000])

# print("==========="*10)
# print(sigbufs[0][29000:])