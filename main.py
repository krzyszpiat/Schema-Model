import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# Import functions for the script
from HebbTask import HebbParadigm
from stimuliGeneration import categoryGeneration
from stimuliGeneration import itemGeneration


# Import variables for the script
from config import *
import config
cfg = {k: v for k, v in vars(config).items() if not k.startswith('_')}


if save_unique:
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    output_dir = f'outputs\\{timestamp}'
else:
    output_dir = 'outputs\\latest'

os.makedirs(output_dir, exist_ok=True)



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

for sim in tqdm(range(n_simulations), desc="Simulations"):

#######################
# Categories & Items
#######################

    categories = categoryGeneration(cfg)

    items = itemGeneration(cfg, categories)


############
# Hebb Task
############

    results = HebbParadigm(cfg, items, positions, output_dir)

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
plt.title(f'Hebb Lists vs Filler Lists, {n_simulations} simulations')
plt.savefig(f'{output_dir}/hebb_effect.png')
plt.close()


# Serial position curves
targets_df = results_df['targets'].apply(pd.Series)
responses_df = results_df['responses'].apply(pd.Series)

position_accuracy = (targets_df == responses_df)
curves_df = pd.concat([results_df, position_accuracy], axis=1)

Hebbs = curves_df[curves_df['type'] == 'Hebb List'].groupby('cycle')[list(range(n_targets))].mean()
Fillers = curves_df[curves_df['type'] == 'Filler List'].groupby('cycle')[list(range(n_targets))].mean()


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Curves plots: Hebb

colors = plt.cm.Blues(np.linspace(0.3, 1.0, n_cycles))

for c, (cycle, row) in enumerate(Hebbs.iterrows()):
    ax1.plot(range(1, n_targets + 1), 
             row.values, 
             marker='o', 
             color=colors[c], 
             label=f'Cycle {cycle + 1}')

ax1.set_xlabel('Serial Position')
ax1.set_ylabel('Accuracy')
ax1.set_ylim(0, 1.05)
ax1.set_title(f'Hebb Lists, serial position curve, {n_simulations} simulations')


# Curves plot: Fillers
colors = plt.cm.Oranges(np.linspace(0.3, 1.0, n_cycles))

for c, (cycle, row) in enumerate(Fillers.iterrows()):
    ax2.plot(range(1, n_targets + 1), 
             row.values, 
             marker='o', 
             color=colors[c], 
             label=f'Cycle {cycle + 1}')
    
ax2.set_xlabel('Serial Position')
ax2.set_ylabel('Accuracy')
ax2.set_ylim(0, 1.05)
ax2.set_title(f'Filler Lists, serial position curve, {n_simulations} simulations')

plt.savefig(f'{output_dir}/curves.png')
plt.close()


if show_snapshot:
    os.startfile(output_dir)

if show_plots == 1:
    os.startfile(f'{output_dir}\\hebb_effect.png')
    os.startfile(f'{output_dir}\\curves.png')
elif show_plots == 2:
    os.startfile(f'{output_dir}\\hebb_effect.png')
