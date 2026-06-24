import numpy as np
import pandas as pd
from utils import cosim

def HebbParadigm(items, positions, n_targets, n_cycles, n_fillers, n_trials, features, threshold, decay_rate, decay_slope):

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
                effective_rate = decay_rate * (decay_slope ** (i - d))
                m = m - effective_rate * encoded_associations[d]
            

            

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
                row.append(cosim(outputs[o], items[(cur_cat, cycle_index)]))
            sim_matrix.append(row)

        sim_df = pd.DataFrame(
            sim_matrix,
            index=[f"Output {i}" for i in cat_seq],
            columns=cat_seq)        
        
        # Serial reconstruction

        accuracy = 0

        for item in range(n_targets):
            if sim_df.iloc[item].max() > threshold:
                recalled = sim_df.iloc[item].idxmax()
                if recalled == cat_seq[item]: 
                    accuracy += 1
                sim_df = sim_df.drop(recalled, axis = 1)
                recalled_items.append(recalled)
            else:
                recalled_items.append("blank")

        accuracy = accuracy/n_targets

        results.append({
            'trial': t + 1, 
            'cycle': cycle_index, 
            'type': condition, 
            'accuracy': accuracy,
            'targets': cat_seq,
            'responses': recalled_items})

    
    return(results)