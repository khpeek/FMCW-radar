# FMCW-radar
Simulation and comparison of two alogrithms to compensate for frequency sweep nonlinearity in Frequency-Modulated Continuous-Wave (FMCW) radars.

# Introduction
FMCW radars are used for stealth in military applications. Due to their low transmit power (<1 W), they are difficult to detect by radar intercept receivers. By integrating the received signal over time, they achieve  "processing gain", enabling them to detect targets with the same signal-to-noise ratio as pulse radars with peak powers of >100 kW.

The "processing gain" is achieved by a technique called "stretch processing" [[Caputi 1971](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4103696)]. The received and transmitted signals - which mostly overlap in time - are mixed together produce an "intermediate frequency" (IF) or "beat" signal, the frequency of which is the difference between the frequencies of the transmitted and received signals. Provided that transmitted signal is a linear chirp (that is, a signal whose frequency increases linearly with time), the "beat" frequency for a single target is constant and proportional to the target's range (see below).

![FMCW radar principle](/Images/FMCW_schematic_SPIE.png)

There are, however, various engineering difficulties in producing a perfectly linear chirp. Deviations from chirp linearity cause the beat frequency to not be constant, resulting in loss of range resolution and possibly the presence of 'false targets' in the beat spectrum. The distortion is range-dependent, making it difficult to 'disentangle' even if the nature of the chirp nonlinearity is known, as the range is not known a priori.

# The effect of chirp nonlinearity
 To illustrate how the algorithm works, consider the example shown below of the effect of chirp nonlinearity for two targets at different ranges.

![FMCW schematic](/Images/FMCW_schematic_transmitted_received.png)

In the upper subplot, the green curve represents the time-frequency characteristic of the transmitted signal, which is linear except for a "kink" in the middle. The blue and red curves represent received signals for targets at different ranges, and are simply delayed versions of the transmitted signal. The lower subplot shows time-frequency characteristics of the beat signals for these two targets, and are obtained by taking the difference between the transmitted and respective received time-frequency characteristics. The deviation from a constant frequency apparent, and is somewhat more severe for the more distant target.

# The chirp nonlinearity correction algorithm
Given the phase error of the transmitted signal, it is possible to correct for the effects of chirp nonlinearity in FMCW radar by digital post-processing of the IF signal. The algorithm was invented by Meta et al. [[2006](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4241255)], although a very similar version of the algorithm was described earlier by Burgos-Garcia et al. [[2003](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1182388)]. The steps of the algorithm are depicted below.

![Error correction algorithm schematic](/Images/FMCW_phase_error_correction_algorithm.png)

Subplot 1 shows the time-frequency characteristic of the intermediate frequency (IF) signal 'as is', without any correction. Both targets deviate from having a constant beat frequency. The deviation consists of two parts: one emanating from the transmitted signal, and one from the received signal. The portion emanating from the transmitted signal is aligned in time, whereas the portion emanating from the received signal is delayed by the two-way transit time to the target, which is not known a priori.

In the first step of the correction algorithm, the distortion from the transmitted signal is removed. This requires the IF signal to be sampled in quadrature, so that it can be represented as a complex exponential, so that phase adjustments can be implemented by (complex) multiplication.

The resulting signal, sIF2, contains nonlinearities emanating from the received signal only. These nonlinearities are 'skewed' in the time-frequency plane, in that phase errors occurring at later times are also modulated onto proportionally higher beat frequencies. The received non-linearities can thus be 're-aligned' by applying a "deskew" filter which implements the reverse skew transformation in the time-frequency plane. (Specifically, the deskew filter has a group delay of -f/alpha, where f is frequency and alpha the nominal chirp rate of the transmitted signal).

In the signal sIF3 at the output of the deskew filter, the nonlinearities emanating from the received signal are time-aligned, but have a slightly different form from the original nonlinearities due to the application of the deskew filter. In the final step of the correction algorithms, these residual phase errors are removed by complex multiplication. In the algorithm of Burgos-Garcia et al., the multiplication is by the complex conjugate of the original phase error, whereas the algorithm of Meta et al. takes into account the skewing of the nonlinearity.


