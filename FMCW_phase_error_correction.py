''' Simulation of a Frequency-Modulated Continuous-Wave (FMCW) radar affected
by nonlinearity of the frequency sweep. Two similar algorithms are compared which 
correct for the effects of the nonlinearity: one 'narrowband' approximation by
Burgos-Garcia et al. [1], which is valid for phase errors which have a ripple
frequency much smaller than the square root of the chirp rate, and a 'wideband'
algorithm by Meta et al. [2] which is exact for temporally infinite chirps.

References
[1] Burgos-Garcia et al., Digital on-line compensation of errors induced by linear distortion in broadband FM radars, Electron. Lett. 39(1), 16 (2002)
[2] Meta et al., Range non-linearities correction in FMCW SAR, IEEE Conf. on Geoscience and Remote Sensing 2006, 403 (2006)
'''

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

def heaviside(t): return 0.5*(np.sign(t)+1)                 # Heaviside step function
def rectpuls(t): return heaviside(t+.5)-heaviside(t-.5)     # Rectangle function
    
def nextpow2(i):        # Returns the next power of of 2 greater than the input
    n=1.
    while n<i: n*=2.
    return n

def hamming(L):         # Hamming window (symmetric)
    N=L-1
    n=np.arange(L)
    w=0.54-0.46*np.cos(2*np.pi*n/N)
    return w    

def Fourier(x,fs,NFFT):     # Approximate Fourier transform on the interval (-fs/2,fs/2)
    k=np.arange(NFFT)
    N=len(x)
    T=N/fs
    f=(-.5+k/float(NFFT))*fs
    n=np.arange(N)
    return f, T/N*np.exp(1j*pi*f*T)*fft(x*(-1.)**n,NFFT)

def invFourier(X,fs,N):     # Approximate inverse Fourier transform on the interval (-T/2,T/2)
    NFFT=len(X)
    k=np.arange(NFFT)
    x=fs*np.exp(1j*np.pi*(N/2.-k))*ifft(X*np.exp(-1j*np.pi*k*N/NFFT),NFFT)
    x=x[:N]
    return x

def deskew(x,fs,alpha):     # Quadratic phase filter with a group delay of -f/alpha
    N=len(x)
    NFFT=int(nextpow2(N+fs**2/alpha))
    f,X=Fourier(x,fs,NFFT)
    Y=X*np.exp(1j*np.pi*f**2/alpha)
    y=invFourier(Y,fs,N)
    return y

fc=10.e9                # Center frequency (10 GHz)
B=50.e6                 # Chirp bandwidth (50 MHz)
T=500.e-6               # Chirp period (500 us)
alpha=B/T               # Chirp rate (100 GHz/s)

R=12.e3                 # Target range (12 km)
c=3.e8                  # Speed of light (in m/s)
tau=2.*R/c              # Two-way transit time (80 us)
fb=alpha*tau            # Beat frequency (8 MHz)
fs=25.e6                # Sampling frequency (25 MHz)
Ts=1./fs                # Sampling period (40 us)

Rmax=15.e3              # Instrumented range (15 km)
taumax=2.*Rmax/c        # Guard interval (100 us)

N=int(T/Ts)             # Number of samples per sweep period (12,500)
Np=int((T-taumax)/Ts)   # Number of processed samples (10,000)

''' Different types of phase error: sinusoidal, cubic, and quartic. Comment in/out to select. '''
Asl=0.5                 # Sidelobe ripple amplitude (in radians)
fsl=0.05*np.sqrt(alpha)  # Sidelobe ripple frequency 
def e(t): return Asl*np.cos(2.*np.pi*fsl*t)     # Sinusoidal phase error function

df_max=Asl*fsl          # Maximum frequency error with sinusoidal error function
''' Cubic phase error function (with same maximum frequency error) '''
#k3=2.*np.pi*df_max/(.5*T)**2  
#def e(t): return k3/3.*t**3     
    
''' Quartic phase error function (with same maximum frequency error) '''
#k4=2.*np.pi*df_max/(.5*T)**3
#def e(t): return k4/4.*t**4
    
def se(t): return np.exp(1j*e(t))       # Phase error function as complex exponential

''' Transmit and beat signal (without phase error) '''
def sTX_lin(t): return rectpuls(t)*np.exp(2j*np.pi*(fc*t+.5*alpha*t**2))
def sb_lin(t): return sTX_lin(t)*np.conj(sTX_lin(t-tau)) 

''' Transmit and beat signal (with phase error) '''
def sTX(t): return sTX_lin(t)*se(t)
def sb(t): return sTX(t)*np.conj(sTX(t-tau))

''' Time grid '''
n=np.arange(N)
t=(-N/2.+n)*Ts              
NFFT=int(nextpow2(N+fs**2/alpha))       # Number of FFT points required to avoid time-domain aliasing in the output of deskew filter

''' Phase error compensation algorithm '''
sIF_lin=sb_lin(t)                   # Ideal beat signal (without phase error)
sIF=sb(t)                           # Beat signal (with phase error)
sIF2=sIF*np.conj(se(t))             # Beat signal with transmitted non-linearities removed
sIF3=deskew(sIF2,fs,alpha)          # Deskew-filtered version of sIF2
sIF4n=sIF3*se(t)                    # Corrected beat signal in the narrowband approximation (Burgos-Garcia et al.)
sea=deskew(se(t),fs,alpha)          # Deskew-filtered error signal
sIF4w=sIF3*sea                      # Corrected beat signal for the wideband case (Meta et al.)

''' Calculate spectra '''
wIF=np.concatenate((np.zeros(N-Np),hamming(Np)))    # Window function for the uncorrected beat signal
f,SIF_lin=Fourier(wIF*sIF_lin,fs,NFFT)              # Ideal beat spectrum 
_,SIF=Fourier(wIF*sIF,fs,NFFT)                      # Actual beat spectrum

wIF4=np.concatenate((hamming(Np),np.zeros(N-Np)))   # Window function for the corrected beat signal
_,SIF4n=Fourier(wIF4*sIF4n,fs,NFFT)                 # Corrected IF spectrum (narrowband approximation)
_,SIF4w=Fourier(wIF4*sIF4w,fs,NFFT)                 # Corrected IF spectrum (wideband)

''' Plot results'''
plt.close('all')
plt.figure()
f_MHz=f/1.e6    # Frequency in MHz
plt.plot(f_MHz,20*np.log10(abs(SIF)/(T-taumax)),'b',label='Before correction')
plt.plot(f_MHz,20*np.log10(abs(SIF4n)/(T-taumax)),'r',label='Corrected (narrowband)')
plt.plot(f_MHz,20*np.log10(abs(SIF4w)/(T-taumax)),'g',label='Corrected (wideband)')
plt.plot(f_MHz,20*np.log10(abs(SIF_lin)/(T-taumax)),'k--',label='Ideal')
plt.title('Sinusoidal phase error (%.1f radians with a ripple frequency of %.1f kHz)' % (Asl, fsl/1.e3))

plt.xlim(np.array([fb-5.e4,fb+5.e4])/1.e6)
plt.ylim([-100,0])
plt.xlabel('Frequency (MHz)')
plt.ylabel('Amplitude spectrum')
handles, labels=plt.gca().get_legend_handles_labels()
plt.legend(handles,labels,loc='lower right')
plt.grid()

plt.show()
