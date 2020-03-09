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

import tiasim

opa = tiasim.OPA847()
gbwp = opa.GBWP


# read gain
d = numpy.genfromtxt('opa847/opa847_gain.txt', comments='#',delimiter=',')  
f = [x[0] for x in d]
aol = [pow(10,x[1]/20.0) for x in d]

# read phase
d = numpy.genfromtxt('opa847/opa847_phase.txt', comments='#', delimiter='\t')
fp = [x[0] for x in d]
phase = [x[1] for x in d]

# read vnoise
d = numpy.genfromtxt('opa847/opa847_v_noise.txt', comments='#', delimiter='\t')
fn = [x[0] for x in d]
vn = [x[1]*1e-9 for x in d]
print fn, vn

# read inoise
d = numpy.genfromtxt('opa847/opa847_i_noise.txt', comments='#', delimiter='\t')
fi = [x[0] for x in d]
vi = [x[1]*1e-12 for x in d]
print fi, vi


plt.figure(figsize=(12,10))
plt.subplot(2,2,1)
plt.semilogx(f, 20*numpy.log10(aol),'o',label='Datasheet')

fm = numpy.logspace(1,9,30)
plt.semilogx( fm, 20*numpy.log10( numpy.abs( opa.gain(fm) ) ),'-',label='TIASim OPA847 model')


fg=numpy.logspace(5,9,20)

plt.semilogx( fg, 20*numpy.log10( gbwp/fg ),'--',label='GBWP = %.2g Hz' % gbwp)


plt.legend()
plt.xlabel('Frequency / Hz')
plt.ylabel('Gain / dB')
plt.title('OPA847 Open-loop gain')
plt.grid()


#plt.figure()
plt.subplot(2,2,2)
plt.title('OPA847 Open-loop phase')
plt.semilogx(fp, phase,'o',label='Datasheet')
plt.semilogx( fm,  360*numpy.angle( opa.gain(fm) )/(2*numpy.pi) ,'-',label='TIASim OPA847 model')
plt.grid()
plt.xlabel('Frequency / Hz')
plt.ylabel('Phase / degrees')
plt.legend()

#plt.figure()
plt.subplot(2,2,3)
plt.title('OPA847 voltage noise')
plt.loglog(fn, vn,'o',label='Datasheet')
plt.loglog( fm,  opa.voltage_noise(fm) ,'-',label='TIASim OPA847 model')
plt.grid()
plt.xlabel('Frequency / Hz')
plt.ylabel('Voltage noise / V/sqrt(Hz)')
plt.ylim((1e-10,1e-7))
plt.legend()

plt.subplot(2,2,4)
plt.title('OPA847 current noise')
plt.loglog(fi, vi,'o',label='Datasheet')
plt.loglog( fm,  opa.current_noise(fm) ,'-',label='TIASim OPA847 model')
plt.grid()
plt.xlabel('Frequency / Hz')
plt.ylabel('Current noise / A/sqrt(Hz)')
plt.legend()
plt.ylim((1e-12,1e-10))
plt.show()
