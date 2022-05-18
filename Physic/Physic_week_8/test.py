import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def func(x, a, b, c):
    return a * np.exp(-b * x) + c


a = np.array([])
b = np.array([])
a = np.append(a, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
b = np.append(b, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
plt.xlabel('X')
plt.ylabel('Y')

res = stats.linregress(a, b)

'''fit = np.polyfit(a, b, 1)
p = np.poly1d(fit)
plt.plot(a, p(a))'''

plt.plot(a, b, 'o', label='original data')
plt.plot(a, res.intercept + res.slope*a, 'r', label='fitted line')
plt.text(5.6, 3.5, 'R-squared = %0.2f' % res.rvalue**2)
plt.legend()

plt.show()
