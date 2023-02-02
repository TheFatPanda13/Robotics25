import numpy as np

xs = [0.9, 1.9, 1.0, -0.3, 0.6, 1.0, -2.2, 0.0, 1.9, -1.0]
ys = [1.7, 0.8, 0.7, 0.3, -1.2, -0.8, -0.4, -1.2, -1.5, 1.8]

cov_matrix = np.cov(xs,ys)
print(cov_matrix)
