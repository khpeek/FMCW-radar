# FMCW-radar
Simulation and comparison of two alogrithms to compensate for frequency sweep nonlinearity in Frequency-Modulated Continuous-Wave (FMCW) radars.

# Introduction
FMCW radars are used in military applications where it is important to "see without being seen". Due to their low transmit power (<1 W), they are difficult to detect by radar intercept receivers compared to pulse radars (which typically transmit peak powers of >100 kW), and appear to be 'buried' ambient noise. They way they can still detect targets is by integrating the received signal over time to achieve "processing gain".

A well-known way to achieve processing gain is to use a matched filter. FMCW radars work slightly differently, however, and employ a technique called "stretch processing" [Caputi 1971](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4103696).
