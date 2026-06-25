# SChema Associative Model (SCAM)
Model simulates the process of incidental schema learning in the Hebb repetition paradigm as observed in [Piątkowski, Zawadzka & Hanczakowski, 2026](https://psycnet.apa.org/record/2027-83839-001)
### Model parameters (and their value scope)
- **alpha** (0-1): similarity between the category prototype and category exemplars
- **threshold** (depending on similarity measure): degree of similarity between retrieved representations and response candidates; if below, response is omitted
- **decay_rate** (0-1): initial value of decay strength, if set to 0 decay disabled
- **decay_slope** (0-1): shape of the decay function, the lower the faster initial decay
## Mechanisms implemented so far
- Fully functional Hebb paradigm
- Within-category similarity of the targets
- *Decay mechanism (still being tested)*
## What the model does so far
- Simulate benefit of the Hebb lists over Filler lists
  - Purely through superposition! No additional mechanisms required
- *Simulate recency effect (not sure if for correct reasons though)*
## What the model does poorly
- No primacy effect
- Performance in the filler lists go down instead of staying relatively constant
## What needs to be implemented
- **Refreshing mechanism**
- Orthogonal serial positions
- episodic LTM layer (?)
- semantic LTM layer (??)
