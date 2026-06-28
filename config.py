#########################
#        FLAGS
#########################
# Collect diagnostics? (1 = yes)
diag = 1
diag_path = 'outputs\\snapshot.txt'

# print position curves? (1 = yes)
crvs = 1

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
alpha = 0.7
threshold = .9 # will need to be adjusted for the dot products
decay_rate = .6 # set to 0 to disable decay
decay_slope = .2