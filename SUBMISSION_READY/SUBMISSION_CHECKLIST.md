# Part 2 DP Submission Checklist

## Verified Locally

- [x] Group ID 151 configuration matches the assignment: 5x5 grid, 2 rescue targets, 1 charger, 3 danger zones, 2 blocked cells, max battery 15, wind probability 20%, max steps 50.
- [x] Environment implements `reset()`, `step(action)`, `render()`, transition probabilities, battery updates, rescue removal, charging, wind, blocked-cell handling, and reward computation.
- [x] State includes `(row, col, battery, rescue_0, rescue_1, charge_0_claimed)` so the one-time charging reward cannot be farmed.
- [x] Value Iteration computes `V*` and `pi*` with threshold `theta = 1e-3`.
- [x] Latest local execution: 2,944 states, 11 iterations, final delta `0.000066`.
- [x] Demonstration rollout rescues both targets in 8 steps and terminates successfully.
- [x] Policy visualizations generated: full battery, low battery, one rescued.
- [x] State-value heatmaps generated: full battery, low battery, one rescued, all rescued terminal check.
- [x] Trajectory plot generated.
- [x] DP scalability discussion included.
- [x] Executed notebook and HTML export generated without notebook errors.

## Must Do In Virtual Lab Before Upload

- [ ] Open `Part2_DroneRescue_DP.ipynb` in the virtual lab.
- [ ] Run all cells in the virtual lab so the top output shows the virtual-lab timestamp and VM ID.
- [ ] Confirm the output still shows both rescues completed, not a charger loop.
- [ ] Export/download as PDF.
- [ ] Verify the PDF contains all convergence logs, policy plots, heatmaps, trajectory plot, scalability discussion, timestamp, and VM ID.
- [ ] Upload the PDF only, as required by the assignment PDF.

