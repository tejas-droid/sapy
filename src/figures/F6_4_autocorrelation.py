"""Generate an auto-correlation."""

# author:   Thomas Haslwanter
# date:     May-2020

import numpy as np
import matplotlib.pyplot as plt

# Import formatting commands if directory "Utilities" is available
import os
import sys
sys.path.append(os.path.join('..', 'Code_Quantlets', 'Utilities'))
try:
    from SAP_mystyle import set_fonts, show_data 
except:
    print('I could not load SAP_mystyle')


if __name__ =='__main__':

    # Generate the data
    signal = np.zeros(20)
    signal[7:10] = 1
    signal[14:17] = 1

    # Determine the auto-correlation 
    auto_corr = np.correlate(signal, signal, 'full')
    shift = np.arange(len(auto_corr)) - (len(signal)-1)

    # Plot the auto-correlation
    set_fonts(14)
    plt.plot(shift, auto_corr)
    plt.xlabel('Shift')
    plt.ylabel('Auto-Correlation')

    ax = plt.gca()
    ax.margins(x=0)

    # Show and save the result
    out_file = 'autoCorrelation.jpg'
    show_data(out_file)