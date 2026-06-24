import numpy as np

def categoryGeneration(n_categories, features, cat_scope):
    categories = []

    # Creating random vectors for categories
    for p in range(n_categories):

        if cat_scope == 1:
            random_vector = np.random.rand(features)
        elif cat_scope == -1:
            random_vector = np.random.randn(features)

        categories.append(random_vector)

    return categories


    # # Checking similarities between categories
    # catrel_matrix = np.vstack(categories)
    # cat_norms_list = []

    # for c in categories:
    #     norm = np.linalg.norm(c)
    #     unit_vector = c / norm
    #     cat_norms_list.append(unit_vector)
    # cat_norms = np.array(cat_norms_list)

def itemGeneration(n_categories, features, alpha, n_items, categories):

    # Creating items for each category
    items = {}

    for c in range(n_categories):
        cat = categories[c]
        #cat_items = []

        for i in range(n_items):
            random_vector = np.random.rand(features)
            item = alpha * cat + (1-alpha) * random_vector
            items[(c,i)] = item

    return items