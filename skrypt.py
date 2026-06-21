import numpy as np

# Flags
features = 100

# Parameters
alpha = 0.8

# Category A prototype
category_A = np.random.rand(features)

# Items from category A
items_A = []

for i in range(5):
    random_vector = np.random.rand(features)
    item = alpha * category_A + (1-alpha) * random_vector
    items_A.append(item)


# Checking similarites between the items and the category prototype

for i in range(5):
    item = items_A[i]
    sim = np.dot(category_A, item) / (np.linalg.norm(category_A) * np.linalg.norm(item))
    dist = np.linalg.norm(category_A - item)
    print(f"item A{i+1}: cosine={sim:.2f}, distance={dist:.2f}")