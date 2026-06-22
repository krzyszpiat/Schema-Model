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
    sim = np.dot(category_A, item) / (np.linalg.norm(category_A) * np.linalg.norm(item))
    dist = np.linalg.norm(category_A - item)
    print(f"item A{i+1}: cosine={sim:.2f}, distance={dist:.2f}")

# Serial positions

pos1 = np.random.rand(features)
pos2 = np.random.rand(features)
pos3 = np.random.rand(features)


# Learning Phase
m = []
m = np.outer(pos1, items_A[0])
m = m + np.outer(pos2, items_A[1])
m = m + np.outer(pos3, items_A[2])


# Retrieval Phase
output1 = np.dot(pos1,m)
output2 = np.dot(pos2,m)
output3 = np.dot(pos3,m) 

# Redintegration

# Cosine similarity of output1 and item1
for i in range(3):
    print(f"pos1 & item{i} cosine similarity = cos({cosim(output1,items_A[i])})")

from utils import cosim
cosim(output1, items_A[0])