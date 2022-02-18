# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:27:21 2022

@author: Caliphax
"""

from pylab import *
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def plot_response(fs, w, h, title):
    "Utility function to plot response functions"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    ax.set_ylim(-90.0, 5.0)
    ax.set_xlim(0, 0.5*fs)
    ax.grid(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.set_title(title)

def mfreqz(b,fs,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    subplot(211)
    plot(w/max(w)*fs/2,h_dB)
    ylim(-100, 5)
    ylabel('Magnitude (db)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Frequency response')
    subplot(212)
    h_Phase = unwrap(arctan2(imag(h),real(h)))
    plot(w/max(w)*fs/2,h_Phase)
    ylabel('Phase (radians)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Phase response')
    subplots_adjust(hspace=0.5)

#Plot step and impulse response
def impz(b,a=1):
    l = len(b)
    impulse = repeat(0.,l); impulse[0] =1.
    x = arange(0,l)
    response = signal.lfilter(b,a,impulse)
    subplot(211)
    stem(x, response)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Impulse response')
    subplot(212)
    step = cumsum(response)
    stem(x, step)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Step response')
    subplots_adjust(hspace=0.5)
    
    
fs = 44100.0         # Sample rate, Hz
band = [3000, 5000]  # Desired pass band, Hz
trans_width = 260    # Width of transition from pass band to stop band, Hz
numtaps = 161        # Size of the FIR filter.

edges = [0, band[0] - trans_width, band[0], band[1],band[1] + trans_width, 0.5*fs]
taps = signal.remez(numtaps, edges, [0, 1, 0], type='hilbert', Hz=fs, maxiter=500)
taps = signal.remez(161, [.00005, .49995], [1], type='hilbert', maxiter=500)
delay = np.zeros(161)
delay[80] = 1.0

plot(taps)
show()
mfreqz(taps,fs)
#impz(taps)
show()
7


fs = 22050.0       # Sample rate, Hz
cutoff = 8000.0    # Desired cutoff frequency, Hz
trans_width = 100  # Width of transition from pass band to stop band, Hz
numtaps = 400      # Size of the FIR filter.
taps = signal.remez(numtaps, [0, cutoff, cutoff + trans_width, 0.5*fs], [1, 0], Hz=fs)
w, h = signal.freqz(taps, [1], worN=2000)
plot_response(fs, w, h, "Low-pass Filter")

fs = 22050.0         # Sample rate, Hz
band = [200, 9000]  # Desired pass band, Hz
trans_width = 190    # Width of transition from pass band to stop band, Hz
numtaps = 201        # Size of the FIR filter.
edges = [0, band[0] - trans_width, band[0], band[1],
         band[1] + trans_width, 0.5*fs]
taps = signal.remez(numtaps, edges, [0, 1, 0], type='hilbert', Hz=fs)
delay = np.zeros(numtaps)
delay[int(numtaps/2)] = 1.0
w, h = signal.freqz(taps, [1], worN=2000)
plot_response(fs, w, h, "Band-pass Filter")


window = signal.windows.kaiser(numtaps, beta=4)
plot( window )

duration = .1   # in seconds, may be float
f = 2000.0        # sine frequency, Hz, may be float
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

out_hilbert = np.convolve( taps, samples )
out_delay = np.convolve( delay, samples )

plot(out_hilbert)
plot(out_delay)

#>>> print("string - %s , float - %3.5f" % ('hello world',3.144343))

filename = 'fir_coeffs_%dTaps_%d_%d_%d.h' % ( numtaps, int(fs), band[0], band[1] )

with open(filename,'w') as file:
    
    print( 'float coeffs_hilbert_%dTaps_%d_%d_%d[] = {' % ( numtaps, int(fs), band[0], band[1] ), file=file)
    for r in taps:
        print( '%15.10f,' % r, file=file )
    print( '};', file=file )
        
    print( 'float coeffs_delay_%d[] = {' % numtaps, file=file)
    for r in delay:
        print( '%15.10f,' % r, file=file )
    print( '};', file=file )

file.close()