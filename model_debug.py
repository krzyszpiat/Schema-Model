import numpy as np
from stimuliGeneration import categoryGeneration, itemGeneration, positionGeneration
from diagnostics import Diagnostics
from HebbTask import HebbParadigm
import config

cfg = {k: v for k, v in vars(config).items() if not k.startswith('_')}

np.random.seed(0)

positions  = positionGeneration(cfg)
categories = categoryGeneration(cfg)
items      = itemGeneration(cfg, categories)

diag = Diagnostics(level=cfg['diag_level'])
diag.set_context(simulation=1)

results = HebbParadigm(cfg, items, positions, 'outputs/testing/debug', diag)
diag.save('outputs/testing/debug')