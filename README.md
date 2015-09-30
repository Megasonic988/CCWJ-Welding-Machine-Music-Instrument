# CCWJ-Welding-Machine-Music-Instrument

A Python script showing the software used to run the welding machine music instrument.

Voltage and current readings are obtained from the welding machine, and are read by Raspberry Pi with an analog to digital converter (ADC). Voltage is converted to pitch, and current to volume, by the Python script. The output is a midi signal that can be played back with a software synth on the Raspberry Pi; FluidSynth was used in this project.

For more information, refer to the project documentation in the Word file.
