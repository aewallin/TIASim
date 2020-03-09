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

q=1.609e-19;    # electron charge
kB=1.38e-23;    # Boltzmann constant
T=273+25;       # Temperature

class IdealOpamp():
    def __init__(self):
        self.AOL_gain = 1e6
        self.AOL_bw = 1e5
        self.GBWP = 10e9
                
    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) 
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        return .0001e-9 
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        return 0.1e-15
    
    def input_capacitance(self):
        cm = 0.001e-12
        diff= 0.001e-12
        return cm+diff 

class OPA855():
    """
         8-GHz Gain Bandwidth Product, Gain of 7-V/V Stable, Bipolar Input Amplifier
         https://www.ti.com/lit/ds/symlink/opa855.pdf
    """
    def __init__(self):
        self.AOL_gain = 10093.79531159  
        self.AOL_bw = 941445.81175752
        self.GBWP = 8e9
        
    def gain(self,f):
        """ gain """
        #return numpy.abs( self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) )
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) 
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        a0 = 0.98e-9
        a1 = 60e-9
        return a0+a1/numpy.sqrt(f) 
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 2.5e-12
        i1 = 1000e-12
        
        return i0+i1/numpy.sqrt(f) 
    
    def input_capacitance(self):
        cm = 0.6e-12
        diff= 0.2e-12
        return cm+diff 
        

class OPA858():
    """
        5.5 GHz Gain Bandwidth Product, Decompensated Transimpedance Amplifier with FET Input
        https://www.ti.com/lit/ds/symlink/opa858.pdf
    """
    def __init__(self):
        self.AOL_gain =  6645.80643846   # pow(10,66.0/20.0)
        self.AOL_bw = 1091348.67318369
        self.GBWP = 5.5e9
        
    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) 
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        # fit vnoise:  [  2.15623045e-09   9.28064032e-07]

        a0 = 2.5e-9
        a1 = 72e-8
         
        return a0+a1/numpy.sqrt(f) 
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 3.22683744e-20

        return i0*f
    
    def input_capacitance(self):
        cm = 0.6e-12
        diff= 0.2e-12
        return cm+diff 


class OPA859():
    """
        1.8 GHz Unity-Gain Bandwidth, 3.3-nV/sqrt(Hz), FET Input Amplifier
    """
    def __init__(self):
        self.AOL_gain = 2152.02871113 
        self.AOL_bw = 519231.04490493
        self.GBWP = 1.8e9
        
    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) 
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        # FIXME, not a good fit to the datasheet
        a0 = 3.3e-9      
        a1 =  93e-8
         
        return a0+a1/numpy.sqrt(f) 
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        i0 = 1e-17
        i1 = 3e-20
        return i0*numpy.sqrt(f)+i1*f
    
    def input_capacitance(self):
        cm = 0.62e-12
        diff= 0.2e-12
        return cm+diff 

class OPA657():
    """
        1.6-GHz, Low-Noise, FET-Input Operational Amplifier
        https://www.ti.com/lit/ds/symlink/opa657.pdf
        
        Gain of +7 stable 
    """
    def __init__(self):
        self.AOL_gain = pow(10,75.0/20.0) 
        self.AOL_bw = 10*45626.55598007
        self.AOL_pole = 300e6
        self.GBWP = 1.6e9
        
    def gain(self,f):
        """ gain """
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) * (1.0/ (1.0+ 1j * f/self.AOL_pole ) )
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        #return numpy.array(len(f)*[4.8e-9]) # FIG 13
        a0 = 4.8e-9      
        a1 =  93e-9
        return a0+a1/pow(f,0.5) 
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        return 1.3e-15
    
    def input_capacitance(self):
        cm = 0.7e-12
        diff= 4.5e-12
        return cm+diff 

class OPA847():
    """
        3.8GHz GBWP  Ultra-Low Noise, Voltage-Feedback, Bipolar Input 
        stable for gains >=12
        https://www.ti.com/lit/ds/symlink/opa847.pdf
    """
    def __init__(self):
        self.AOL_gain = 57666.09586591  
        self.AOL_bw = 65178.06837912
        self.GBWP = 3.9e9
        
    def gain(self,f):
        """ gain """
        #return numpy.abs( self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) )
        return  self.AOL_gain / (1.0+ 1j * f/self.AOL_bw ) 
        
    def voltage_noise(self,f):
        """ amplifier input voltage noise in V/sqrt(Hz) """
        return numpy.array(len(f)*[0.85e-9])
        
    def current_noise(self,f):
        """ amplifier input current noise in A/sqrt(Hz) """
        return numpy.array(len(f)*[2.7e-12])
    
    def input_capacitance(self):
        cm = 1.7e-12
        diff= 2.0e-12
        return cm+diff 

class S5973():
    """
        https://www.hamamatsu.com/resources/pdf/ssd/s5971_etc_kpin1025e.pdf
    """
    def __init__(self):
        self.capacitance = 1.6e-12
        self.responsivity = 0.4 # A/W
    def current(self, P):
        """ photocurrent (A) produced by input optical power P """
        return self.responsivity*P

class FDS015():
    def __init__(self):
        self.capacitance = 0.65e-12
        self.responsivity = 0.4
    def current(self, P):
        """ photocurrent produced by input optical power P """
        return self.responsivity*P
        
        

class TIA():
    def __init__(self, opamp, diode, R_F, C_F=None, C_F_parasitic=None):
        """ build TIA from given opamp, diode and feedback resistance/capacitance """
        self.opamp = opamp
        self.diode = diode
        self.R_F = R_F # feedback resistance
        self.C_tot = self.diode.capacitance + self.opamp.input_capacitance() # total source capacitance
        if C_F_parasitic:
            self.C_F_parasitic=C_F_parasitic
        else:
            self.C_F_parasitic=0.01e-12 # minimum capacitance over R_F
        
        if C_F:
            self.C_F = C_F + self.C_F_parasitic
        else:
            self.set_CF()
        
    
    def ZF(self, f):
        # feedback impedance R_F || C_F
        w = 2.0*numpy.pi*f
        return self.R_F / ( 1j*self.R_F*self.C_F*w + 1.0 ); 
    
    def ZM(self,f):
        # closed loop transimpedance, Hobbs (18.15)
        A = self.opamp.gain(f)
        w = 2.0*numpy.pi*f
        
        return A*self.ZF(f) / ( 1.0 + A + 1j*w*self.ZF(f)*(self.C_tot) ); 
    
    def amp_current_noise(self, f):
        """
            output-referred amplifier current noise, in V/sqrt(Hz)
            computed as amplifier input-referred noise thru transimpedance
            
        """
        return self.opamp.current_noise(f)*numpy.abs(self.ZM(f))   
 
    def amp_voltage_noise(self, f):
        """
            output referred amplifier voltage noise, in V/sqrt(Hz)
        """
        A = self.opamp.gain(f)
        w = 2.0*numpy.pi*f
        Avcl = A / (1.0+A/(1.0+1j*w*self.ZF(f)*(self.C_tot)))  # closed loop voltage gain
        return self.opamp.voltage_noise(f) * numpy.abs(Avcl) 
        
    def johnson_noise(self, f):
        """
            output-referred voltage noise due to R_F, in V/sqrt(Hz)
            Computed as johnson current noise thru transimpedance
        """
        return numpy.sqrt( 4*kB*T/self.R_F ) * numpy.abs(self.ZM(f)) 
    
    def shot_noise(self, P, f):
        """
            output-referred shot noise due to optical power P, in V/sqrt(Hz)
            shot-noise current thru transimpedance
        """
        I_PD = self.diode.current(P)
        q=1.609e-19
        return numpy.sqrt(2.0*q*I_PD) * numpy.abs(self.ZM(f)) 
    
    def dark_noise(self, f):
        """
            output referred TIA noise without any shot noise, in V/sqrt(Hz)
            quadrature sum of voltage, current, and RF johnson noise
        """
        c2 = self.amp_current_noise(f)**2
        v2 = self.amp_voltage_noise(f)**2
        j2 = self.johnson_noise(f)**2
        return numpy.sqrt( c2+v2+j2 )
    
    def bright_noise(self,P,f):
        """
            output referred TIA bright-noise with optical power P
            dark_noise + shot noise of photocurrent.
            Photocurrent computed as optical power times photodiode responsivity
        """
        d2 = self.dark_noise(f)**2
        s2 = self.shot_noise(P,f)**2
        return numpy.sqrt( d2+s2 )
    
    def dc_output(self, P, f):
        I_PD = self.diode.current(P)
        return I_PD*numpy.abs(self.ZM(f))
    
    def bandwidth_approx(self):
        f3db = numpy.sqrt( self.opamp.GBWP /(2*numpy.pi*self.R_F*self.C_tot))
        return f3db
        
    def bandwidth(self):
        """ find the -3 dB bandwidth of the TIA """
        f = numpy.logspace(1,10,1e6)
        zm = numpy.abs( self.ZM(f) )
        try:
            ind = min( min(numpy.where( zm < zm[0]/numpy.sqrt(2.0)) ) )
            #print zm[0], zm[ind], zm[ind]/zm[0]
            f_3dB= f[ind]
            return f_3dB
        except:
            print "WARNING -3dB point not found"
            return -1
    
    def set_CF(self):
        """ 
            set optimum value for C_F
            C_opt = sqrt( C_source / 2*pi*GbWP*R_F )
        """
        C_optimal = numpy.sqrt( self.C_tot / (2.0*numpy.pi*self.opamp.GBWP*self.R_F))
        if C_optimal > self.C_F_parasitic:
            self.C_F = C_optimal
        else:
            self.C_F = self.C_F_parasitic
            
        print "optimum: %.3f pF, set C_F= %.3f pF" % (C_optimal*1e12, self.C_F*1e12)

    def cnr(self, f):
        """ carrier to noise ratio """
        P = 1.0
        c = 10.0*numpy.log10( self.bright_noise(P, f) )
        n = 10.0*numpy.log10( self.bright_noise(0.0, f) )
        #print c,n
        return c,n,c-n

if __name__ == "__main__":
    P = 5*25e-6
    #R_F = 1e3
    R_F = 1.5e3 # 4.6e3
    C_F = 0.1e-12
    #tia = TIA( OPA847(), S5973(), R_F, C_F ) # shot noise limit 200uW, 1kOhm, 390 MHz
    #tia = TIA( IdealOpamp(), FDS015(), R_F, C_F )
    tia = TIA( OPA859(), FDS015(), R_F  , None, 0.05e-12) 
    #tia = TIA( OPA657(), S5973(), R_F  , C_F, 0.05e-12) 
    #tia = TIA( OPA858(), S5973(), R_F  , None, 0.25e-12) 
    #tia.C_F = 0.4e-12 # set manually
    print "P optical ", P*1e6 , " uW"
    print "Photocurrent ", P*0.4, " uA"
    print "DC signal ", R_F*P*0.4, " V"
    
    print "I shot %.2g A/sqrt(Hz)" % (numpy.sqrt(0.4*P*q*2.0))
    print "R_F voltage ", tia.dc_output(P,100e3)
    print "Bandwidth ", tia.bandwidth()/1e6, " MHz"
 
    print "simple bw model ", tia.bandwidth_approx()/1e6, " MHz"

    f = numpy.logspace(3,9.5,100)
    print "ZM"
    zm = numpy.abs( tia.ZM(f) )
    # transimpedance
    plt.figure()
    plt.loglog(f,zm,'-')
    bw = tia.bandwidth()
    plt.loglog( bw, numpy.abs(tia.ZM( bw )), 'o')
    plt.loglog( 0.1*bw, numpy.abs(tia.ZM( 0.1*bw )), 'o')
    plt.text( bw, numpy.abs(tia.ZM( bw )), '%.1f MHz'%(bw/1e6))
    plt.ylabel('Transimpedance / Ohm')
    
    ax2 = plt.twinx()
    ax2.loglog(f,tia.dark_noise(f),'--') 
    ax2.loglog(f,tia.bright_noise(P, f))
    plt.grid()

    # shot-noise-ratio
    plt.figure()
    dark = tia.dark_noise(f)
    bright = tia.bright_noise(P,f)
    
    def shot_noise_ratio_dB(fn):
        f3db_shot = 20*numpy.log10( tia.shot_noise(P,fn) )
        f3db_dark = 20*numpy.log10( tia.dark_noise(fn) )
        return f3db_shot - f3db_dark 
    
    #plt.semilogx( f, 20*numpy.log10( bright )-20*numpy.log10(dark),'-')
    plt.semilogx( f, shot_noise_ratio_dB(f),'-')
    
    plt.semilogx( tia.bandwidth(), shot_noise_ratio_dB(tia.bandwidth()) ,'o',label='f_-3dB')
    plt.semilogx( 0.1*tia.bandwidth(), shot_noise_ratio_dB(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
    
    plt.ylabel('shot-noise/amp-noise ratio / dB')
    plt.grid()
    
    # output voltage noise
    plt.figure()
    print "amp_i"
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
    plt.loglog( tia.bandwidth(), tia.dark_noise(tia.bandwidth()),'o',label='f_-3dB')
    plt.loglog( 0.1*tia.bandwidth(), tia.dark_noise(0.1*tia.bandwidth()),'o',label='0.1*f_-3dB')
    
    plt.ylim((1e-9,1e-7))
    plt.grid()
    plt.legend()
    
    def v_to_dbm(v_psd, RBW = 1.0, termination=True):
        v2_psd = v_psd*v_psd # V^2 / Hz
        # P = UI = U^2 / R
        p_psd = v2_psd / 50.0 # W / Hz
        dbm = 10.0*numpy.log10( RBW*p_psd / 1.0e-3)
        if termination:
            dbm = dbm - 6.0 # 50-ohm termination halves voltage, so -6dB power
        return dbm
    
    # load experimental data
    d = numpy.genfromtxt('/home/anders/Dropbox/2020-01-18_circular_tia/CSV1.csv',comments='#',delimiter=',')
    print d
    df = d.T[0]
    d_bright = d.T[1]
    d_dark = d.T[2]
    d_sa = d.T[3]
        
    plt.figure()
    plt.plot(df, d_bright)
    plt.plot(df, d_dark)
    plt.plot(df, d_sa)

    rbw = 6*3e3
    for p in 1e-6*numpy.logspace(-1,6,6):
        bright = v_to_dbm( tia.bright_noise(p, f), RBW = rbw)
        plt.plot(f,bright,label='P=%.1f uW'%(p*1e6))
        
    plt.xlim((10e6,100e6))
    plt.xlabel('Frequency / Hz')
    plt.ylabel('dBm / RBW=%.1g Hz' % rbw)
    plt.grid()
    plt.legend()
    plt.show()

"""
amps = [('OPA847',0.85e-9, 2.7e-12),  # V/sqrt(Hz), A/sqrt(Hz)
       ('LMH6629',0.69e-9, 2.6e-12),  # V/sqrt(Hz), A/sqrt(Hz)
        ('OPA657',4.8e-9, 1.3e-15)
        ]
        
plt.figure()
for a in amps:
    plt.loglog(a[1], a[2],'o',label=a[0])
#plt.loglog(lmh6629[0], lmh6629[1],'o',label='lmh6629')

plt.loglog([1e-10, 10e-9], 2*[shot(1e-6)],'--',label='1uW')
plt.loglog([1e-10, 10e-9], 2*[shot(10e-6)],'--',label='10uW')
plt.loglog([1e-10, 10e-9], 2*[shot(100e-6)],'--',label='100uW')
plt.loglog([1e-10, 10e-9], 2*[shot(1000e-6)],'--',label='1mW')

plt.legend()

plt.ylabel('A/sqrt(Hz)')
plt.xlabel('V/sqrt(Hz)')

plt.grid()
plt.show()
"""
