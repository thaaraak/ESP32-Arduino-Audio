# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:27:21 2022

@author: NA5Y
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
    
    
# This function generates a Hilbert transform with 'numtaps' coefficients and
# an associated delay line with the same number of taps.
#   sample_rate         Sample Rate in Hz
#   band                Pass band limits for the filter
#   transition_width    width in Hz between the pass band and stop band
#   window_function     Window function used (kaiser is used in the example)

def generate_hilbert( numtaps, sample_rate, band, transition_width, window_function ):

    edges = [0, band[0] - transition_width, band[0], band[1],
             band[1] + transition_width, 0.5*sample_rate]
    t = signal.remez(numtaps, edges, [0, 1, 0], type='hilbert', Hz=sample_rate)
    d = np.zeros(numtaps)
    d[int(numtaps/2)] = 1.0
    
    if window_function is not None:
        t = t * window_function

    return d, t
   
def read_coeffs( filename ):
    
    ret=[]
    with open(filename) as file: 
        for line in file:
           if (line.strip()):
                ret.append(float(line.strip()))
    return ret


def generate_hilbert_header( numtaps, sample_rate, band, delay, taps ):
    filename = 'fir_coeffs_%dTaps_%d_%d_%d.h' % ( numtaps, int(sample_rate), band[0], band[1] )
    
    with open(filename,'w') as file:
        
        print( 'float coeffs_hilbert_%dTaps_%d_%d_%d[] = {' % ( numtaps, int(sample_rate), band[0], band[1] ), file=file)
        for r in taps:
            print( '%15.10f,' % r, file=file )
        print( '};', file=file )
            
        print( 'float coeffs_delay_%d[] = {' % numtaps, file=file)
        for r in delay:
            print( '%15.10f,' % r, file=file )
        print( '};', file=file )
    
    file.close()


fs = 44100.0        # Sample rate, Hz
band = [200, 19200]  # Desired pass band, Hz
trans_width = 190   # Width of transition from pass band to stop band, Hz
numtaps = 501       # Size of the FIR filter.
window = signal.windows.kaiser(numtaps, beta=8) # Window function to be used

delay, taps = generate_hilbert( numtaps, fs, band, trans_width, window )
generate_hilbert_header(numtaps, fs, band, delay, taps)

# Plot the frequency response
w, h = signal.freqz(taps, [1], worN=2000)
#plot_response(fs, w, h, "Band-pass Filter")

# Test the filter with a simulated signal
duration = .1   # in seconds, may be float
f = 700.0      # sine frequency, Hz, may be float
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs) + 
           np.sin(2*np.pi*np.arange(fs*duration)*1900.0/fs)
           ).astype(np.float32)

# Plot the output. For a 90 degree phase shift the scatter plot
# should be a perfect circle

minus45 = read_coeffs( '501Tap-0.txt' );
plus45 = read_coeffs( '501Tap-90.txt' );

# Convolve the test signal with the Hilbert transform and the Delay line
# There should be a 90 degree phase offset between the hilbert and the delay convolved
# output signals
out_plus45 = np.convolve( minus45, samples )
out_minus45 = np.convolve( plus45, samples )

out_hilbert = np.convolve( taps, samples )
out_delay = np.convolve( delay, samples )


figure(1)
plot(out_hilbert[200:-200])
plot(out_delay[200:-200])

figure(2)
scatter( out_hilbert[200:-200], out_delay[200:-200], s=5, marker='.' )

figure(3)
plot(out_minus45[200:-200])
plot(out_plus45[200:-200])

figure(4)
scatter( out_minus45[200:-200], out_plus45[200:-200], s=5, marker='.' )



