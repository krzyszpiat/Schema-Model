import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import cosim
from HebbTask import HebbParadigm

# FLAGS
# Scope of category vectors (1 = (0:1), -1 = (-1:1))
cat_scope = -1

# CONFIG
features = 100

n_targets = 8 # number of targets per trial
n_cycles = 10 # number of learning cycles
n_fillers = 2 # number of filler trials per cycle


n_categories = n_targets * (1 + n_fillers) # number of categories used in experiment
n_items = n_cycles #number of items per category
n_trials = n_cycles * (1 + n_fillers)


# PARAMETERS
alpha = 0.5


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


########################
# EXPERIMENT SIMULATION
########################

results = HebbParadigm(items, positions, n_targets, n_cycles, n_fillers, n_trials, features)


###################
# Results
###################

results_df = pd.DataFrame(results)



hebb_acc = results_df[results_df['type'] == 'Hebb List'].groupby('cycle')['accuracy'].mean()
filler_acc = results_df[results_df['type'] == 'Filler List'].groupby('cycle')['accuracy'].mean()


plt.plot(hebb_acc.index, hebb_acc.values, label='Hebb List', marker='o')
plt.plot(filler_acc.index, filler_acc.values, label='Filler List', marker='o')

plt.xlabel('Cycle')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.xticks(range(1, n_cycles + 1))
plt.legend()
plt.title('Hebb Repetition Effect')


#print(results_df)
plt.show()