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

opa = tiasim.OPA818()
#opa = tiasim.OPA855()
gbwp = opa.GBWP

Rf = 300
# G = 1 + Rf/Rg
# Rg = Rf/(G-1)
Rg = 33
ni = tiasim.NonInvertingAmp( opa, Rf, Rg )

f = numpy.logspace(6,9,100)
Av = ni.gain(f)
#print(f)

plt.figure()
plt.subplot(1,2,1)
ni.Rg = ni.Rf/(7-1)
g7 = tiasim.gain_to_db( numpy.abs(ni.gain(f))) 
plt.semilogx(f, g7, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )

ni.Rg = ni.Rf/(10-1)
g10 = tiasim.gain_to_db( numpy.abs(ni.gain(f))) 
#plt.semilogx(f, g10, label='G = %.1f V/V'%ni.gain_nominal())
plt.semilogx(f, g10, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )

ni.Rg = ni.Rf/(20-1)
g20 = tiasim.gain_to_db( numpy.abs(ni.gain(f)))
#plt.semilogx(f,  g20, label='G = %.1f V/V'%ni.gain_nominal())
plt.semilogx(f, g20, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )

ni.Rf=3e3
ni.Rg = ni.Rf/(50-1)
g50 = tiasim.gain_to_db( numpy.abs(ni.gain(f))) 
#plt.semilogx(f, g50 , label='G = %.1f V/V'%ni.gain_nominal())
plt.semilogx(f, g50, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )

ni.Rf=3e3
ni.Rg = ni.Rf/(100-1)
g100 = tiasim.gain_to_db( numpy.abs(ni.gain(f))) 
#plt.semilogx(f, g100, label='G = %.1f V/V'%ni.gain_nominal())
plt.semilogx(f, g100, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )

ni.Rf=6e3
ni.Rg = ni.Rf/(200-1)
g200 = tiasim.gain_to_db( numpy.abs(ni.gain(f))) 
plt.semilogx(f, g200, label='G = %.1f V/V = %.1f dB, RF=%.4g Ohm, RG=%.4g Ohm'%(ni.gain_nominal(), tiasim.gain_to_db( ni.gain_nominal() ), ni.Rf, ni.Rg))
plt.text( ni.bandwidth(), tiasim.gain_to_db(ni.gain_nominal())-3, "%.1f MHz"% (ni.bandwidth()/1e6) )


plt.grid()
plt.legend()
plt.ylabel('Gain / dB')
plt.xlabel('Frequency / Hz')
plt.title('OPA818 non-inverting amplifier')

plt.subplot(1,2,2)
plt.semilogx(f, g7 - tiasim.gain_to_db(7) , label='G = 7 V/V')


plt.semilogx(f, g10 - tiasim.gain_to_db(10), label='G = 10 V/V' )
plt.semilogx(f, g20 - tiasim.gain_to_db(20), label='G = 20 V/V' )
plt.semilogx(f, g50 - tiasim.gain_to_db(50), label='G = 50 V/V' )
plt.semilogx(f, g100 - tiasim.gain_to_db(100), label='G = 100 V/V' )
plt.grid()
plt.ylim((-12,3))
plt.ylabel('Normalized gain / dB')
plt.xlabel('Frequency / Hz')
plt.legend()



plt.show()
