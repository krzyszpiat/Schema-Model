#########################
#        FLAGS
#########################
# Collect diagnostics? (1 = yes)
diag = 1
diag_path = 'outputs\\snapshot.txt'

# Open plots? (1 = yes, 2 = only Hebb effect)
show_plots = 1
# Open snapshot? (1 = yes)
show_snapshot = 1

# Wchich similarity measure?
#measure = "cosim"
measure = "dot"

#########################
#        CONFIG
#########################
cat_scope = -1 # Scope of category vectors (1 = (0:1), -1 = (-1:1))
item_scope = -1 # Scope of item vectors (1 = (0:1), -1 = (-1:1))

n_simulations = 100
features = 100

n_targets = 8 # number of targets per trial
n_cycles = 10 # number of learning cycles
n_fillers = 2 # number of filler trials per cycle


n_categories = n_targets * (1 + n_fillers) # number of categories used in experiment
n_items = n_cycles #number of items per category
n_trials = n_cycles * (1 + n_fillers)

#########################
#    MODEL PARAMETERS
#########################
alpha = .4
threshold = 5
refresh_threshold = threshold
decay_rate = .8 # set to 0 to disable decay
decay_slope = .8
n_refreshing_cycles = 10
refresh_rate = .01