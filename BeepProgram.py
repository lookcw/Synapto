#Beep Program

import winsound
import random

#Baseline is 500 Hz and Oddball is 1000 Hz.
#Duration (Dur) is the number of milliseconds that the sound is played.
Baseline = 500
Oddball = 1000
Duration = 10

#a is 200 numbers starting from 6 (starting from 6 because we don't
#want the first 5 beeps to be oddball. To avoid consecutive number
#generation, increment range by 2.
#z gives you 40 random numbers from the range of 200 numbers.
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
        winsound.Beep(Baseline,Duration)
        normalBeeps += 1
        oddballPlayed = 0
    else:
        if(oddballPlayed == 0 and maxOddballBeeps < 24):
            winsound.Beep(Oddball,Duration)
            maxOddballBeeps += 1
            oddballPlayed = 1
            print(counter)
        else:                       #Makes sure that consecutive beeps aren't played.
            winsound.Beep(Baseline,Duration) 
            print("odd ball skipped") 
    counter +=1
    if (normalBeeps + maxOddballBeeps >= 200):
        break
    
print(maxOddballBeeps)
print(normalBeeps)




    







    


