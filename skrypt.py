import numpy as np

from utils import cosim

# FLAGS
# Scope of category vectors (1 = (0:1), -1 = (-1:1))
cat_scope = -1

# CONFIG
features = 100
n_categories = 4
n_lists = 2
n_items = n_categories #* n_lists


# PARAMETERS
alpha = 0.8


#######################
# Categories & Items
#######################

categories = []

# Creating random vectors for categories
for p in range(n_categories):

    if cat_scope == 1:
        random_vector = np.random.rand(features)
    elif cat_scope == -1:
        random_vector = np.random.randn(features)

    categories.append(random_vector)


# Checking similarities between categories
catrel_matrix = np.vstack(categories)
cat_norms_list = []

for c in categories:
    norm = np.linalg.norm(c)
    unit_vector = c / norm
    cat_norms_list.append(unit_vector)
cat_norms = np.array(cat_norms_list)

catrel_check = cat_norms @ cat_norms.T

# Printing correlation matrix of category prototypes
print(np.round(catrel_check, 2))


# Creating items for each category
items = []

for c in range(n_categories):
    cat = categories[c]
    cat_items = []

    for i in range(n_items):
        random_vector = np.random.rand(features)
        item = alpha * cat + (1-alpha) * random_vector
        cat_items.append(item)

    items.append(cat_items)


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
    cur_item = items[i][i] # selecting all the items from different categories
    m = m + np.outer(positions[i], cur_item)


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
        print(f"Output {o + 1} & item {i + 1} cosine similarity = cos({cosim(outputs[o],items[i][i])})")