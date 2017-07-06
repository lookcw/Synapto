#Beep Program
from __future__ import division
import random
import math
import pygame as pg
try:
    from itertools import izip
except ImportError: # Pytho 3
    izip = zip
    xrange = range






def play_music(music_file, volume=0.8):
    '''
    stream music with mixer.music module in a blocking manner
    this will stream the sound from disk while playing
    '''
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(1)

#Baseline is 500 Hz and Oddball is 1000 Hz.
#Duration is the number of milliseconds that the sound is played.
Baseline = 500
Oddball = 1000
Duration = 1

#a is 200 numbers starting from 6 (starting from 6 because we don't
#want the first 5 beeps to be oddball). 
#z gives you 40 random numbers from the range of 200 numbers (these are the list of numbers where oddball beep occurs).
#numOddballBeeps is greater than the total number of oddball beeps we want to hear
#because we want a large range of numbers in case the oddball beep gets skipped.
numOddballBeeps = 40
a = range(6, 200)
z = random.sample(a, numOddballBeeps)
print(z)

numBeeps = 300
maxOddballBeeps = 0
normalBeeps = 0
counter = 0
oddballCounter = 0
oddballPlayed = 0
while counter in range(numBeeps):
    if counter not in list(z):
        play_music('500.wav',0.8)
        print "standard"

        normalBeeps += 1
        oddballPlayed = 0
    else:
        if(oddballPlayed == 0 and maxOddballBeeps < 24):
            play_music('1000.wav',0.8)
            print "oddball"
            maxOddballBeeps += 1
            oddballPlayed = 1
            print(counter)
        else:                       #Makes sure that consecutive beeps aren't played.
            play_music('1000.wav',0.8)
            print("odd ball skipped") 
    counter +=1
    if (normalBeeps + maxOddballBeeps >= 200):
        break
    
print(maxOddballBeeps)
print(normalBeeps)
