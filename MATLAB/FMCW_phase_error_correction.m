clear; close all; clc;

fc=10e9;    % center frequency (10 GHz)
B=50e6;     % chirp bandwidth (50 MHz)
T=500e-6;   % chirp period (500 us)
alpha=B/T;  % chirp rate (100 GHz/s)

R=15e3;         % target range 15 km
c=3e8;          % speed of light
tau=2*R/c;      % target transit time 100 us
fb=alpha*tau;   % beat frequency 10 MHz
fs=25e6;        % sampling frequency 25 MHz
Ts=1/fs;        % sampling period (40 ns)
N=T/Ts;         % number of samples per sweep (12,500)
Np=(T-tau)/Ts;  % number of processed samples per sweep (10,000)
A=alpha/fs^2;   % dimensionless chirp parameter

% Phase error function
Asl=0.5;                        % phase error amplitude (radian)
fsl=.2*sqrt(alpha);             % phase error frequency
e=@(t) Asl*cos(2*pi*fsl*t);     % phase error
se=@(t) exp(1j*e(t));           % error function

heaviside=@(t) 0.5*(sign(t)+1);
rectpuls=@(t) heaviside(t+.5)-heaviside(t-.5);

% Generation of the beat signal
phiTX=@(t) 2*pi*(fc*t+1/2*alpha*t.^2)+e(t);     % transmit signal phase
phib=@(t) phiTX(t)-phiTX(t-tau);                % beat signal phase
r=@(t) rectpuls((t-tau/2)/(T-tau));             % observation window
sb=@(t) r(t).*exp(1j*phib(t));                  % complex beat signal

% Time and frequency grids
n=0:N-1;                    % time index
t=(-N/2+n)*Ts;              % time grid
NFFT=2^nextpow2(N+1/A);     % as required for deskew filter processing
k=0:NFFT-1;                 % frequency index
f=(-NFFT/2+k)/NFFT*fs;      % frequency grid

% Phase error compensation algorithm
sIF=sb(t);                  % sampled beat signal
sIF2=sIF.*conj(se(t));      % remove transmitted phase errors sIF2
sIF3=deskew(sIF2,A);        % deskew filter to obtain sIF3
sIF4n=sIF3.*se(t);          % sIF4 (narrowband IF)
sea=deskew(se(t),A);        % residual phase error function
sIF4w=sIF3.*sea;            % sIF4 (wideband IF)

% Calculate spectra
sIFd=@(t) r(t).*exp(1j*2*pi*(fc*tau-1/2*alpha*tau^2+alpha*tau*t));      % ideal beat signal
wIF=[zeros(1,N-Np) hamming(Np,'periodic')'];                            % window for sIF
SIFd=T/N*exp(1j*pi*N*(-1/2+k/NFFT)).*fft(wIF.*sIFd(t).*(-1).^n,NFFT);   % SIF (ideal)
SIF=T/N*exp(1j*pi*N*(-1/2+k/NFFT)).*fft(wIF.*sIF.*(-1).^n,NFFT);        % SIF (observed)

wIF4=[hamming(Np,'periodic')' zeros(1,N-Np)];                           % window for sIF4
SIF4n=T/N*(-1).^(N*(-1/2+k/NFFT)).*fft(wIF4.*sIF4n.*(-1).^n,NFFT);      % SIF4 (narrowband IF)
SIF4w=T/N*(-1).^(N*(-1/2+k/NFFT)).*fft(wIF4.*sIF4w.*(-1).^n,NFFT);      % SIF4 (wideband IF)

% Convert to normalized decibel scale
SIFd_dB=20*log10(abs(SIFd)/(T-tau));
SIF_dB=20*log10(abs(SIF)/(T-tau));
SIF4n_dB=20*log10(abs(SIF4n)/(T-tau));
SIF4w_dB=20*log10(abs(SIF4w)/(T-tau));

% Plot results
figure(1); hold on; grid on
fMHz=f/1e6;                 % frequency in MHz
plot(fMHz,SIFd_dB,'g')      % ideal signal
plot(fMHz,SIF_dB)           % original IF signal
plot(fMHz,SIF4n_dB,'k')     % compensated signal (narrowband approximation)
plot(fMHz,SIF4w_dB,'m:')    % compensated signal (wideband)

scale=1.5*fsl*T;                        % frequency offset for axis limits
xlim([fb-scale/T fb+scale/T]/1e6)       % frequency axis limits
xlabel('frequency (MHz)'); ylabel('amplitude spectrum (dB)')
legend('s_I_F (ideal)','s_I_F','s_I_F_4 (narrowband IF method)','s_I_F_4 (wideband IF method)')
ylim([-80 0])
