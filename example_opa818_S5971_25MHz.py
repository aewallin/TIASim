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
        This example shows data from a photodetector built 2020-01.
        PCB:            One-Inch-Photodetector, https://github.com/aewallin/One-Inch-Photodetector
        Opamp:          OPA657, SOT23-5
        Transimpedance: 10 kOhm
        Photodiode:     S5973
    """
    P = 3e-3
    R_F = 20e3
    C_F =  None # 0.1e-12 # None # 0.1e-12 # None # .6e-12 # None # None # 0.2e-12
    C_parasitic = 0.005e-12
    
    diode = tiasim.S5971()
    #diode.capacitance = 1.6e-12
    
    opamp = tiasim.OPA818()
    #o#pamp.AOL_gain = pow(10,65.0/20.0) # NOTE: modify to make it fit data!?
    # this could be because of capacitive load on the output??
    # MMCX connector on PCB, followed by ca 150mm thin coax, to SMA-connector.
    
    tia = tiasim.TIA( opamp, diode, R_F  , C_F, C_parasitic) 
    
    f = numpy.logspace(3,9.5,100)
    bw = tia.bandwidth() # bandwidth
    zm = numpy.abs( tia.ZM(f) ) # transimpedance
    z_phase = numpy.angle( tia.ZM(f) ) # transimpedance phase
    
    # load experimental data
    d = numpy.genfromtxt('measurement_data/OPA657_S5793_10kOhm.csv',comments='#',delimiter=',')


    df = d.T[0]
    d_bright = d.T[2]
    d_bright2 = d.T[1]
    d_dark = d.T[3]
    d_sa = d.T[4]
    #"""
    
    print( "P optical ", P*1e6 , " uW")
    print( "Photocurrent ", P*0.4, " uA")
    print( "DC signal ", R_F*P*0.4, " V")
    
    print( "I shot %.2g A/sqrt(Hz)" % (numpy.sqrt(0.4*P*tiasim.q*2.0)))
    print( "R_F voltage ", tia.dc_output(P,100e3))
    print( "Bandwidth ", bw/1e6, " MHz")
 
    print( "simple bw model ", tia.bandwidth_approx()/1e6, " MHz")


    # transimpedance plot
    plt.figure()
    plt.subplot(2,1,1)
    plt.loglog(f,zm,'-', label='Transimpedance')
    
    plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o',label='-3 dB BW')
    plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o',label='BW/10')
    plt.text( bw, numpy.abs(tia.ZM( bw )), '%.3f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    plt.xlabel('Frequency / Hz')
    
    plt.legend()
    plt.grid()
    plt.subplot(2,1,2)
    plt.semilogx(f,z_phase,'-', label='phase')
    plt.legend()
    plt.grid()
    
    # output voltage noise
    plt.figure()
    #print "amp_i"
    amp_i = tia.amp_current_noise(f)
    amp_v = tia.amp_voltage_noise(f)
    john = tia.johnson_noise(f)
    dark = tia.dark_noise(f)
    shot = tia.shot_noise(P,f)
    bright = tia.bright_noise(P, f)

    plt.loglog(f,amp_i,label='amp i-noise')
    plt.loglog(f,amp_v,label='amp v-noise')

    plt.loglog(f,john,'-.',label='R_F Johnson')
    plt.loglog(f,dark,label='Dark')
    plt.loglog(f,shot,label='shot noise P=%f uW'%(P*1e6))

    plt.loglog(f,bright,label='Bright')
    plt.loglog( tia.bandwidth(), tia.dark_noise(tia.bandwidth()),'o',label='f_-3dB = %.3f MHz'%(bw/1e6))
    plt.loglog( 0.1*tia.bandwidth(), tia.dark_noise(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
    
    plt.ylim((1e-9,1e-5))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Output-referred voltage noise / V/sqrt(Hz)')
    plt.grid()
    plt.legend()
    
    # plot measured data and compare to model
    plt.figure()
    plt.plot(df, d_bright,'o',label='1st Measured response')
    plt.plot(df, d_bright2,'o',label='2nd Measured response')
    plt.plot(df, d_dark,'o',label='Measured dark')
    plt.plot(df, d_sa,'o',label='Measured SA floor')

    rbw = 10e3
    plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw),'-',label='TIASim Dark')
    
    for p in 1e-6*numpy.logspace(1, 8.5, 4):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f), RBW = rbw)
        plt.plot(f,bright,label='TIASim P_shot =%.3g W'%(p))
    
    plt.xlim((1e5,500e6))
    plt.ylim((-120,-30))
    
    #plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.grid()
    plt.legend()
    plt.show()


 
