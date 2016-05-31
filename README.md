# FMCW-radar
Simulation and comparison of two algorithms for compensating the effects of frequency sweep nonlinearity in Frequency-Modulated Continuous-Wave (FMCW) radars.

## Introduction ##
FMCW radars are used for stealth in military applications. Due to their low transmit power (<1 W), they are difficult to detect by radar intercept receivers. By integrating the received signal over time, they achieve  "processing gain" enabling them to detect targets with the same signal-to-noise ratio as pulse radars with peak powers of >100 kW.

The "processing gain" is achieved by a technique called "stretch processing" [[Caputi 1971](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4103696)]. The received and transmitted signals - which mostly overlap in time - are mixed together produce an "intermediate frequency" (IF) or "beat" signal, the frequency of which is the difference between the frequencies of the transmitted and received signals. Provided that transmitted signal is a linear chirp (that is, a signal whose frequency increases linearly with time), the "beat" frequency for a single target is constant and proportional to the target's range (see below).

![FMCW radar principle](/Images/FMCW_schematic_SPIE.png)

There are, however, various engineering difficulties in producing a perfectly linear chirp. Deviations from chirp linearity cause the beat frequency to not be constant, resulting in loss of range resolution and possibly the presence of 'false targets' in the beat spectrum. The distortion is range-dependent, making it difficult to 'disentangle' even if the nature of the chirp nonlinearity is known, as the range is not known a priori.

## The effect of chirp nonlinearity ##
 To illustrate how the algorithm works, consider the example shown below of the effect of chirp nonlinearity for two targets at different ranges.

![FMCW schematic](/Images/FMCW_schematic_transmitted_received.png)

In the upper subplot, the green curve represents the time-frequency characteristic of the transmitted signal, which is linear except for a "kink" in the middle. The blue and red dashed curves represent received signals for targets at different ranges, and are simply delayed versions of the transmitted signal. The lower subplot shows time-frequency characteristics of the beat signals for these two targets, and are obtained by taking the difference between the transmitted and respective received time-frequency characteristics. Both deviate from a constant frequency; the deviation is more severe for the more distant target, where the phase errors are more de-correlated.

## The chirp nonlinearity correction algorithm ##
Given the phase error of the transmitted signal, it is possible to correct for the effects of chirp nonlinearity in FMCW radar by digital post-processing of the IF signal. The algorithm was invented by Meta et al. [[2006](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4241255)], although a very similar version of the algorithm was described earlier by Burgos-Garcia et al. [[2003](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1182388)]. The steps of the algorithm are depicted below.

![Error correction algorithm schematic](/Images/FMCW_phase_error_correction_algorithm.png)

The topmost subplot shows the time-frequency characteristic of the intermediate frequency (IF) signal 'as is', without correction. Both targets deviate from having a constant beat frequency. The deviation consists of two parts: one resulting from the nonlinearity of the transmitted signal, and one from the received signal. The former is aligned in time, whereas the latter is delayed by the two-way transit time to the target, which is not known *a priori*.

In the first step of the correction algorithm, the distortion from the transmitted signal is removed. This requires the IF signal to be sampled in quadrature, so that it can be represented as a complex exponential, so that phase adjustments can be implemented by (complex) multiplication.

The resulting signal, sIF2, contains nonlinearities from the received signal only. These nonlinearities are 'skewed' in the time-frequency plane, in that phase errors occurring at later times are modulated onto proportionally higher beat frequencies. The received nonlinearities can be 're-aligned' in time by applying a "deskew" filter which implements the reverse skew transformation in the time-frequency plane. (Specifically, the deskew filter has a group delay of -f/alpha, where f is the frequency and alpha the nominal chirp rate of the transmitted signal).

In the signal sIF3 at the output of the deskew filter, the nonlinearities emanating from the received signal are time-aligned, but have a slightly different form from the original nonlinearities due to the application of the deskew filter. In the final step of the correction algorithms, these residual phase errors are removed by complex multiplication. In the algorithm of Burgos-Garcia et al., the multiplication is by the complex conjugate of the original phase error, whereas the algorithm of Meta et al. takes into account the skewing of the nonlinearity.

## Results ##
The script FMCW_phase_error_correction.py simulates both correction algorithms for an X-band FMCW radar with a carrier frequency of 10 GHz, chirp bandwidth of 50 MHz, and chirp period of 500 us. The target is at a range of 12 km, corresponding to a two-way transit time of 80 us and a beat frequency of 8 GHz. To avoid the fly-back from the previous sweep, only the last 400 us of each sweep is processed; this corresponds to an instrumented range of 15 km.

#### Sinusoidal phase errors ####
The phase error is sinusoidal and has the form Asl*cos(2*pi*fsl*t), where Asl is the maximum phase error (in radians) and fsl the sidelobe ripple frequency. For illustration, the maximum phase error is chosen at a large value of Asl = 0.5 radians. Below is shown the resulting beat spectrum for a sidelobe ripple frequency of fsl = 15.8 kHz.

![Results low ripple frequency](/Images/FMCW_sinusoidal_phase_error_low_ripple_frequency.png)

As seen from the plot, the sinusoidal phase errors results in "paired echoes" offset from the ideal beat signal by mutiples of the sidelobe ripple frequency fsl. For this value of fsl, both algorithms work quite well, and the spectrum of the corrected signal is almost indistinguishable from the ideal beat spectrum. (A Hamming window was applied to reduce sidelobes. The spectrum is plotted on a decibel scale referenced to the maximum attainable signal strength without Hamming window.)

As the ripple frequency is increased, the difference between the "narrowband" algorithm of Burgos-Garcia et al. and "wideband" algorithm of Meta et al. becomes apparent. The spectrum below illustrates this for a sidelobe ripple frequency of fsl = 31.6 kHz.

![Results high ripple frequency](/Images/FMCW_sinusoidal_phase_error_high_ripple_frequency.png)

At this increased ripple frequency, the "wideband" algorithm still performs well, whereas the "narrowband" still leaves behind paired echoes, which could falsely be interpreted as targets.

#### Cubic phase errors ####
The correction algorithm also works for different kinds of phase error, such as a cubic one of the form k3/3*t^3. (Note that the time axis is chosen at the middle of the transmitted chirp). The spectrum below illustrates this for a cubic phase error with a maximum frequency error of 7.9 kHz.

![Results cubic phase error](/Images/FMCW_cubic_phase_error.png)

As seen from the figure, the cubic phase error results in a 'blurred' (actually, linearly chirped) beat signal with less range resolution peak signal power. Both algorithms restore resolution and signal power to the ideal response.

#### Quartic phase errors ####
Finally, the performance of the algorithm for a quartic phase error k4/4*t^4 is shown below. The maximum frequency deviation is the same as for the cubic phase error.

![Results quartic phase error](/Images/FMCW_quartic_phase_error.png)

Besides asymmetric 'blurring' of the point target response, the quartic phase error also results in a range error: the peak of the beat frequency spectrum is at a different location from the ideal response. Again, both algorithms perform well in restoring the response to the ideal.

## Discussion ##
One of the main advantages of FMCW radars is their "homodyne" architecture - the fact that the transmitted signal is also used as the local oscillator (LO) for down-converting the received signal. In particular, the analog-to-digital converter at the receiver no longer needs to sample the full bandwidth of the received signal, but can suffice with a smaller bandwidth covering the range of beat frequencies expected. This property is an advantage over the matched filter, which - if implemented digitally - would require sampling over the full bandwidth of the received signal.

Conventionally, however, a drawback of FMCW radars has been the requirement of linear chirps. This has led to great engineering effort, for example, linearizing voltage-controlled oscillators (VCOs) and using direct digital synthesizers (DDSs) despite their relatively limited bandwidth and quantization noise. The phase error correction algorithms essentially eliminate this drawback by offering a 'software' method of chirp linearization, albeit at a slightly increase of the computation cost.

In short, the algorithms implemented here promise to greatly increase the applicability of FMCW radars, by giving the possibility to add modulation beyond the linear chirp. This can increase stealth by making it more difficult for radar intercept receivers to estimate the modulation used, or could be used to add communications to radar signals. (This is of interest for FMCW radars in Advanced Driver Assistance Systems (ADAS), since it would allow formations of cars to communicate with each other).
