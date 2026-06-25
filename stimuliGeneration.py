import numpy as np

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