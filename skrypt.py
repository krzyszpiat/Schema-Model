import numpy as np
import pandas as pd

from utils import cosim

# FLAGS
# Scope of category vectors (1 = (0:1), -1 = (-1:1))
cat_scope = -1

# CONFIG
features = 100

n_targets = 4 # number of targets per trial
n_cycles = 2 # number of learning cycles
n_fillers = 2 # number of filler trials per cycle


n_categories = n_targets * (1 + n_fillers) # number of categories used in experiment
n_items = n_cycles #number of items per category
n_trials = n_cycles * (1 + n_fillers)


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
for p in range(n_targets):
    random_vector = np.random.rand(features)
    positions.append(random_vector)

# Making the position vectors orthogonal
pos_matrix = np.column_stack(positions)

Q, R = np.linalg.qr(pos_matrix) # QR decomposition 

positions = []

for p in range(n_targets):
    position = Q[:,p]
    positions.append(position)

# checking orthogonality of the first two positions
np.dot(positions[0], positions[1])


#################################################
#
#             EXPERIMENT SIMULATION
#
################################################


# setting an order of trials within a block
cycle_str = ["F"] * n_fillers + ["H"]
exp_str = cycle_str * n_cycles

for t in range(n_trials):
    
    # starting a new cycle after each Hebb list
    cycle_index = (t // (n_fillers + 1)) + 1
    
    # setting the list type for the current trial
    trial_type = exp_str[t]

    # selecting categories for the current trial
    trial_pos = t % (n_fillers + 1)
    selection_start = trial_pos * n_targets
    selection = list(range(selection_start, selection_start + n_targets))

    # setting up the order of categories for the current trial
    if trial_type == "F":
        cat_seq = np.random.permutation(selection)
    elif trial_type == "H":
        cat_seq = selection


#################
# Learning Phase
################# 

    # initializing the weight matrix
    m = np.zeros((features, features))

    # Hebbian learning
    for i in range(n_targets):
        cur_cat = cat_seq[i]
        cur_item = items[cur_cat][cycle_index - 1]
         # the line above can be hardcoded to cur_item = items[cur_cat][0] and simulate standard Hebb
        m = m + np.outer(positions[i], cur_item)

##################
# Retrieval Phase
##################

    outputs = []

    for o in range(n_targets):
        output = np.dot(positions[o],m)
        outputs.append(output)


###################
# Redintegration
###################

    print()
    print(f"================ Trial {t + 1} ================")
    print()

    sim_matrix = []

    for o in range(n_targets):
        row = []
        for i in range(n_targets):
            cur_cat = cat_seq[i]
            row.append(cosim(outputs[o], items[cur_cat][cycle_index - 1]))
        sim_matrix.append(row)

    df = pd.DataFrame(
        sim_matrix,
        index=[f"Output {i+1}" for i in range(n_targets)],
        columns=[f"Item {i+1}" for i in range(n_targets)]
    )

    print(df.round(3))