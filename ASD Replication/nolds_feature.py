import nolds
import numpy as np

rwalk = np.cumsum(np.random.random(1000))
dfa = nolds.dfa(rwalk)
sampen = nolds.sampen(rwalk)

print(dfa)
print(sampen)