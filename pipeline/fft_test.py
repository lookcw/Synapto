import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft


Fs = 250.0;  # sampling rate
N = 1000 # Number of sample points

freq = np.arange(0,Fs/2,Fs/N)

x = np.linspace(0, 200, N)
y = 2 ** (np.sin(x) + np.sin(x/3.2))

yf = fft(y)
yf = yf[0:(N/2)]

# plt.plot(freq, (2.0/N) * np.abs(yf))
plt.plot(freq, 10*np.log10(2.0/N * np.abs(yf)))
plt.grid()
plt.show()