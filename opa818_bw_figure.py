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

#opa = tiasim.OPA818()
#gbwp = opa.GBWP


# read gain
d = numpy.genfromtxt('opa818/bw_100k.txt', comments='#', delimiter=',')
cd_100k = [x[0] for x in d] # pF
bw_100k = [x[1] for x in d] # MHz
d = numpy.genfromtxt('opa818/bw_500k.txt', comments='#', delimiter=',')
cd_500k = [x[0] for x in d] # pF
bw_500k = [x[1] for x in d] # MHz

d = numpy.genfromtxt('opa818/bw_50k.txt', comments='#', delimiter=',')
cd_50k = [x[0] for x in d] # pF
bw_50k = [x[1] for x in d] # MHz

d = numpy.genfromtxt('opa818/bw_20k.txt', comments='#', delimiter=',')
cd_20k = [x[0] for x in d] # pF
bw_20k = [x[1] for x in d] # MHz


"""
# read phase
d = numpy.genfromtxt('opa818/opa818_AOL_phase.txt', comments='#', delimiter=',')
fp = [x[0]*1e6 for x in d]
phase = [x[1] for x in d]
print "Phase: ", fp, phase

# read vnoise
d = numpy.genfromtxt('opa818/opa818_vn.txt', comments='#', delimiter=',')
fn = [x[0]*1e6 for x in d]
vn = [x[1]*1e-9 for x in d] # from nV/sqrt(Hz)
print "Vnoise: ", fn, vn

# read inoise
d = numpy.genfromtxt('opa818/opa818_in.txt', comments='#', delimiter=',')
fin = [x[0]*1e6 for x in d]
inoise = [x[1]*1e-15 for x in d] # from fA/sqrt(Hz)
print "Inoise: ", fin, inoise
"""

plt.figure(figsize=(12,10))
#plt.subplot(2,2,1)
plt.plot(cd_500k, bw_500k,'o',label='Datasheet, RF=500k')
plt.plot(cd_100k, bw_100k,'o',label='Datasheet, RF=100k')
plt.plot(cd_50k, bw_50k,'o',label='Datasheet, RF=50k')
plt.plot(cd_20k, bw_20k,'o',label='Datasheet, RF=20k')

cd = numpy.linspace(0.5, 20, 20)
def TIA_BW(R_F):
    bw_100k = []
    #R_F=100e3
    C_F=None
    C_parasitic = 0.005e-12
    for c in cd:
        diode = tiasim.S5971()
        diode.capacitance = c*1e-12
        opamp = tiasim.OPA818()
        # note sqrt(2) factor here in addition to formula from tiasim.py
        C_optimal = numpy.sqrt(2)*numpy.sqrt( (diode.capacitance+opamp.input_capacitance()) / (2.0*numpy.pi*opamp.GBWP*R_F))
        tia = tiasim.TIA( opamp, diode, R_F  , C_optimal, C_parasitic)
        bw_100k.append( tia.bandwidth()/1e6) # MHz
    return bw_100k

plt.plot( cd, TIA_BW(500e3), '-', label='TIASim RF=500k')
plt.plot( cd, TIA_BW(100e3), '-', label='TIASim RF=100k')
plt.plot( cd, TIA_BW(50e3), '-', label='TIASim RF=50k')
plt.plot( cd, TIA_BW(20e3), '-', label='TIASim RF=20k')
#plt.plot( cd, TIA_BW(2e3), '-', label='TIASim RF=2k')
#plt.plot( cd, TIA_BW(1.5e3), '-', label='TIASim RF=1.5k')
#plt.plot( cd, TIA_BW(1e3), '-', label='TIASim RF=1k')
#plt.plot( [0.65, 0.65],[10,500],'r--',label="0.65 pF")


plt.legend()
plt.xlabel('PD capacitance / pF')
plt.ylabel('TIA BW / MHz')
plt.title('OPA818 TIA Bandwidth vs. source capacitance')
plt.grid()

plt.show()
