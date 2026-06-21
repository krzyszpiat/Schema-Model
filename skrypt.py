import numpy as np

vector1 = np.random.rand(10)
vector2 = np.random.rand(10)

dot = np.dot(vector1, vector2)
outer = np.outer(vector1, vector2)

np.set_printoptions(precision=2)

print(outer)

retrieved = outer @ vector2

np.set_printoptions(precision=2)
print(retrieved)
print(vector1)

retrieved = (outer @ vector2) / np.dot(vector2, vector2)


print(retrieved)

print(np.allclose(retrieved, vector1))