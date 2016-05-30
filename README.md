# FMCW-radar
Simulation and comparison of two alogrithms to compensate for frequency sweep nonlinearity in Frequency-Modulated Continuous-Wave (FMCW) radars.

# Introduction
FMCW radars are used in military applications where it is important to "see without being seen". Due to their low transmit power (<1 W), they are difficult to detect by radar intercept receivers. By integrating the received signal over time, they achieve the  "processing gain" necessary to detect targets with the same signal-to-noise ratio as pulse radars with peak powers of >100 kW.

The "processing gain" is achieved by a technique called "stretch processing" [[Caputi 1971](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4103696)]. The received and transmitted signals - which mostly overlap in time - are mixed together produce an "intermediate frequency" (IF) or "beat" signal, the frequency of which is the difference between the frequencies of the transmitted and received signals. Provided that transmitted signal is a linear chirp (that is, a signal whose frequency increases linearly with time), the "beat" frequency for a single target is constant and proportional to the target's range (see below).

![FMCW radar principle](/Images/FMCW_schematic_SPIE.png)

There are, however, various engineering difficulties in producing a perfectly linear chirp. Deviations from chirp linearity cause the beat frequency to not be constant, resulting in loss of range resolution and possibly the presence of 'false targets' in the beat spectrum. The distortion is range-dependent, making it difficult to 'disentangle' even if the nature of the chirp nonlinearity is known, as the range is not known a priori.

# The effect of chirp nonlinearity
Given the phase error of the transmitted signal - that is, how much the phase deviates from a linear chirp - it is possible to correct for the effects of chirp nonlinearity in FMCW radar by digital post-processing of the IF signal. This algorithm was invented by Meta et al. [[2006](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4241255)], although a very similar version of the algorithm was described earlier by Burgos-Garcia et al. [[2003](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1182388)]. To illustrate how the algorithm works, below we first show the effect of chirp nonlinearity for two targets at different ranges.

![FMCW schematic](/Images/FMCW_schematic_transmitted_received.png)

In the figure, the green line represents the time-frequency characteristic of the transmitted signal, which is linear except for a "kink" in the middle, which corresponds to a phase error. The green and red curves represent received signals for targets at different ranges, and are simply delayed versions of the transmitted signal. The lower subplot shows time-frequency characteristics of the beat signals for these two targets, and are obtained by taking the difference between the transmitted and respective received time-frequency characteristics. The deviation from a constant frequency apparent, and is somewhat more severe for the more distant target.

# The chirp nonlinearity correction algorithm
The 



