import numpy as np

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