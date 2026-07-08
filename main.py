import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# Import functions for the script
from HebbTask import HebbParadigm
from stimuliGeneration import categoryGeneration, itemGeneration
from diagnostics import Diagnostics


# Import variables for the script
from config import *  # noqa: F403
import config
cfg = {k: v for k, v in vars(config).items() if not k.startswith('_')}

# Determine the folder for saving outputs
if save_unique:  # noqa: F405
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    output_dir = f'outputs\\{timestamp}'
else:
    output_dir = 'outputs\\latest'

os.makedirs(output_dir, exist_ok=True)

# Prepare bins for collecting data

diag = Diagnostics(level=cfg['diag_level'])

all_results = []

for sim in tqdm(range(n_simulations), desc="Simulations"):  # noqa: F405
    diag.set_context(simulation=sim + 1)

#######################
# Categories & Items
#######################

    categories = categoryGeneration(cfg)

    items = itemGeneration(cfg, categories)


############
# Hebb Task
############

    results = HebbParadigm(cfg, items, output_dir, diag)

    for r in results:
        r['simulation'] = sim + 1

    all_results.extend(results)

diag.save(output_dir)

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
plt.xticks(range(1, n_cycles + 1))  # noqa: F405
plt.legend()
plt.title(f'Hebb Lists vs Filler Lists, {n_simulations} simulations')  # noqa: F405
plt.savefig(f'{output_dir}/hebb_effect.png')
plt.close()


# Serial position curves
targets_df = results_df['targets'].apply(pd.Series)
responses_df = results_df['responses'].apply(pd.Series)

position_accuracy = (targets_df == responses_df)
curves_df = pd.concat([results_df, position_accuracy], axis=1)

Hebbs = curves_df[curves_df['type'] == 'Hebb List'].groupby('cycle')[list(range(n_targets))].mean()  # noqa: F405
Fillers = curves_df[curves_df['type'] == 'Filler List'].groupby('cycle')[list(range(n_targets))].mean()  # noqa: F405


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Curves plots: Hebb

colors = plt.cm.Blues(np.linspace(0.3, 1.0, n_cycles))  # noqa: F405

for c, (cycle, row) in enumerate(Hebbs.iterrows()):
    ax1.plot(range(1, n_targets + 1),  # noqa: F405
             row.values, 
             marker='o', 
             color=colors[c], 
             label=f'Cycle {cycle + 1}')

ax1.set_xlabel('Serial Position')
ax1.set_ylabel('Accuracy')
ax1.set_ylim(0, 1.05)
ax1.set_title(f'Hebb Lists, serial position curve, {n_simulations} simulations')  # noqa: F405
ax1.legend()


# Curves plot: Fillers
colors = plt.cm.Oranges(np.linspace(0.3, 1.0, n_cycles))  # noqa: F405

for c, (cycle, row) in enumerate(Fillers.iterrows()):
    ax2.plot(range(1, n_targets + 1),  # noqa: F405
             row.values, 
             marker='o', 
             color=colors[c], 
             label=f'Cycle {cycle + 1}')
    
ax2.set_xlabel('Serial Position')
ax2.set_ylabel('Accuracy')
ax2.set_ylim(0, 1.05)
ax2.set_title(f'Filler Lists, serial position curve, {n_simulations} simulations')  # noqa: F405
ax2.legend()

plt.savefig(f'{output_dir}/curves.png')
plt.close()


p = open(f'{output_dir}\\simulation parameters.txt', 'w') # jeżeli drugi argument to 'a' then it appends

p.write(f'SIMULATIONS = {n_simulations}\n\n')  # noqa: F405
parameters = ['phi',
              'alpha',
              'threshold',
              'refresh_threshold',
              'decay_rate',
              'decay_slope',
              'refresh_rate',
              'decay_asymptote',
              'hebbRetrievalProb'
              ]

for par in parameters:
    p.write(f'{par} = {cfg[par]}\n')

p.close()


if show_snapshot:  # noqa: F405
    os.startfile(f'{output_dir}\\snapshot.txt')

if show_plots == 1:  # noqa: F405
    os.startfile(f'{output_dir}\\hebb_effect.png')
    os.startfile(f'{output_dir}\\curves.png')
elif show_plots == 2:  # noqa: F405
    os.startfile(f'{output_dir}\\hebb_effect.png')
