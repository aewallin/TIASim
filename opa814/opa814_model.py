import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.interpolate

def opamp_gain(f, gain, bw):
    #function out = opampgain(x, f)
    #return numpy.abs( gain / (1.0+ 1j * f/bw ) )
    pole=800e6
    return numpy.abs( gain / (1.0+ 1j * f/bw ) * (1.0/ (1.0+ 1j * f/pole ) ) )

    #out = abs( x(1) ./ (1+ 1i .* f./x(2) ) );
    #pass

def opamp_phase(f, gain, bw):
    #function out = opampphase(x, f)
    #return numpy.angle( gain / (1.0+ 1j * f/bw ) )
    pole=800e6
    return numpy.angle( gain / (1.0+ 1j * f/bw ) * (1.0/ (1.0+ 1j * f/pole ) ) )

def opamp_v_noise(f, a0, a1):
    # noise model, wide-band flat noise + 1/f noise
    #return a0+a1/numpy.sqrt(f)
    return a0+a1/pow(f,0.6)

def opamp_i_noise_BJT(f, a0, a1):
    # noise model, wide-band flat noise + 1/f noise
    return a0+a1/numpy.sqrt(f)
    
def opamp_i_noise_FET(f, a0):
    # noise model
    return a0*f
    
# photodiode transimpedance model
q=1.609e-19;    # electron charge
kB=1.38e-23;    # Boltzmann constant
T=273+25;       # Temperature


#P     =  10e-6     # Optical power (W)
#P     =  50e-6     # Optical power (W)
#AW    =  .4       # Photodiode response (A/W)
#I_PD  = AW*P      # photocurrent (A)
#print "Optical ", P*1e6, " uW"
#print "Photocurrent ", I_PD*1e6, " uA"

# open loop gain of amp
#tmp=load('opa657_absA.dat');
tmp=numpy.genfromtxt('./opa814_Aol.txt', comments='#', delimiter=',')
#print tmp
f=numpy.array(tmp[:,0]) # to Hz
A=numpy.array(tmp[:,1]) 
print(f)

A = 10.0**(A/20.0) # from dB to V/V gain
print(A)

tmp=numpy.genfromtxt('./opa814_Aol_fi.txt', comments='#', delimiter=',')
#print tmp
ffi=numpy.array(tmp[:,0]) # to Hz
fi=numpy.array(tmp[:,1]) 


plt.figure()
plt.subplot(2,2,1)
plt.semilogx(f,20.0*numpy.log10(A),'o', label='Datasheet') # plot in dB

f_gbwp=numpy.logspace(5,8,100)
gbwp = 250e6
plt.semilogx(f_gbwp, 20.0*numpy.log10( gbwp/f_gbwp),'--',label='GBWP = %.1f GHz' % (gbwp/1e9) )

plt.grid(which='both')
plt.ylabel('Gain (dB)')
plt.xlabel('Frequency (Hz)')


x0 = [10**(95.0/20.0), 5e4];

x, xcov = curve_fit(opamp_gain,f, A, p0=x0);
print("fit AOL gain/f ",x)
# 

#%pa = polyfit(f,10.^(A./20),4);
#hold on
#print opamp_gain(f,x[0],x[1])

aol_db = 20*numpy.log10(x[0])
plt.semilogx(f,20.0*numpy.log10( opamp_gain(f,x[0],x[1]) ),'--', label='%.1f dB, %.3f kHz'%(aol_db, x[1]/1e3))
#hold off
#% break
plt.legend()
plt.title('OPA814 open loop gain')

plt.subplot(2,2,2)
plt.semilogx(ffi,fi,'o', label='Datasheet')
fplot=numpy.logspace(2,9,500)
plt.semilogx(fplot,360*opamp_phase(fplot,x[0],x[1])/(2*numpy.pi) ,'--', label='%.f dB, %.2f kHz'%(aol_db, x[1]/1e3))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (Degrees)')
plt.grid(which='both')
plt.title('OPA814 open loop phase')




#%%


#%% voltage noise of amp
tmp=numpy.genfromtxt('opa814_vn.txt', delimiter=',');
e_F=tmp[:,0]# Hz
e_N=tmp[:,1]*1e-9  # V / sqrt(Hz), input file in nV/sqrt(Hz)
#e2_N=e_N**2;  # V^2 / Hz
print( "voltage noise ", e_N)
#e2_N = e2_N[-1] # pick last value
#plt.figure()
plt.subplot(2,2,3)
plt.title('Amp voltage noise')
plt.loglog(e_F, e_N,'o',label='datasheet')
f_int=numpy.logspace(1,6,1000);

noise0 = [5.3e-9, 4e-8];

vnoise, vnoisecov = curve_fit(opamp_v_noise,e_F, e_N, p0=noise0);
#pn = numpy.polyfit(e_F,e_N,3)
print( "fit vnoise: ", vnoise)
e_model = opamp_v_noise(f_int, vnoise[0], vnoise[1]) # Vspline(f_int)
plt.loglog(f_int,e_model,'--',label='model')
#plt.loglog(f_int,opamp_v_noise(f_int, 5.3e-9, 860e-9),'--',label='model2')
#plt.loglog(f_int,numpy.polyval(pn, f_int),'--',label='model3')

plt.legend()
plt.grid(which='both')
plt.ylabel('V/sqrt(Hz)')
plt.xlabel('Frequency (Hz)')
#plt.show()

#%% current noise of amp
tmp=numpy.genfromtxt('opa814_in.txt', delimiter=',');
i_F=tmp[:,0] # Hz
i_N=tmp[:,1]*1e-15  # A / sqrt(Hz)
#e2_N=e_N**2;  # V^2 / Hz
print( "current noise ", i_N)
#e2_N = e2_N[-1] # pick last value
#plt.figure()

plt.subplot(2,2,4)
plt.title('Amp current noise')
plt.loglog(i_F, i_N,'o',label='datasheet')
f_int=numpy.logspace(4,8,1000);

noise0 = [2.5e-15];

inoise, inoisecov = curve_fit(opamp_i_noise_FET,i_F, i_N, p0=noise0);
#pn = numpy.polyfit(e_F,e_N,3)
print("fit inoise: ", inoise)
i_model = opamp_i_noise_FET(f_int, inoise[0]) # Vspline(f_int)
plt.loglog(f_int,i_model,'--',label='model')
#plt.loglog(f_int,opamp_i_noise_FET(f_int, 5e-15),'--',label='model2')
#plt.loglog(f_int,numpy.polyval(pn, f_int),'--',label='model3')

plt.legend()
plt.grid(which='both')
plt.ylabel('A/sqrt(Hz)')
plt.xlabel('Frequency (Hz)')
