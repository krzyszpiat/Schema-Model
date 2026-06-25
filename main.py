import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from HebbTask import HebbParadigm
from stimuliGeneration import categoryGeneration
from stimuliGeneration import itemGeneration

# FLAGS
# Collect diagnostics? (1 = yes)
diag = 1 

# print position curves? (1 = yes)
crvs = 1

# Wchich similarity measure?
measure = "cosim"
#measure = "dot"

# CONFIG
cat_scope = -1 # Scope of category vectors (1 = (0:1), -1 = (-1:1))
item_scope = 1 # Scope of item vectors (1 = (0:1), -1 = (-1:1))

n_simulations = 100
features = 100

n_targets = 8 # number of targets per trial
n_cycles = 10 # number of learning cycles
n_fillers = 2 # number of filler trials per cycle


n_categories = n_targets * (1 + n_fillers) # number of categories used in experiment
n_items = n_cycles #number of items per category
n_trials = n_cycles * (1 + n_fillers)


# PARAMETERS
alpha = 0.3
threshold = .8 # will need to be adjusted for the dot products
decay_rate = .7 # set to 0 to disable decay
decay_slope = .8


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

    items = itemGeneration(n_categories, features, alpha, n_items, categories, item_scope)


############
# Hebb Task
############

    results = HebbParadigm(items, positions, n_targets, n_cycles, n_fillers, n_trials, features, threshold, decay_rate, decay_slope, measure)

    for r in results:
        r['simulation'] = sim + 1

    all_results.extend(results)



###################
# Results
###################

# Hebb Repetition Effect

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


# Serial position curves

if crvs == 1:
    targets_df = results_df['targets'].apply(pd.Series)
    responses_df = results_df['responses'].apply(pd.Series)

    position_accuracy = (targets_df == responses_df)

    curves_df = pd.concat([results_df, position_accuracy], axis=1)


    Hebbs = curves_df[curves_df['type'] == 'Hebb List'][range(n_targets)].mean()
    Fillers = curves_df[curves_df['type'] == 'Filler List'][range(n_targets)].mean()

    plt.plot(range(1, n_targets+1), Hebbs[range(n_targets)].values, marker='o')
    plt.xlabel('Serial Position')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.05)
    plt.title(f'Hebb Lists, serial position curve, {n_simulations} simulations')
    plt.show()



    plt.plot(range(1, n_targets+1), Fillers[range(n_targets)].values, marker='o', color = 'orange')
    plt.xlabel('Serial Position')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.05)
    plt.title(f'Filler Lists, serial position curve, {n_simulations} simulations')
    plt.show()