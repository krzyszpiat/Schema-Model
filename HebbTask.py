import numpy as np
import pandas as pd
from utils import cosim

def HebbParadigm(cfg, items, positions, output_dir):

    n_targets = cfg['n_targets'] 
    n_cycles = cfg['n_cycles']
    n_fillers = cfg['n_fillers']
    n_trials = cfg['n_trials']
    features = cfg['features']
    threshold = cfg['threshold']
    decay_rate = cfg['decay_rate']
    decay_slope = cfg['decay_slope']
    measure = cfg['measure']
    diag = cfg['diag']

    # prepare diagnostics logging
    if diag:
        f = open(f'{output_dir}\\snapshot.txt', 'w') # jeżeli drugi argument to 'a' then it appends

    def log_msg(msg):
        if diag:
            f.write(msg + '\n')

    # setting an order of trials within a block
    cycle_str = ["F"] * n_fillers + ["H"]
    exp_str = cycle_str * n_cycles

    # initializing the weight matrix
    m = np.zeros((features, features))

    results = []

    for t in range(n_trials):
        
        # starting a new cycle after each Hebb list
        cycle_index = (t // (n_fillers + 1))
        
        # setting the list type for the current trial
        trial_type = exp_str[t]

        # selecting categories for the current trial
        trial_pos = t % (n_fillers + 1)
        selection_start = trial_pos * n_targets
        selection = list(range(selection_start, selection_start + n_targets))

        # setting up the order of categories for the current trial
        if trial_type == "F":
            cat_seq = np.random.permutation(selection)
            condition = "Filler List"
        elif trial_type == "H":
            cat_seq = selection
            condition = "Hebb List"


    #################
    # Learning Phase
    ################# 

        encoded_associations = []

        # Hebbian learning
        for i in range(n_targets):
            ### ENCODING ###
            # selecting category to be presented
            cur_cat = cat_seq[i]
            # selecting item from the current category
            cur_item = items[(cur_cat, cycle_index)]# this line above can be hardcoded to cur_item = items[(cur_cat,0)] and simulate standard Hebb
            # associating current item with the current serial position
            outerProduct = np.outer(positions[i], cur_item)
            encoded_associations.append(outerProduct)
            m = m + outerProduct
            ### DECAY ###
            for d in range(i):
                # Setting the decay rate for the current item to be decayed
                effective_rate = decay_rate * (decay_slope ** (i - d))
                # Anti-Hebbian learning
                old_assoc = encoded_associations[d].copy()
                encoded_associations[d] *= (1 - effective_rate)
                m = m - (old_assoc - encoded_associations[d])
            

            

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

        # Calculating input-output weight matrix
        
        recalled_items = []
        sim_matrix = []

        for o in range(n_targets):
            row = []
            for i in range(n_targets):
                cur_cat = cat_seq[i]
                if measure == "dot":
                    row.append(np.dot(outputs[o], items[(cur_cat, cycle_index)]))
                elif measure == "cosim":
                    row.append(cosim(outputs[o], items[(cur_cat, cycle_index)]))
            sim_matrix.append(row)
       
      
      

        sim_df = pd.DataFrame(
            sim_matrix,
            index=[f"Output {i}" for i in cat_seq],
            columns=cat_seq)

        full_sim_df = sim_df.copy()

        log_msg('=' * 48)
        log_msg(f'Trial {t + 1} | {condition} | Cycle {cycle_index}')
        log_msg('=' * 48)
        log_msg(full_sim_df.round(2).to_string())        
        
        # Serial reconstruction

        accuracy = 0

        for item in range(n_targets):
            if sim_df.iloc[item].max() > threshold:
                recalled = sim_df.iloc[item].idxmax()
                acc = recalled == cat_seq[item]
                if acc: 
                    accuracy += 1
                sim_df = sim_df.drop(recalled, axis = 1)
                recalled_items.append(recalled)
            else:
                recalled_items.append("blank")
                acc = "omission"
            log_msg(f'\nPosition {item}:'
                    f'\n{'-' * 24}'
                    f'\nTarget: {cat_seq[item]}, Response: {recalled_items[item]}'
                    f'\nAccuracy: {"CORRECT" if acc == 1 else "incorrect" if acc == 0 else "omission"}')


        accuracy = accuracy/n_targets

        results.append({
            'trial': t + 1, 
            'cycle': cycle_index, 
            'type': condition, 
            'accuracy': accuracy,
            'targets': cat_seq,
            'responses': recalled_items})
        
        log_msg('\n')
        log_msg('*' * 30)
        log_msg(f'TRIAL {t+1} PERFORMANCE: {accuracy}')
        log_msg('*' * 30)


    
    if diag:
        f.close()

    return results