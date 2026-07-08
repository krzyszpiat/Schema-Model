import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
from stimuliGeneration import categoryGeneration, itemGeneration  # noqa: E402
from diagnostics import Diagnostics  # noqa: E402
from HebbTask import HebbParadigm  # noqa: E402
import config  # noqa: E402

cfg = {k: v for k, v in vars(config).items() if not k.startswith('_')}

np.random.seed(0)

categories = categoryGeneration(cfg)
items      = itemGeneration(cfg, categories)

diag = Diagnostics(level=cfg['diag_level'])
diag.set_context(simulation=1)

results = HebbParadigm(cfg, items, 'outputs/testing/debug', diag)
diag.save('outputs/testing/debug')
