import numpy as np

from utils import cosim

# Config
features = 100
n_items = 5

# Parameters
alpha = 0.8

# Creating category A prototype
category_A = np.random.rand(features)

# Creating items from category A
items_A = []

for i in range(n_items):
    random_vector = np.random.rand(features)
    item = alpha * category_A + (1-alpha) * random_vector
    items_A.append(item)


# Checking similarites between the items and the category prototype
for i in range(n_items):
    item = items_A[i]
    sim = cosim(category_A, item)
    dist = np.linalg.norm(category_A - item)
    print(f"item A{i+1}: cosine={sim:.2f}, distance={dist:.2f}")

##################
# Serial positions
##################
positions = []

# Creating random vectors for serial positions
for p in range(n_items):
    random_vector = np.random.rand(features)
    positions.append(random_vector)

# Making the position vectors orthogonal
pos_matrix = np.column_stack(positions)

Q, R = np.linalg.qr(pos_matrix) # QR decomposition 

positions = []

for p in range(n_items):
    position = Q[:,p]
    positions.append(position)

# checking orthogonality of the first two positions
np.dot(positions[0], positions[1])


#################
# Learning Phase
#################

# initializing the weight matrix
m = np.zeros((features, features))

# Hebbian learning
for i in range(n_items):
    m = m + np.outer(positions[i], items_A[i])


##################
# Retrieval Phase
##################
outputs = []

for o in range(n_items):
    output = np.dot(positions[o],m)
    outputs.append(output)


###################
# Redintegration
###################

# Printing cosine similarities
for o in range(n_items):
    for i in range(n_items):
        print(f"Output {o + 1} & item {i + 1} cosine similarity = cos({cosim(outputs[o],items_A[i])})")    