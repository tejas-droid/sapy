""" Example of Fourier Transformation and Power-spectra

If you want the output to use the LaTeX-formatting, please
    i) make sure that LaTeX is installed properly on your system, and then
    ii) manually set the flag 'latex_installed' in line 22 to 'True'
"""
    

# author:   Thomas Haslwanter
# date:     June-2020

# Import the standard packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import os

# For simplified presentation
from utilities.my_style import set_fonts, show_data 

latex_installed = True
    
if latex_installed:
    import matplotlib
    matplotlib.rcParams['text.usetex'] = True

def generate_data() -> None:
    """ Generate sample data for the FFT-demo """

    # Generate some data, as a superposition of three sine waves
    # First set the parameters
    rate = 200     # [Hz]
    duration = 60   # [sec]
    freqs = [3, 7, 20]
    amps = [1, 2, 3]
    
    # Then calculate the data
    dt = 1/rate
    t = np.arange(0, duration, dt)
    
    # The clear way of doing it
    sig = np.zeros_like(t)
    for (amp, freq) in zip(amps, freqs):
        omega = 2 * np.pi * freq
        sig += amp * np.sin(omega*t)
        
    # Add some noise, and an offset
    np.random.seed(12345)
    offset = 1
    noise_amp = 5
    sig_without_noise = sig + offset
    sig_with_noise = sig_without_noise + noise_amp * np.random.randn(len(sig)) 
    
    # Note that the same could be achived with a single line of code.
    # However, in my opinion that is much less clear
    #sig = np.ravel(np.atleast_2d(amps) @ np.sin(2*np.pi * np.c_[freqs]*t)) + \
        #np.random.randn(len(t))*5
        
    return (t, dt, sig_with_noise, sig_without_noise)


def power_spectrum(t: np.ndarray, dt: float, sig: np.ndarray,
                   sig_ideal: np.ndarray) -> None:
    """ Demonstrate three different ways to calculate the power-spectrum
    
    Parameters
    ----------
    t : time [sec]
    dt : sample period [sec]
    sig : sample signal to be analyzed
    sig_ideal : signal without noise
    """
    
    set_fonts(16)
    
    fig, axs = plt.subplots(1,2, figsize=(10, 5))
    
    if latex_installed:
        txt ='$\displaystyle signal=offset + \sum_{i=0}^{2} a_i*sin(\omega_i*t) + noise$'
        label = '$|FFT|\; ()$'
        label2 = '$|FFT|^2  ()$'
    else:
        txt = 'signal = offset + sum(i=0:2) a_i*sin(omega_i*t)'
        label = '|FFT| ()'
        label2 = '|FFT|^2 ()'
        
    # From a quick look we learn - nothing
    axs[0].plot(t, sig, lw=0.7, label='noisy')
    axs[0].plot(t, sig_ideal, ls='dashed', lw=2, label='ideal')
    axs[0].set_xlim(0, 0.4)
    axs[0].set_ylim(-15, 25)
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Signal ()')
    axs[0].legend()
    axs[0].text(0.2, 24, s=txt, fontsize=16)
    
    # Calculate the spectrum by hand
    fft = np.fft.fft(sig)
    print(fft[:3])
    fft_abs = np.abs(fft)
    
    # The easiest way to calculate the frequencies
    freq = np.fft.fftfreq(len(sig), dt)
    
    axs[1].plot(freq, fft_abs)
    axs[1].set_xlim(0, 35)
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel(label)
        
    axs[1].set_yticklabels([])
    show_data('FFT_sines.jpg')
    
    # Also show the double-sided spectrum
    fig, ax = plt.subplots(1,1)
    ax.plot(fft_abs)
    #ax.set_xlim(0, 35)
    ax.set_xlabel('Points')
    ax.set_ylabel(label)
    plt.tight_layout()
    show_data('FFT_doublesided.jpg')
    
    # With real input, the power spectrum is symmetrical and we only one half
    fft_abs = fft_abs[:int(len(fft_abs)/2)]
    freq = freq[:int(len(freq)/2)]
    
    # The power is the norm of the amplitude squared
    Pxx = fft_abs**2
    # Showing the same data on a linear and a log scale
    fig, axs = plt.subplots(2,1, sharex=True)
    axs[0].plot(freq, Pxx)
    axs[0].set_ylabel('Power (linear)')
    axs[1].semilogy(freq, Pxx)
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Power (dB)')
    show_data('FFT_sines_power_lin_log.jpg')
    
    # Periodogram and Welch-Periodogram
    f_pgram, P_pgram = signal.periodogram(sig, fs = 1/dt)
    f_welch, P_welch = signal.welch(sig, fs = 100, nperseg=2**8)
    
    fig, axs = plt.subplots(2, 1, sharex=True)
    
    axs[0].semilogy(f_pgram, P_pgram, label='periodogram')
    axs[1].semilogy(f_welch, P_welch, label='welch')
    
    axs[0].set_ylabel('Spectral Density (dB)')
    axs[0].legend()
    axs[0].set_ylim(1e-4, 1e3)
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Spectral Density (dB)')
    axs[1].legend()
    show_data('FFT_sines_periodogram.jpg')
    

if __name__ == '__main__':
    data = generate_data()
    
    power_spectrum(*data)
    # Equivalent to: 
    # power_spectrum(data[0], data[1], data[2])
    
