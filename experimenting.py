import numpy as np
import matplotlib.pyplot as plt
import seaborn
from matplotlib.pyplot import figure


mean = [0, 0]
cov = [[1, 2], [2, 5]]

X = np.random.multivariate_normal(mean, cov, 100)
X.shape

seaborn.set()
plt.figure(figsize=(10, 8), dpi=300)
plt.scatter(X[:, 0], X[:, 1])
plt.show()
