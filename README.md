# SChema Associative Model (ScAM)

Model simulates the process of incidental schema learning in the Hebb repetition paradigm as observed in [Piątkowski, Zawadzka \& Hanczakowski, 2026](https://psycnet.apa.org/record/2027-83839-001)

### Model parameters (and their value scope)

* **alpha** (0-1): similarity between the category prototype and category exemplars
* **threshold** (depending on similarity measure): degree of similarity between retrieved representations and response candidates; if below, response is omitted
* **decay\_rate** (0-1): initial value of decay strength, if set to 0 decay disabled
* **decay\_slope** (0-1): shape of the decay function, the higher the faster initial decay

## Mechanisms implemented so far

* Fully functional Hebb paradigm
* Within-category similarity of the targets
* Decay mechanism
  * Simulated through anti-Hebbian learning of the item-position associations
  * Exponential decay curve
  * Decay asymptote at 0

## What the model does so far

* Simulate benefit of the Hebb lists over Filler lists
  * Purely through superposition! No additional mechanisms required
* Simulate recency effect

## What the model does poorly

* No primacy effect
* Performance in the filler lists goes down instead of staying relatively constant
* No decay for the last item in the trial
  * Might be fixed by the last ISI

## What needs to be implemented

* Refreshing mechanism (currently tested)
* **Non-orthogonal serial positions**
* episodic LTM layer (?)
* semantic LTM layer (??)

