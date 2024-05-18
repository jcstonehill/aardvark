import numpy as np

my = 5*[10]
my2 = 5*[8]

print(my)
print(my2)

my = np.array(my)
my2 = np.array(my2)

diff = my-my2
print(diff**2)

