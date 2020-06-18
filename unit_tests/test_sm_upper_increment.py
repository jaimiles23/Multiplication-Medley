
##########
# Imports
##########

from math import sqrt
from statistics import stdev
import matplotlib.pyplot as plt
import numpy as np


##########
# Axis
##########

questions = [num for num in range(70)]
sm_upper = 5
y_sm_upper = []

for q in questions:
    y_sm_upper.append(sm_upper)
    if not q % int(sqrt(sm_upper) * 1.5):
        sm_upper += 1


##########
# Results
##########

print(questions)
print(y_sm_upper)

for i in range(len(questions)):
    print(questions[i], '\t', y_sm_upper[i])


# plt.plot(questions, y_sm_upper)
# plt.show()

# for i in range(len(questions)):
#     mu, sigma = y_sm_upper[i] / 1.1, (sqrt(y_sm_upper[i]) - 1) * 1.5
#     x = mu + sigma * np.random.randn(10000)

#     n, bins, patches = plt.hist(x, 50, density = 1, facecolor = 'g', alpha = 0.75)

#     plt.xlabel('Question')
#     plt.ylabel('frequency')
#     plt.title('Histogram of sampled tables')
#     plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#     plt.axis([40, 160, 0, 0.03])
#     plt.grid(True)
#     plt.show()
#     input()

