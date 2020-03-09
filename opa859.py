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

import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.interpolate

import tiasim

def opamp_gain(f, gain, bw):
    #function out = opampgain(x, f)
    return numpy.abs( gain / (1.0+ 1j * f/bw ) )
    #out = abs( x(1) ./ (1+ 1i .* f./x(2) ) );
    pass

def opamp_phase(f, gain, bw):
    #function out = opampphase(x, f)
    return numpy.angle( gain / (1.0+ 1j * f/bw ) )

def opamp_v_noise(f, a0, a1):
    # noise model, wide-band flat noise + 1/f noise
    return a0+a1/numpy.sqrt(f)

def opamp_i_noise(f, a0, a1):
    # noise model, wide-band flat noise + 1/f noise
    return a0*numpy.sqrt(f)+a1*f
    
# photodiode transimpedance model
q=1.609e-19;    # electron charge
kB=1.38e-23;    # Boltzmann constant
T=273+25;       # Temperature


# https://www.ti.com/lit/ds/symlink/opa859.pdf

# open loop gain of amp
#tmp=load('opa657_absA.dat');
tmp=numpy.genfromtxt('opa859/opa859_gain.txt',delimiter=",")
#print tmp
f=numpy.array(tmp[:,0])*1e3 # to Hz
A=numpy.array(tmp[:,1])
A = 10.0**(A/20.0) # from dB to V/V gain

plt.figure(figsize=(12,10))
plt.subplot(2,2,1)
plt.title('Amp gain')
plt.semilogx(f,20.0*numpy.log10(A),'o',label='Datasheet') # plot in dB
plt.grid()
plt.ylabel('Gain (dB)')
plt.xlabel('Frequency (Hz)')


#x0 = [10**(95.0/20.0), 5e4];

#x, xcov = curve_fit(opamp_gain,f[:-6], A[:-6], p0=x0);
#print "fit AOL gain/f ",x
# 

#%pa = polyfit(f,10.^(A./20),4);
#hold on
#print opamp_gain(f,x[0],x[1])
opa = tiasim.OPA859()
gbwp = opa.GBWP


fm = numpy.logspace(1,9,30)
plt.semilogx( fm, 20*numpy.log10( numpy.abs( opa.gain(fm) ) ),'-',label='TIASim OPA859 model')

fg=numpy.logspace(5,9,20)

plt.semilogx( fg, 20*numpy.log10( gbwp/fg ),'--',label='GBWP = %.2g Hz' % gbwp)

#aol_db = 20*numpy.log10(x[0])
#plt.semilogx(f,20.0*numpy.log10( opamp_gain(f,x[0],x[1]) ),'--', label='%.f dB, %.2f kHz'%(aol_db, x[1]/1e3))
#hold off
#% break
plt.legend()


# phase
plt.subplot(2,2,2)
plt.title('Amp phase')
plt.semilogx( fm,  360*numpy.angle( opa.gain(fm) )/(2*numpy.pi) ,'-',label='TIASim OPA859 model')
plt.grid()
plt.ylabel('Phase / degrees')
plt.legend()


# voltage noise of amp
tmp=numpy.genfromtxt('opa859/opa859_vn.txt', delimiter=',');
e_F=tmp[:,0] # Hz
e_N=tmp[:,1]*1e-9  # V / sqrt(Hz), input file in nV/sqrt(Hz)
#e2_N=e_N**2;  # V^2 / Hz
print "voltage noise ", e_N
#e2_N = e2_N[-1] # pick last value
plt.subplot(2,2,3)
plt.title('Amp voltage noise')
plt.loglog(e_F, e_N,'o',label='datasheet')
f_int=numpy.logspace(3,numpy.log10(max(f)),1000);

noise0 = [0.8e-9, 4e-8];

vnoise, vnoisecov = curve_fit(opamp_v_noise,e_F, e_N, p0=noise0);
#pn = numpy.polyfit(e_F,e_N,3)
print "fit vnoise: ", vnoise
#e_model = opamp_v_noise(f_int, vnoise[0], vnoise[1]) # Vspline(f_int)
#plt.loglog(f_int,e_model,'--',label='model')
#plt.loglog(f_int,opamp_v_noise(f_int, 3.3e-9, 93e-8),'--',label='model2')

plt.loglog(f_int, opa.voltage_noise(f_int),'-',label='TIASim OPA859')

#plt.loglog(f_int,numpy.polyval(pn, f_int),'--',label='model3')

plt.legend()
plt.grid()
plt.ylabel('V/sqrt(Hz)')
#plt.show()

# current noise of amp
tmp=numpy.genfromtxt('opa859/opa859_in.txt', delimiter=',');
i_F=tmp[:,0] # Hz
i_N=tmp[:,1]*1e-15  # A / sqrt(Hz)
#e2_N=e_N**2;  # V^2 / Hz
print "voltage noise ", i_N
#e2_N = e2_N[-1] # pick last value
plt.subplot(2,2,4)
plt.title('Amp current noise')
plt.loglog(i_F, i_N,'o',label='datasheet')
f_int=numpy.logspace(3,numpy.log10(max(f)),1000);

noise0 = [1e-17, 3e-20];

inoise, inoisecov = curve_fit(opamp_i_noise,i_F, i_N, p0=noise0);
#pn = numpy.polyfit(e_F,e_N,3)
print "fit inoise: ", inoise
i_model = opamp_i_noise(f_int, inoise[0], inoise[1]) # Vspline(f_int)
pi = numpy.polyfit(i_F, i_N, 4)
i_model2 = opamp_i_noise(f_int, 1e-17, 3e-20)  #numpy.polyval(pi, f_int)
#plt.loglog(f_int,i_model,'--',label='model')
#plt.loglog(f_int,i_model2,'--',label='model2')
plt.loglog(f_int, opa.current_noise(f_int),'-',label='TIASim OPA859')

#plt.loglog(f_int,numpy.polyval(pn, f_int),'--',label='model3')

plt.legend()
plt.grid()
plt.ylabel('A/sqrt(Hz)')
plt.show()
