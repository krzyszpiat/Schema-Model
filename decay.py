import numpy as np
from utils import cosim

n_steps = 1000
decay_rate = .1
some_factor = .9

f = 100

vec1 =  np.random.rand(f)
vec2 =  np.random.rand(f)

mat = np.outer(vec1, vec2)

output = np.dot(vec1,mat)

cosim(vec2,output)

###############################
# COSINE SIMILARITY
# accumulating noise

# for step in range(n_steps):
#     mat = mat + decay_rate * np.random.randn(f, f)
#     output = np.dot(vec1, mat)
#     print(step, cosim(vec2, output))

###############################

###############################
# DOT PRODUCT
# anti-Hebbian learning

# for step in range(n_steps):
#     mat = mat * (1 - decay_rate)
#     output = np.dot(vec1, mat)
#     print(step, np.dot(vec2, output))
###############################


###############################
# COSINE SIMILARITY
# non-linear decay

# some_factor = .8

for step in range(n_steps):
    effective_rate = decay_rate * (some_factor ** step)
    mat = mat - effective_rate * np.outer(vec1, vec2)
    output = np.dot(vec1, mat)
    print(step, np.dot(vec2, output))

###############################