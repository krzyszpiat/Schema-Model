import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools

from tqdm import tqdm

from stimuliGeneration import categoryGeneration, itemGeneration
from diagnostics import Diagnostics
from HebbTask import HebbParadigm

import config

plots = 0

cfg = {k: v for k, v in vars(config).items() if not k.startswith('_')}

cfg['n_cycles'] = 1
cfg['n_trials'] = cfg['n_cycles'] * (1 + cfg['n_fillers'])


# PARAMETERS
param_grid = {
    'threshold': [20, 30, 40, 50, 60],
    'refresh_threshold': [5,10,15,20],
    'decay_rate': [round(x, 1) for x in np.linspace(0.5, 0.9, 5)],
    'decay_slope': [round(x, 1) for x in np.linspace(0.3, 0.7, 5)],
    'refresh_rate': [round(x, 1) for x in np.linspace(0.3, 0.9, 7)]
}

param_names = list(param_grid.keys())
param_combinations = list(itertools.product(*param_grid.values()))

sims = 100

# Start estimating
all_results = []
diag = Diagnostics(enabled=False)


for comb in tqdm(param_combinations, desc="Overall progress", position=0):
    comb_dict = dict(zip(param_names, comb))
    cfg.update(comb_dict)

    for sim in tqdm(range(sims), desc=f"{comb_dict}", position=1, leave=False):
        np.random.seed(sim)

        categories = categoryGeneration(cfg)
        items      = itemGeneration(cfg, categories)

        results = HebbParadigm(cfg, items, 'outputs/testing/firstCycle', diag)
        
        for r in results:
            r.update(comb_dict)

        all_results.extend(results)

results_df = pd.DataFrame(all_results)

targets_df = results_df['targets'].apply(pd.Series)
responses_df = results_df['responses'].apply(pd.Series)

position_accuracy = (targets_df == responses_df)
curves_df = pd.concat([results_df, position_accuracy], axis=1)

summary_df = (
    curves_df
    .groupby(param_names + ['type'])[list(range(cfg['n_targets']))]
    .mean()
    .reset_index()
)



summary_df.to_csv('outputs/testing/firstCycle/param_sweep_results.csv', index=False)





# Serial position curves
if plots == 1:

    Hebbs = curves_df[curves_df['type'] == 'Hebb List'][list(range(cfg['n_targets']))].mean()
    Fillers = curves_df[curves_df['type'] == 'Filler List'][list(range(cfg['n_targets']))].mean()


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))


    for combo in param_combinations:
        combo_dict = dict(zip(param_names, combo))
        mask = np.all([curves_df[k] == v for k, v in combo_dict.items()], axis=0)
        subset = curves_df[mask]

        Hebbs   = subset[subset['type'] == 'Hebb List'][list(range(cfg['n_targets']))].mean()
        Fillers = subset[subset['type'] == 'Filler List'][list(range(cfg['n_targets']))].mean()

        label = ', '.join(f'{k}={v}' for k, v in combo_dict.items())
        ax1.plot(Fillers.index, Fillers.values, label=label)
        ax2.plot(Hebbs.index, Hebbs.values, label=label)


    # Curves plot: Fillers
    ax1.plot(Fillers.index, Fillers.values)

    ax1.set_xlabel('Serial Position')
    ax1.set_ylabel('Accuracy')
    ax1.set_ylim(0, 1.05)
    ax1.set_title(f'Filler Lists, serial position curve, {cfg['n_simulations']} simulations')  # noqa: F405
    ax1.legend()


    # Curves plots: Hebb

    ax2.plot(Hebbs.index, Hebbs.values)

    ax2.set_xlabel('Serial Position')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.05)
    ax2.set_title(f'Hebb Lists, serial position curve, {cfg['n_simulations']} simulations')  # noqa: F405
    ax2.legend()


    plt.savefig('outputs/testing/firstCycle/curves.png')
    plt.close()
