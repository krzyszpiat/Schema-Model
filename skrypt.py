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
output1 = np.dot(positions[0],m)
output2 = np.dot(positions[1],m)
output3 = np.dot(positions[2],m) 

###################
# Redintegration

# Cosine similarity of output1 and items
for i in range(3):
    print(f"Output 1 & item {i} cosine similarity = cos({cosim(output1,items_A[i])})")

# Cosine similarity of output2 and items
for i in range(3):
    print(f"Output 2 & item {i} cosine similarity = cos({cosim(output2,items_A[i])})")

# Cosine similarity of output3 and items
for i in range(3):
    print(f"Output 3 & item {i} cosine similarity = cos({cosim(output3,items_A[i])})")