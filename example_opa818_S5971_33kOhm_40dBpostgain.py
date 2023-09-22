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

    """
    P = 1e-3
    R_F = 33e3
    C_F =  0.2e-12 # 0.08e-12 # None # #  # .6e-12 # None # None # 0.2e-12
    C_parasitic = 0.02e-12
    
    diode = tiasim.S5971()
    diode.responsivity=0.15 # for 422nm
        
    #opamp = tiasim.OPA657()
    #opamp.AOL_gain = pow(10,70.0/20.0) # NOTE: modify to make it fit data!?
    # this could be because of capacitive load on the output??
    # MMCX connector on PCB, followed by ca 150mm thin coax, to SMA-connector.    
    #tia2 = tiasim.TIA( opamp, diode, R_F  , C_F, C_parasitic) 
    
    ## new detector with OPA818
    #RF2 = 33e3
    #CF2 = 0.15e-12
    #CP2 = 0.02e-12
    tia = tiasim.TIA( tiasim.OPA818(), diode, R_F, C_F, C_parasitic)
    
    
    # postgain, non-inverting configuration
    Rf = 3000
    # G = 1 + Rf/Rg
    # Rg = Rf/(G-1)
    Rg = 33
    ni = tiasim.NonInvertingAmp( tiasim.OPA818(), Rf, Rg )

    f = numpy.logspace(3,8,600)
    bw = tia.bandwidth() # bandwidth
    zm = numpy.abs( tia.ZM(f) ) # transimpedance
    
    # load experimental data, old OPA857 detector
    d = numpy.genfromtxt('measurement_data/2023-09-22_opa818_s5791_33kohm_40dbpostgain.csv',comments='#',delimiter=',')
    df = d.T[0]
    d_bright = d.T[3]
    d_bright2 = d.T[1]
    d_dark = d.T[2]
    d_sa = d.T[4]
    

 
    
    print( "P optical ", P*1e6 , " uW")
    print( "Photocurrent ", P*diode.responsivity, " uA")
    print( "DC signal ", R_F*P*diode.responsivity, " V")
    
    print( "I shot %.2g A/sqrt(Hz)" % (numpy.sqrt(diode.responsivity*P*tiasim.q*2.0)))
    print( "R_F voltage ", tia.dc_output(P,100e3))
    print( "Bandwidth ", bw/1e6, " MHz")
 
    print( "simple bw model ", tia.bandwidth_approx()/1e6, " MHz")


    # transimpedance plot
    plt.figure()
    plt.subplot(2,2,1)
    #plt.loglog(f,zm,'-', label='OPA657 Transimpedance')
    plt.loglog(f,numpy.abs( tia.ZM(f) ),'-', label='OPA818 Transimpedance')
        
    plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o',label='-3 dB BW')
    
    plt.loglog(f,  numpy.abs(ni.gain(f)),label='postgain' )
    plt.loglog(f,  numpy.abs( tia.ZM(f) )*numpy.abs(ni.gain(f)),label='total' )
    
    #plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o',label='BW/10')
    plt.text( bw, numpy.abs(tia.ZM( bw )), '%.3f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    plt.xlabel('Frequency / Hz')
    
    plt.legend(loc='lower left')
    plt.grid()
    plt.title('Transimpedance')
    
    # output voltage noise
    #plt.figure()
    plt.subplot(2,2,2)
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

    plt.loglog(f,bright,label='Bright, P=%f uW'%(P*1e6))
    plt.loglog( tia.bandwidth(), tia.dark_noise(tia.bandwidth()),'o',label='f_-3dB = %.3f MHz'%(bw/1e6))
    #plt.loglog( 0.1*tia.bandwidth(), tia.dark_noise(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
    
    plt.ylim((1e-9,1e-5))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Output-referred voltage noise / V/sqrt(Hz)')
    plt.grid()
    plt.legend()
    plt.title('Output-referred noise')
    
    ##############################################
    # plot measured data and compare to model
    # measurements through 10 dB coupler
    #plt.figure()

    plt.subplot(2,2,3)
    plt.plot(df, d_bright,'.',label='dark')
    plt.plot(df, d_bright2,'.',label='signal')
    plt.plot(df, d_dark,'.',label='bright, DC-output ca 0.5 V')
    plt.plot(df, d_sa,'.',label='SA floor')
       
    #plt.plot(df, d_sa,'o',label='Measured SA floor')

    rbw = 30e3
    # 10 V/V voltage-gain = 20 dB power gain
    #plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw)+postgain_db,'-',label='OPA657/38kOhm TIASim Dark')

    #r = RF2 / R_F
    #r_dB = 0 # 20*numpy.log10( r )
    plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f)*numpy.abs(ni.gain(f)), RBW = rbw),'-.',label='OPA818 TIASim Dark')

    
    for p in 1e-6*numpy.array([10,100, 0.5e5, 0.5e6]):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f)*numpy.abs(ni.gain(f)), RBW = rbw)
        #bright2 = tiasim.v_to_dbm( tia2.bright_noise(p, f), RBW = rbw)+postgain_db
        plt.plot(f,bright,label='OPA818 detector, TIASim P_shot =%.3g W'%(p))
        #plt.plot(f,bright2,'-.',label='TIASim P_shot =%.3g W'%(p))
    
    # johnson_noise(self, f)
    jn = tiasim.v_to_dbm( tia.johnson_noise(f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.plot(f,jn,'-',label='RF Johnson noise')

    plt.plot([25e6, 25e6],[-80, -30],'k--',label='25 MHz EOM frequency')
    
    #plt.xlim((1e5,100e6))
    plt.ylim((-65,10))
    
    #plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.title('S5793 photodiode, OPA818 38kOhm TIA (Cf+Cp=0.17 pF), 10 V/V postgain')
    #plt.title('S5793 photodiode, OPA818 33kOhm TIA, 10 V/V postgain')

    plt.grid()
    plt.legend()
    plt.xscale('linear')
    plt.xlim((1e5,100e6))

    plt.subplot(2,2,4)
    plt.semilogx(df, d_bright,'.',label='dark')
    plt.semilogx(df, d_bright2,'.',label='signal')
    plt.semilogx(df, d_dark,'.',label='bright, DC-output ca 0.5 V')
    plt.semilogx(df, d_sa,'.',label='SA floor')
       
    #plt.plot(df, d_sa,'o',label='Measured SA floor')

    rbw = 30e3
    postgain_db = 21 # 10 V/V voltage-gain = 20 dB power gain
    #plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f), RBW = rbw)+postgain_db,'-',label='OPA657/38kOhm TIASim Dark')

    #r = RF2 / R_F
    #r_dB = 0 # 20*numpy.log10( r )
    plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f)*numpy.abs(ni.gain(f)), RBW = rbw),'-.',label='OPA818 TIASim Dark')

    
    for p in 1e-6*numpy.array([10,100, 0.5e5, 0.5e6]):
        bright = tiasim.v_to_dbm( tia.bright_noise(p, f)*numpy.abs(ni.gain(f)), RBW = rbw)
        #bright2 = tiasim.v_to_dbm( tia2.bright_noise(p, f), RBW = rbw)+postgain_db
        plt.semilogx(f,bright,label='OPA818 detector, TIASim P_shot =%.3g W'%(p))
        #plt.plot(f,bright2,'-.',label='TIASim P_shot =%.3g W'%(p))
    
    # johnson_noise(self, f)
    jn = tiasim.v_to_dbm( tia.johnson_noise(f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.semilogx(f,jn,'-',label='RF Johnson noise')

    
    plt.semilogx([25e6, 25e6],[-80, -30],'k--',label='25 MHz EOM frequency')
    
    plt.xlim((1e5,500e6))
    plt.ylim((-65,10))
    
    #plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.title('S5793 photodiode, OPA818 38kOhm TIA, 10 V/V postgain')
    plt.grid()
    plt.legend()
    #plt.xscale('linear')
    plt.xlim((1e5,100e6))
    
    #%%
    
    plt.figure()
    plt.semilogx(df, d_sa,'.',label='SA floor')
    plt.semilogx(df, d_bright,'k.',label='Detector dark')
    plt.semilogx(df, d_dark,'.',label='Detector shot-noise, DC-output ca 0.55 V')
    plt.semilogx(df, d_bright2,'.',label='Signal')
    
    p=20e-3
    bright = tiasim.v_to_dbm( tia.bright_noise(p, f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.semilogx(f,bright,label='OPA818 detector, TIASim P_shot =%.3g mW'%(1e3*p))
    
    p=35
    bright = tiasim.v_to_dbm( tia.bright_noise(p, f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.semilogx(f,bright,label='TIASim ')
    
    
    plt.semilogx(f, tiasim.v_to_dbm( tia.bright_noise(0, f)*numpy.abs(ni.gain(f)), RBW = rbw),'-.',label='OPA818 TIASim Dark')

    plt.semilogx(f,jn,'-',label='RF Johnson noise')
    amp_v = tiasim.v_to_dbm( tia.amp_voltage_noise(f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.semilogx(f,amp_v,'-',label='OpAmp Voltage noise')
    amp_i = tiasim.v_to_dbm( tia.amp_current_noise(f)*numpy.abs(ni.gain(f)), RBW = rbw)
    plt.semilogx(f,amp_i,'-',label='OpAmp Current noise')
    
    plt.grid()
    plt.legend()
    plt.ylim((-70,10))
    plt.xlim((1e5,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.show()

"""

    ##########################3
    # Shot Noise levels
    plt.figure()
    #sidx = 5
    #plt.plot(dsf[sidx:-1], ds_bright[sidx:-1],'.',label='Bright, 0.5 VDC')
    #plt.plot(dsf[sidx:-1], ds_bright2[sidx:-1],'.',label='Bright, 0.1 VDC')
    #plt.plot(dsf[sidx:-1], ds_dark[sidx:-1],'.',label='Bright, 0.2 VDC')
    #plt.plot(dsf[sidx:-1], ds_bright3[sidx:-1],'.',label='Dark')
    rbw = 300000
    
    #plt.plot(dsf[sidx:-1], tiasim.v_to_dbm( tia.bright_noise(0, dsf[sidx:-1]), RBW = rbw)+postgain_db,'-.',label='OPA818 TIASim Dark')
    # P*R*RF * 0.5 * postgain = VDC
    # P = VDC / (R*RF*postgain*0.5)
    #P1 = 0.1 / (0.4*R_F*pow(10, postgain_db/20)*0.5)
    #plt.plot(dsf[sidx:-1], tiasim.v_to_dbm( tia.bright_noise(P1, dsf[sidx:-1]), RBW = rbw)+postgain_db,'-.',label='OPA818 TIASim Bright, 0.1 VDC = %g W'%P1)
    #P2 = 10e-6
    #plt.plot(dsf[sidx:-1], tiasim.v_to_dbm( tia.bright_noise(P2, dsf[sidx:-1]), RBW = rbw)+postgain_db,'-.',label='OPA818 TIASim Bright,  %g W'%P2)
    #P3 = 100e-6
    #plt.plot(dsf[sidx:-1], tiasim.v_to_dbm( tia.bright_noise(P3, dsf[sidx:-1]), RBW = rbw)+postgain_db,'-.',label='OPA818 TIASim Bright,  %g W'%P3)
    
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    #plt.title('S5793 photodiode, OPA657 38kOhm TIA, 10 V/V postgain')
    plt.grid()
    plt.legend()
    #plt.xscale('linear')
    #plt.xlim((1e6,250e6))
    plt.show()

    plt.show()
"""
