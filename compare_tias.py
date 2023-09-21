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
        experimental..
    """
    P = 10e-6
    R_F = 33e3
    C_F = None # 0.6e-12
    C_parasitic = 0.15e-12
    
    diode1 = tiasim.S5973()
    opamp1 = tiasim.OPA818()
    tia1 = tiasim.TIA( opamp1, diode1, R_F  , C_F, C_parasitic) 

    #diode1 = tiasim.FDS015()
    opamp2 = tiasim.OPA657()
    tia2 = tiasim.TIA( opamp2, diode1, R_F  , C_F, C_parasitic) 
    opamp3 = tiasim.LTC6268_10()
    tia3 = tiasim.TIA( opamp3, diode1, R_F  , C_F, C_parasitic) 
    
    
    tias = [tia2, tia1, tia3]
    f = numpy.logspace(6,9.5,300)
    


    # transimpedance plot
    plt.figure()
    for tia in tias:
        plt.subplot(1,2,1)
        bw = tia.bandwidth() # bandwidth
        zm = numpy.abs( tia.ZM(f) ) # transimpedance
    
        plt.loglog(f,numpy.abs( tia.ZM(f) ) ,'-', label='%s Transimpedance'%(tia.opamp.__class__.__name__))

        plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o',label='%s BW %.1f MHz'%(tia.opamp.__class__.__name__, bw/1e6))
        #plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o',label='BW/10')
        
        #ax = plt.gca()
        #ax2 = ax.twinx()
        #ax2.set_ylabel('Phase / degrees')
        #ax2.semilogx(f, numpy.angle( tia.ZM(f), deg=True ),'r-' )
        #plt.text( bw, numpy.abs(tia.ZM( bw )), '%.3f MHz'%(bw/1e6))
        plt.ylabel('Transimpedance / Ohm')
        plt.xlabel('Frequency / Hz')
        
        plt.legend()
        plt.grid()
        
        # output voltage noise
        plt.subplot(1,2,2)
        print("amp_i")
        amp_i = tia.amp_current_noise(f)
        amp_v = tia.amp_voltage_noise(f)
        john = tia.johnson_noise(f)
        dark = tia.dark_noise(f)
        shot = tia.shot_noise(P,f)
        bright = tia.bright_noise(P, f)

        #plt.loglog(f,amp_i,label='amp i-noise')
        #plt.loglog(f,amp_v,label='amp v-noise')

        #plt.loglog(f,john,'-.',label='R_F Johnson')
        plt.loglog(f,dark,label='%s Dark'%(tia.opamp.__class__.__name__))
        #plt.loglog(f,shot,label='shot noise P=%f uW'%(P*1e6))

        plt.loglog(f,bright,'--',label='%s Bright'%(tia.opamp.__class__.__name__))
        #plt.loglog( tia.bandwidth(), tia.dark_noise(tia.bandwidth()),'o',label='f_-3dB = %.3f MHz'%(bw/1e6))
        #plt.loglog( 0.1*tia.bandwidth(), tia.dark_noise(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
        
        plt.ylim((1e-9,1e-5))
        plt.xlabel('Frequency / Hz')
        plt.ylabel('Output-referred voltage noise / V/sqrt(Hz)')
        plt.grid()
        plt.legend()
    

    
    plt.show()


 
