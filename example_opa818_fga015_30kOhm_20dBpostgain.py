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
        This example shows data from a photodetector built 2022-10.
        PCB:            2-stage TIA-board with AC and DC outputs
        Opamp:          OPA818, with OPA818 postgain (AC-output), and OPA657 postgain (DC-output)
        Transimpedance: 30 kOhm
        CF:             0.16 pF (adjusted based on measured spectra)
        Photodiode:     Thorlabs FGA015
        Bandwidth:      ca 44 MHz
    """
    P = 10e-6
    R_F = 30e3
    C_F =  0.15e-12 # 0.08e-12 # None # #  # .6e-12 # None # None # 0.2e-12
    C_parasitic = 0.01e-12
    
    diode = tiasim.FGA015()    
    opamp = tiasim.OPA818()
    tia = tiasim.TIA( opamp, diode, R_F  , C_F, C_parasitic) 
    
    
    f = numpy.logspace(3,9.5,600)
    bw = tia.bandwidth() # bandwidth
    zm = numpy.abs( tia.ZM(f) ) # transimpedance
    
  
    d = numpy.genfromtxt('measurement_data/2022-10-05_opa818_30k_20dB.csv',comments='#',delimiter=',')
    df = d.T[0]
    d_bright = d.T[3]
    d_dark = d.T[2]
    d_safloor = d.T[1]
    
 
    
    print( "P optical ", P*1e6 , " uW")
    print( "Photocurrent ", P*0.4, " uA")
    print( "DC signal ", R_F*P*0.4, " V")
    
    print( "I shot %.2g A/sqrt(Hz)" % (numpy.sqrt(0.4*P*tiasim.q*2.0)))
    print( "R_F voltage ", tia.dc_output(P,100e3))
    print( "Bandwidth ", bw/1e6, " MHz")
 
    print( "simple bw model ", tia.bandwidth_approx()/1e6, " MHz")


    # transimpedance plot
    plt.figure()
    plt.loglog(f,zm,'-', label='OPA657 Transimpedance')
    #plt.loglog(f,numpy.abs( tia2.ZM(f) ),'-', label='OPA818 Transimpedance')
        
    plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o',label='-3 dB BW')
    plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o',label='BW/10')
    plt.text( bw, numpy.abs(tia.ZM( bw )), '%.3f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    plt.xlabel('Frequency / Hz')
    
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
    
    ##############################################
    # plot measured data and compare to model
    plt.figure()
    plt.plot(df, d_bright,'o',label='Frequency response')
    plt.plot(df, d_dark,'o',label='dark')
    plt.plot(df, d_safloor,'o',label='SA floor')
    
    #plt.plot(ddf, dd_bright,'.',label='dark')
    #plt.plot(ddf, dd_bright2,'.',label='signal')
    #plt.plot(ddf, dd_dark,'.',label='bright, DC-output ca 0.5 V')
    #plt.plot(ddf, dd_bright3,'.',label='SA floor')
       
    #plt.plot(df, d_sa,'o',label='Measured SA floor')

    rbw = 30e3
    postgain_db = 20+3 # 10 V/V voltage-gain = 20 dB power gain
    #plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw)+postgain_db,'-',label='OPA657/38kOhm TIASim Dark')

    #r = RF2 / R_F
    #r_dB = 0 # 20*numpy.log10( r )

    
    for p in 1e-6*numpy.array([10,100, 1e3, 1e4, 0.5e5]):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f), RBW = rbw)+postgain_db
        #bright2 = tiasim.v_to_dbm( tia2.bright_noise(p, f), RBW = rbw)+postgain_db
        plt.plot(f,bright,label='OPA818/FGA015 detector, TIASim P_shot =%.3g W'%(p))
        #plt.plot(f,bright2,'-.',label='TIASim P_shot =%.3g W'%(p))
        
    for cf in [0.2e-12]:
        tia.C_F = cf
        plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw)+postgain_db,'k-.',label='OPA818 TIASim Dark')
    
    # johnson_noise(self, f)
    jn = tiasim.v_to_dbm( tia.johnson_noise(f), RBW = rbw)+postgain_db
    plt.plot(f,jn,'-',label='RF Johnson noise')

    plt.plot([25e6, 25e6],[-80, -30],'k--',label='25 MHz EOM frequency')
    
    plt.xlim((1e5,100e6))
    plt.ylim((-100,-20))
    
    #plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Output-referred noise, dBm / RBW=%.1g Hz' % rbw)
    plt.title('2022-10-06, FGA015 photodiode, OPA818 30 kOhm TIA, 23 dB postgain, C_F+Cp = 0.16 pF')
    plt.grid()
    plt.legend()
    plt.xscale('linear')
    #plt.xlim((1e6,250e6))


    ##########################3


    plt.show()
