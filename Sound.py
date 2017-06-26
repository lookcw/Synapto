import winsound
import random

Baseline = 500
Oddball = 1000
Dur = 1000

y = range(0,100,5)

for counter in range(120):
    x = random.randint(0,100)
    print(x)
    if x not in list(y) or counter<5:
        winsound.Beep(Baseline,Dur)
    else:
        winsound.Beep(Oddball,Dur)




    


