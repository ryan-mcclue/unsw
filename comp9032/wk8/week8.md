<!-- SPDX-License-Identifier: zlib-acknowledgement -->

DAC (digital to analog converter; convert to continous value, i.e. quantised) 
should go through some signal conditioning after to perform voltage amplification,
smoothing, buffering (protection from dangerous voltages), bandwidth limiting etc. 
(this applies to any analog signal, input or output)

parallel interface (so multiple bits over multiple channels at the same time)

* High-res DAC means high number of bits
  However, may be given in volts, meaning the smallest step in voltage possible
* Linearity is how close to actual value, i.e. accuracy
* Settling time is how long for output voltage to settle

A DAC will have a number of switches in its circuitry
Glitch occurs if switching from 1 to 0 faster than 0 to 1 

Binary-weighted vs ladder DAC?

ADC typically have a transducer (energy from one form to another, e.g. microphone, light-dependent resistor) 
to convert from physical analog to electrical analog
ADC will recieve a sampled signal from a sample-and-hold circuit.

Shannon's sampling theorem states to preserve information of signal, must sample
at least twice maximum frequency. ∴, this minimum sampling frequency known as Nyquist rate
If below Nyquist, will be undersampled, producing aliasing 
(components that were not present in the original signal)
As such, will have to modify clock signal and reference voltage to use

Successive approximation vs parallel (faster; expensive) vs two stage (commonly used) ADC?

* Conversion time (determines upper frequency limit); aperture time is time looking at signal
* Resolution
* Accuracy
IMPORTANT: n-bit ADC may have less than n-bits accuracy
