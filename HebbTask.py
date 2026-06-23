import numpy as np
from utils import cosim

def HebbParadigm(items, positions, categories, n_targets, n_cycles, n_fillers, n_trials, features):

    # setting an order of trials within a block
    cycle_str = ["F"] * n_fillers + ["H"]
    exp_str = cycle_str * n_cycles

    # initializing the weight matrix
    m = np.zeros((features, features))

    results = []

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
            condition = "Filler List"
        elif trial_type == "H":
            cat_seq = selection
            condition = "Hebb List"


    #################
    # Learning Phase
    ################# 

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

        # Calculating accuracy
        
        sim_matrix = []

        for o in range(n_targets):
            row = []
            for i in range(n_targets):
                cur_cat = cat_seq[i]
                row.append(cosim(outputs[o], items[cur_cat][cycle_index - 1]))
            sim_matrix.append(row)

        accuracy = np.mean(np.argmax(sim_matrix, axis=1) == range(n_targets))

        results.append({'trial': t + 1, 'cycle': cycle_index, 'type': condition, 'accuracy': accuracy})


        
        # df = pd.DataFrame(
        #     sim_matrix,
        #     index=[f"Output {i+1}" for i in range(n_targets)],
        #     columns=[f"Item {i+1}" for i in range(n_targets)]
        # )
    
    
    return(results)

