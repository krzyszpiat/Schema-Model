import numpy as np
import pandas as pd
from utils import cosim
from stimuliGeneration import positionGeneration

def HebbParadigm(cfg, items, output_dir, diag):

    n_targets = cfg['n_targets'] 
    n_cycles = cfg['n_cycles']
    n_fillers = cfg['n_fillers']
    n_trials = cfg['n_trials']
    features = cfg['features']
    threshold = cfg['threshold']
    decay_rate = cfg['decay_rate']
    decay_slope = cfg['decay_slope']
    measure = cfg['measure']
    snapshot_on = cfg['snapshot_on']
    n_refreshing_cycles = cfg['n_refreshing_cycles']
    refresh_threshold = cfg['refresh_threshold']
    refresh_rate = cfg['refresh_rate']
    decay_on   = cfg['decay_on']
    refresh_on = cfg['refresh_on']
    decay_asymptote = cfg['decay_asymptote']

    # prepare diagnostics logging
    if snapshot_on:
        f = open(f'{output_dir}\\snapshot.txt', 'w')

    def log_msg(msg):
        if snapshot_on:
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

        # creating positions' representations for the current trial
        positions = positionGeneration(cfg)

        diag.set_context(trial=t + 1, cycle=cycle_index, type=condition)        


        #################
        # LEARNING PHASE
        ################# 

        encoded_associations = []
        #associations_strengths = []
        targets = []


        for i in range(n_targets):

            ###########################
            ### TARGET PRESENTATION ###
            ###########################


            #=== ENCODING THE CURRENT ITEM ===#

            # Select category to be encoded on the current position
            cur_cat = cat_seq[i]

            # Select the item to be encoded from the selected category
            cur_item = items[(cur_cat, cycle_index)]# this line can be hardcoded to cur_item = items[(cur_cat,0)] and simulate standard Hebb
            targets.append(cur_item)

            # Associate the current target with the active serial position
            outerProduct = np.outer(positions[i], cur_item)
            encoded_associations.append(outerProduct)
            #associations_strengths.append(1.0)
            m = m + outerProduct
            
            diag.log('encoding', position=i, category=cur_cat, item_index=cycle_index, encoding_strength=np.linalg.norm(outerProduct))
            
            #=== DECAY OF THE OLDER ITEMS WHILE NEW ONE IS BEING ENCODED ===#

            # Dodać logowanie informacji
            if decay_on:
                for d in range(i):
                    # Setting the decay rate for the current item to be decayed
                    effective_rate = decay_rate * (decay_slope ** (i - d))
                    # Setting the decay asymptote for the current position-item pair
                    decay_floor = decay_asymptote * np.outer(positions[d], targets[d])
                    # Anti-Hebbian learning
                    old_assoc = encoded_associations[d].copy()
                    encoded_associations[d] = decay_floor + (encoded_associations[d] - decay_floor) * (1 - effective_rate)
                    m = m - (old_assoc - encoded_associations[d])

                

            ###############################
            ### INTER STIMULUS INTERVAL ###
            ###############################

            for c in range(n_refreshing_cycles):
                candidates = {}
                weakest = None
                availble_items = set(range(i+1))


                #=== REFRESHING ===#
                # -Dodać logowanie informacji

                ##  Retrieve the strongest item for each position ##
                if refresh_on:
                    for pos in (range(i + 1)):
                        
                        # Fetch a vector from the weight matrix using current position
                        cand = np.dot(positions[pos],m)
                        
                        # Redintegrate the fetched vector
                        redintegrated = None
                        stren = 0
                        winning = 99
                        for tar in availble_items: # Loop over candidates that were not redintegrated so far
                            red_cand_str = np.dot(cand, targets[tar])

                            # Diagnostics logging
                            diag.log('refreshing_redintegration', interval_index = i, refreshing_cycle = c, position=pos, candidate_index = tar, red_cand_str = red_cand_str)

                            # If the target from position tar is above refreshing threshold, choose it as redintegration candidate                      
                            if red_cand_str > refresh_threshold and red_cand_str > stren:                            
                                redintegrated = targets[tar]
                                stren = red_cand_str
                                winning = tar

                            

                        # Record the redintegrated representation
                        candidates[pos] = {'candidate': redintegrated, 'strength': stren, 'position': pos, 'winning': winning}

                        # Discard the selected item from the candidates for redintegration pool
                        if redintegrated is not None:
                            availble_items.discard(winning)

                        # Diagnostics logging
                        diag.log('refreshing_redintegration', refreshing_cycle = c, position=pos, interval_index = i, winning = winning, selected_stren = candidates[pos]['strength'])


                    # Select the position with the most decayed representation
                    valid_candidates = {pos: val for pos, val in candidates.items() if val['candidate'] is not None}

                    if valid_candidates:
                        weakest_strength = float('inf')

                        for pos in valid_candidates:
                            if valid_candidates[pos]['strength'] < weakest_strength:
                                weakest_strength = candidates[pos]['strength']
                                weakest = pos

                        # Refresh the weakest representation
                        refresh_asymptote = np.dot(candidates[weakest]['candidate'], candidates[weakest]['candidate'])
                        gap = max(0.0, 1.0 - weakest_strength / refresh_asymptote)
                        refreshing_strength = refresh_rate * gap

                        boost = np.outer(positions[weakest], candidates[weakest]['candidate']) * refreshing_strength
                        m = m + boost
                        encoded_associations[weakest] += boost
                        
                #=== DECAY ===#

                if decay_on:
                    for d in range(i):
                        if weakest is None or d != weakest: 
                            # Setting the decay rate for the current item to be decayed
                            effective_rate = (decay_rate * (decay_slope ** (i - d))) / n_refreshing_cycles

                            # Setting the decay asymptote for the current position-item pair
                            decay_floor = decay_asymptote * np.outer(positions[d], targets[d])

                            # Anti-Hebbian learning
                            old_assoc = encoded_associations[d].copy()
                            encoded_associations[d] = decay_floor + (encoded_associations[d] - decay_floor) * (1 - effective_rate)
                            m = m - (old_assoc - encoded_associations[d])
                            
                            diag.log('decay', at_position=i, decayed_position=d, effective_rate=effective_rate, strength_after=np.linalg.norm(encoded_associations[d])) 

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
                diag.log('retrieval',
                         output_position=o,
                         candidate_position=i,
                         candidate_category=cur_cat,
                         similarity=row[-1])
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
            diag.log('recall',
                     position=item,
                     target=cat_seq[item],
                     response=recalled_items[item],
                     accuracy="correct" if acc == 1 else "incorrect" if acc == 0 else "omission")


        accuracy = accuracy/n_targets

        diag.log('trials', accuracy=accuracy)

        results.append({
            'trial': t + 1, 
            'cycle': cycle_index, 
            'type': condition, 
            'accuracy': accuracy,
            'targets': cat_seq,
            'responses': recalled_items})

        # Post-recall decay
     
        for item in range(n_targets):
            decay_floor = decay_asymptote * np.outer(positions[item], targets[item])
            delta = encoded_associations[item] - decay_floor
            m = m - delta


        log_msg('\n')
        log_msg('*' * 30)
        log_msg(f'TRIAL {t+1} PERFORMANCE: {accuracy}')
        log_msg('*' * 30)


    
    if snapshot_on:
        f.close()

    return results
