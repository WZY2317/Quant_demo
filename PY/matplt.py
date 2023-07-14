import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]
plt.plot(x, y)
plt.axis([0, 6, 0, 20])
plt.show()
t = np.arange(0, 5, 0.2)
x1 = t
y1 = t
y2 = t**2
x2 = x1
x3 = t
y3 = t**3
linelist = plt.plot(x1, y1, x2, y2, x3, y3)
plt.setp(linelist, color='blue')
plt.show()
fig = plt.figure(1)
ax1 = plt.subplot(2, 1, 1)
plt.plot([1, 2, 3, 4])
ax2 = plt.subplot(2, 1, 2)
plt.plot([4, 5, 6])
plt.show()