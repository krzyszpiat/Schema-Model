import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import functions for the script
from HebbTask import HebbParadigm
from stimuliGeneration import categoryGeneration
from stimuliGeneration import itemGeneration


# Import variables for the script
from config import *
import config
cfg = {k: v for k, v in vars(config).items() if not k.startswith('__')} #print(pd.Series(cfg))



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

    categories = categoryGeneration(cfg)

    items = itemGeneration(cfg, categories)


############
# Hebb Task
############

    results = HebbParadigm(cfg, items, positions)

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