#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 08:21:02 2022

@author: xenir
"""
import numpy as np
import matplotlib.pyplot as plt


import numpy.fft
import matplotlib.pyplot as plt

coeffs = numpy.fft.fftshift(
    numpy.fft.ifft([0] + [1]*200 + [0]*200)
)

fs = 44100.0        # Sample rate, Hz
duration = 1   # in seconds, may be float
f = 700.0      # sine frequency, Hz, may be float

#plt.plot(numpy.imag(coeffs))
#plt.plot(numpy.real(coeffs))
#plt.show()

samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

i = numpy.imag(coeffs)
r = numpy.real(coeffs)

out_imag = np.convolve( i, samples )
out_real = np.convolve( r, samples )

#plt.plot(out_imag)
#plt.plot(out_real)

plt.scatter( out_imag[200:-200], out_real[200:-200], s=5, marker='.' )
