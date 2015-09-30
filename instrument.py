#This script will measure 2 voltages (on A0 and A1 inputs on the ADC), and turn the A0 into a pitch, and A1 into a volume.
#Voltage readings are also outputted in terminal.

import time
import signal 
import sys
import pygame.midi
from Adafruit_ADS1x15 import ADS1x15


def conf_midi():
    instrument = 86
    pygame.init()
    pygame.midi.init()
    port = 0
    global midiOutput
    midiOutput = pygame.midi.Output(port, 0)
    midiOutput.set_instrument(instrument)

def play_midi(note, b4note, volume):
    if (note != b4note):
        midiOutput.note_off(b4note)
        midiOutput.note_on(note,volume)
    time.sleep(.15)

def get_note(voltage=0):
    """ Compute the note based on the distance measurements, get percentages of each scale and compare """
    minVolt = 0    
    maxVolt = 0.7
    octaves = 1
    minNote = 48   # c4 middle c
    maxNote = minNote + 12*octaves
    # Percentage formula
    fup = (voltage - minVolt)*(maxNote - minNote)
    fdown = (maxVolt - minVolt)
    note = minNote + fup/fdown
    return int(note)

def get_volume(current=0):
    """Compute a volume based on current, linear proportion"""
    mVmax = 0.55 		#maximum mV from shunt (in volts)
    mVmin = 0.012
    if (current < mVmin):
	volume = 0
    else:
	minVol = 0
	maxVol = 127
	volume = (current / mVmax)*(maxVol - minVol)
	#volume = ((current - mVmin)/( mVmax - mVmin))*(maxVol - minVol)
	return int(volume)

ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC
gain = 4096  # +/- 4.096V
sps = 3300
adc = ADS1x15(ic=ADS1015)

note = 0
conf_midi()
volume = 127

try:
    while True:
        b4note = note
        # get voltage
	volts1 = adc.readADCSingleEnded(0, gain, sps) / 1000
	note = get_note(v1)
        volts2 = adc.readADCSingleEnded(1, gain, sps) / 1000
	volume = get_volume(v2)
        column1 = [volts1]
        column2 = [volts2]
        for c1, c2 in zip(column1, column2):
    	    print "%-9s %s" % (c1, c2)
        # calculate note
        # play the note
        play_midi(note, b4note, volume)
except KeyboardInterrupt:
    del midiOutput
    pygame.midi.quit()
pygame.midi.quit()
