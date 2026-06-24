import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HebbTask import HebbParadigm
from stimuliGeneration import categoryGeneration
from stimuliGeneration import itemGeneration

# FLAGS
# Scope of category vectors (1 = (0:1), -1 = (-1:1))
cat_scope = -1

# CONFIG
n_simulations = 100
features = 100

n_targets = 8 # number of targets per trial
n_cycles = 10 # number of learning cycles
n_fillers = 2 # number of filler trials per cycle


n_categories = n_targets * (1 + n_fillers) # number of categories used in experiment
n_items = n_cycles #number of items per category
n_trials = n_cycles * (1 + n_fillers)


# PARAMETERS
alpha = 0.5


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


all_results = []

for sim in range(n_simulations):

#######################
# Categories & Items
#######################

    categories = categoryGeneration(n_categories, features, cat_scope)

    items = itemGeneration(n_categories, features, alpha, n_items, categories)


############
# Hebb Task
############

    results = HebbParadigm(items, positions, n_targets, n_cycles, n_fillers, n_trials, features)

    for r in results:
        r['simulation'] = sim + 1

    all_results.extend(results)


###################
# Results
###################

results_df = pd.DataFrame(all_results)


hebb_acc = results_df[results_df['type'] == 'Hebb List'].groupby('cycle')['accuracy'].mean()
filler_acc = results_df[results_df['type'] == 'Filler List'].groupby('cycle')['accuracy'].mean()


plt.plot(hebb_acc.index, hebb_acc.values, label='Hebb List', marker='o')
plt.plot(filler_acc.index, filler_acc.values, label='Filler List', marker='o')

plt.xlabel('Cycle')
plt.ylabel('Accuracy')
plt.ylim(0, 1.05)
plt.xticks(range(1, n_cycles + 1))
plt.legend()
plt.title(f'Hebb Lists vs Filler lists, {n_simulations} simulations')


print(results_df)
plt.show()