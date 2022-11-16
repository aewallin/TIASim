"""
    This file is part of TIASim.
    https://github.com/aewallin/TIASim

    TIASim is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TIASim is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TIASim.  If not, see <https://www.gnu.org/licenses/>.
"""


import matplotlib.pyplot as plt
import numpy

import tiasim

if __name__ == "__main__":
    
    """
        This example shows data from a photodetector built 2021-09.
        PCB:            One-Inch-Photodetector, https://github.com/aewallin/One-Inch-Photodetector
        Opamp:          OPA818 (with BUF602 output-buffer)
        Transimpedance: 5.1 kOhm
        CF:             not installed
        Photodiode:     Fermionics FD80FC InGaAs, 0.4pF @ 5V
        Bandwidth:      ca 250 MHz
    """
    P = 2e-6
    R_F = 5.1e3

    C_F = 0.16e-12 # NOTE: no component installed, this is parasitic capacitance due to PCB-traces etc. (2021-09 version)
    C_F = 0.16e-12 # (2022-11 version)
    C_parasitic = 0.0e-12 
    diode = tiasim.FD80FC() 
    opamp = tiasim.OPA818()
    title = "FD80FC OPA818, RF=5k1, CF=0.16pF, (AW2021-09, 2022-11)"
    tia = tiasim.TIA( opamp, diode, R_F, C_F, C_parasitic) 
    f = numpy.logspace(3,9,500)
    bw = tia.bandwidth() # bandwidth estimate
    zm = numpy.abs( tia.ZM(f) ) # transimpedance

    # transimpedance plot
    plt.figure()
    plt.loglog(f,zm,'-', label='Fermionics FD80FC 0.4pF, RF=5k1, BW=%.1f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    plt.xlabel('Frequency / Hz')
    
    plt.legend()
    plt.grid()
    
    # output voltage noise plot
    plt.figure()
    amp_i = tia.amp_current_noise(f)
    amp_v = tia.amp_voltage_noise(f)
    john = tia.johnson_noise(f)
    dark = tia.dark_noise(f)
    shot = tia.shot_noise(P,f)
    bright = tia.bright_noise(P, f)
    plt.loglog(f,amp_i,label='OPA818 amp i-noise')
    plt.loglog(f,amp_v,label='OPA818 amp v-noise')
    plt.loglog(f, tia.dark_noise(f),label='Dark noise, OPA818')
    plt.loglog(f, tia.johnson_noise(f),'-.',label='R_F 5k1 Johnson')
    plt.ylim((1e-9,1e-5))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Output-referred voltage noise / V/sqrt(Hz)')
    plt.grid()
    plt.legend()
    
    rbw = 30e3 # spectrum analyzer RBW
    # load experimental data
    #d = numpy.genfromtxt('measurement_data/OPA818_FD80FC_5k1.csv',comments='#',delimiter=',')
    d = numpy.genfromtxt('measurement_data/2022-11-16_opa818_fd80fc_5k1.csv',comments='#',delimiter=',')
    df = d.T[0]
    d_SA = d.T[1] # spectrum analyzer floor
    d_dark = d.T[2] # detector dark noise
    d_bright1 = d.T[3] # detector bright, signal
    #d_bright2 = d.T[4]
    
    # plot measured data and compare to model
    plt.figure(figsize=(12,10))
    plt.plot(df, d_bright1,'ro',label='Measured response 1')
    #plt.plot(df, d_bright2,'o',label='Measured response 2 (10dB opt att.)')
    plt.plot(df, d_dark,'o',label='Measured dark')
    plt.plot(df, d_SA,'o',label='SA floor')
    
    plt.plot(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw, termination=True),'-',label='TIASim Dark')
    plt.plot(f, tiasim.v_to_dbm( numpy.sqrt( 4*tiasim.kB*tiasim.T/R_F )*R_F*numpy.ones((len(f),1)) , RBW = rbw),'--',label='RF thermal noise')
    
    # TIAsim bright response
    for p in 0.6e-6*numpy.logspace(3, 6.5, 5):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f), RBW = rbw)
        plt.plot(f,bright,label='TIASim P_shot =%.2g W'%(p))
    
    plt.plot([bw,bw], [-120,-20],  '--', label='f3dB = %.1f MHz' % (bw/1e6))
    plt.xlim((10e6, 0.5e9))
    plt.ylim((-120,-25))
    plt.title(title)
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.grid()
    plt.legend()
    plt.show()
    plt.show()


 
