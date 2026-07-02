import numpy as np
from utils import unit

def categoryGeneration(cfg):
    n_categories = cfg['n_categories']
    features = cfg['features']
    cat_scope = cfg['cat_scope']
    
    categories = []

    # Creating random vectors for categories
    for p in range(n_categories):

        if cat_scope == 1:
            random_vector = np.random.rand(features)
        elif cat_scope == -1:
            random_vector = np.random.randn(features)

        categories.append(random_vector)

    return categories

def itemGeneration(cfg, categories):
    n_categories = cfg['n_categories']
    features = cfg['features']
    alpha = cfg['alpha']
    n_items = cfg['n_items']
    item_scope = cfg['item_scope']


    # Creating items for each category
    items = {}

    for c in range(n_categories):
        cat = categories[c]
        #cat_items = []

        for i in range(n_items):
            if item_scope == 1:
                random_vector = np.random.rand(features)
            elif item_scope == -1:
                random_vector = np.random.randn(features)
            item = alpha * cat + (1-alpha) * random_vector
            items[(c,i)] = item

    return items

def positionGeneration(cfg):
    pos_switch = cfg['positions']
    phi = cfg['phi']
    features = cfg['features']
    n_targets = cfg['n_targets']
    positions = []

    if pos_switch == "o":
    # Creating random vectors for serial positions
        for p in range(n_targets):
            random_vector = np.random.rand(features)
            positions.append(random_vector)

        # Making the position vectors orthogonal
        pos_matrix = np.column_stack(positions)

        Q, R = np.linalg.qr(pos_matrix) # QR decomposition 

        for p in range(n_targets):
            position = Q[:,p]
            positions.append(position)

    elif pos_switch == "no":

        positions.append(unit(np.random.randn(features)))

        for p in range(n_targets-1):
            noise = unit(np.random.randn(features))
            position_vector = phi * positions[p] + (1 - phi) * noise
            position_vector = unit(position_vector)
            positions.append(position_vector)

    return positions