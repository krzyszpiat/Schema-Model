import numpy as np

# Cosine similarity function
def cosim(item1,item2):
    sim = np.dot(item1,item2) / (np.linalg.norm(item1) * np.linalg.norm(item2))
    return(sim)

def unit(v):
    return v / np.linalg.norm(v)