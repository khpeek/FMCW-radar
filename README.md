# FMCW-radar
Simulation and comparison of two alogrithms to compensate for frequency sweep nonlinearity in Frequency-Modulated Continuous-Wave (FMCW) radars.

# Introduction
FMCW radars are used in military applications where it is important to "see without being seen". Due to their low transmit power (<1 W), they are difficult to detect by radar intercept receivers. By integrating the received signal over time, they achieve the  "processing gain" necessary to detect targets with the same signal-to-noise ratio as pulse radars with peak powers of >100 kW.

The way that "processing gain" is achieved is different from a matched filter, and is called "stretch processing" [Caputi 1971](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4103696). Unlike in a pulse radar, the received and transmitted signals overlap in time, and are mixed together produce an "intermediate frequency" (IF) or "beat" signal. The frequency of the "beat" signal is proportional to the range of the target, provided that the frequency of the transmit increases linearly with time. (Such a signal is called a "linear chirp").

The problem is that it is technically difficult to transmit a perfectly linear chirp. Deviations from chirp linearity cause the beat frequency to not be constant, resulting in loss of range resolution and possibly the presence of 'false targets' in the beat spectrum. Even if we know the form of the nonlinearity, the distortions in the beat signal are dependent on the range of target, which is not known a priori.

