# 🚁 Part 2 — Autonomous Drone Rescue Using Dynamic Programming

## Design Document

**Course**: Deep Reinforcement Learning (DRL NSP4)  
**Assignment**: Assignment 1 — Part 2 (DP)  
**Total Marks**: 5  
**Author**: Abhinav Mandloi  
**Group ID**: **151** (last digit = **1**)  
**Date Created**: 2026-05-23  
**Last Updated**: 2026-05-23  

---

## Table of Contents

1. [Problem Overview](#1-problem-overview)
2. [Group-Specific Configuration](#2-group-specific-configuration)
3. [MDP Formulation](#3-mdp-formulation)
4. [Environment Design](#4-environment-design)
5. [Dynamic Programming Algorithm](#5-dynamic-programming-algorithm)
6. [Visualization Plan](#6-visualization-plan)
7. [Analysis Plan](#7-analysis-plan)
8. [Scalability Discussion Outline](#8-scalability-discussion-outline)
9. [File Structure](#9-file-structure)
10. [Design Decisions Log](#10-design-decisions-log)
11. [Open Issues & Questions](#11-open-issues--questions)
12. [References](#12-references)

---

## 1. Problem Overview

### 1.1 Scenario

An autonomous rescue drone is deployed in a disaster-hit city after an earthquake. The city
is represented as a **grid world**. The drone must:

- **Rescue** stranded civilians (reach rescue target cells)
- **Avoid** dangerous areas (fire, radiation, unstable structures)
- **Manage** limited battery power
- **Recharge** at charging stations before battery depletion
- **Handle** wind zones that introduce stochastic movement

### 1.2 Objective

Design and implement an RL agent using **Dynamic Programming** (Value Iteration or
Policy Iteration) to compute the **optimal policy** — the best action to take in every
possible state — that maximises total rescue reward.

### 1.3 Deliverables

| # | Deliverable | Marks | Status |
|---|-------------|-------|--------|
| 1 | Custom Drone Rescue Environment | 1 | ⬜ Not Started |
| 2 | DP Solution (Value / Policy Iteration) | 2 | ⬜ Not Started |
| 3 | Policy Visualisation | 1 | ⬜ Not Started |
| 4 | State-Value Analysis | 1 | ⬜ Not Started |
| 5 | DP Scalability Discussion | 1 | ⬜ Not Started |

---

## 2. Group-Specific Configuration

> **⚠️ Fill in your Group ID below. All other values will be derived from it.**

| Parameter | Rule | Your Value |
|-----------|------|------------|
| **Group ID** | — | **151** |
| **Last digit of Group ID** | — | **1** |
| **Grid Size** | 0–4 → 5×5 | **5×5** |
| **Rescue Targets** | 0–4 → 2 | **2** |
| **Charging Stations** | 0–4 → 1 | **1** |
| **Danger Zones** | 0–4 → 3 | **3** |
| **Blocked Cells** | 0–4 → 2 | **2** |
| **Max Battery** | Odd → 15 | **15** |
| **Wind Probability** | 0–4 → 20% | **20%** |
| **Max Steps** | 5×5 → 50 | **50** |

### 2.1 Grid Layout

```
Group ID: 151 | 5×5 Grid
     Col0  Col1  Col2  Col3  Col4
Row0 [ S ] [ F ] [ W ] [ F ] [ D ]
Row1 [ F ] [ X ] [ F ] [ R ] [ F ]
Row2 [ D ] [ F ] [ C ] [ F ] [ W ]
Row3 [ F ] [ D ] [ F ] [ F ] [ F ]
Row4 [ X ] [ F ] [ R ] [ F ] [ F ]
```

**Grid Design Rationale:**
- **S at (0,0)**: Fixed per assignment rules
- **R at (1,3) and (4,2)**: Spread apart — drone must plan a multi-stop route
- **C at (2,2)**: Central position — reachable from most of the grid
- **D at (0,4), (2,0), (3,1)**: Create obstacles along direct paths to rescue targets
- **X at (1,1), (4,0)**: Block shortcuts, force longer routes
- **W at (0,2), (2,4)**: On key paths — introduce stochastic risk in route planning

### 2.2 Design Rules for Grid Placement

- Start position (S) is **fixed at top-left corner** (0, 0)
- Placement of R, C, D, X, W cells must be **clearly explained and justified**
- Grid should create **interesting decision-making scenarios**:
  - Rescue targets should NOT all be trivially reachable
  - Charging stations should be strategically placed
  - Danger zones should create meaningful obstacles
  - Wind zones should affect key paths

---

## 3. MDP Formulation

### 3.1 State Space (S)

Each state is a **tuple** containing:

```
state = (row, col, battery_level, rescue_status_1, rescue_status_2, ...)
```

| Component | Type | Range | Description |
|-----------|------|-------|-------------|
| `row` | int | 0 to GRID_ROWS-1 | Drone row position |
| `col` | int | 0 to GRID_COLS-1 | Drone column position |
| `battery` | int | 0 to MAX_BATTERY | Current battery level |
| `rescue_i` | bool | 0 or 1 | Whether rescue target i has been rescued |

**State space size calculation:**

```
|S| = GRID_ROWS × GRID_COLS × (MAX_BATTERY + 1) × 2^NUM_RESCUE_TARGETS
     - (blocked_cells × (MAX_BATTERY + 1) × 2^NUM_RESCUE_TARGETS)
```

For a 5×5 grid, battery=10, 2 rescue targets:
```
|S| = 25 × 11 × 4 = 1,100 states (minus blocked cell states)
```

For a 6×6 grid, battery=15, 3 rescue targets:
```
|S| = 36 × 16 × 8 = 4,608 states (minus blocked cell states)
```

### 3.2 Action Space (A)

| Action | Index | Movement (Δrow, Δcol) |
|--------|-------|-----------------------|
| Up | 0 | (-1, 0) |
| Down | 1 | (+1, 0) |
| Left | 2 | (0, -1) |
| Right | 3 | (0, +1) |
| Hover | 4 | (0, 0) |

**Valid action rules:**
- All 5 actions are always available (invalid moves = stay in place + burn battery)
- Moving into a blocked cell (X) or off-grid → drone stays, battery still consumed

### 3.3 Transition Function P(s'|s, a)

The transition function is the **core complexity** of this environment.

#### 3.3.1 Normal Cells (S, F, R, C, D)

- **Deterministic**: P(intended_next_state | s, a) = 1.0
- Movement action → drone moves to intended cell (if valid)
- Hover on non-charging cell → drone stays, battery -= 1

#### 3.3.2 Wind Cells (W)

When the drone is **currently on a wind cell** and takes a movement action:

```
With probability (1 - P_WIND):
    → Intended movement succeeds

With probability P_WIND:
    → Movement direction is uniformly random from {Up, Down, Left, Right}
    → Each direction has probability P_WIND / 4
```

**Effective transition probabilities from a wind cell:**

```
P(intended_direction) = (1 - P_WIND) + (P_WIND / 4)
P(each_other_direction) = P_WIND / 4
```

For P_WIND = 0.20:
```
P(intended) = 0.80 + 0.05 = 0.85
P(each other) = 0.05
```

For P_WIND = 0.30:
```
P(intended) = 0.70 + 0.075 = 0.775
P(each other) = 0.075
```

> **Note**: Hover action on wind cell → stays in place, no wind effect on hover (hover is not a "movement action")

#### 3.3.3 State Transitions Summary

After determining the destination cell, apply these updates:

| Destination Cell | Battery Update | Reward | Additional Effect |
|-----------------|---------------|--------|-------------------|
| F (Free) | battery -= 1 | -1 | — |
| S (Start) | battery -= 1 | -1 | Treated as free cell |
| D (Danger) | battery -= 1 | -10 | No termination |
| R (Rescue, not yet rescued) | battery -= 1 | +20 | Mark target as rescued, cell → F |
| R (Rescue, already rescued) | battery -= 1 | -1 | Treated as free cell |
| C (Charging) | battery = MAX | +5 | Battery fully restored |
| W (Wind) | battery -= 1 | -1 | Wind affects NEXT move from here |
| X (Blocked) / Off-grid | battery -= 1 | -1 | Drone stays in current position |
| Hover on C | battery = min(battery + 2, MAX) | -1 | Battery +2 (capped); no repeated charging reward |
| Hover on non-C | battery -= 1 | -1 | — |

### 3.4 Reward Structure (R)

| Event | Reward |
|-------|--------|
| Rescue target reached (first time) | **+20** |
| Enter danger zone | **-10** |
| Battery exhausted (reaches 0) | **-20** |
| Reach charging station | **+5** |
| Regular movement / hover | **-1** |

### 3.5 Discount Factor (γ)

- **Chosen value**: `γ = 0.95` *(design decision — see section 10)*
- Rationale: Balances immediate rescue urgency with long-term planning (battery management)

### 3.6 Terminal States

An episode terminates when:

1. **Battery = 0** → terminal reward = -20
2. **All rescue targets rescued** → episode success
3. **Step count exceeds limit** (50 for 5×5 / 75 for 6×6) → forced termination

> **For DP purposes**: Terminal states have V(s_terminal) = 0 (no future rewards possible). The -20 penalty for battery=0 is part of the transition reward, not the terminal state value.

---

## 4. Environment Design

### 4.1 Class Structure

```python
class DroneRescueEnv:
    """Custom grid-world environment for autonomous drone rescue."""

    def __init__(self, grid_layout, max_battery, wind_prob, max_steps):
        """
        Initialize the environment.

        Args:
            grid_layout: 2D list of cell types (S, F, D, R, C, W, X)
            max_battery: Maximum battery capacity
            wind_prob: Probability of wind disturbance on W cells
            max_steps: Maximum steps per episode
        """

    def reset(self):
        """Reset environment to initial state. Returns initial state tuple."""

    def step(self, action):
        """
        Execute one action.

        Args:
            action: int (0=Up, 1=Down, 2=Left, 3=Right, 4=Hover)

        Returns:
            next_state: tuple (row, col, battery, *rescue_statuses)
            reward: float
            done: bool
            info: dict with debug info
        """

    def render(self):
        """Print current grid state with drone position, battery, rescue status."""

    def get_all_states(self):
        """Return list of all valid states for DP enumeration."""

    def get_valid_actions(self, state):
        """Return list of valid actions from given state."""

    def get_transition_prob(self, state, action):
        """
        Return transition probabilities for DP.

        Returns:
            list of (probability, next_state, reward, done) tuples
        """

    def encode_state(self, row, col, battery, rescue_status):
        """Convert state components to a hashable state tuple."""

    def decode_state(self, state):
        """Convert state tuple back to components."""
```

### 4.2 State Encoding

```python
# State as a tuple (hashable, can be dict key):
state = (row, col, battery, rescue_0, rescue_1)  # for 2 targets
state = (row, col, battery, rescue_0, rescue_1, rescue_2)  # for 3 targets

# Example:
# Drone at (2,3), battery=7, target 0 rescued, target 1 not rescued
state = (2, 3, 7, 1, 0)
```

### 4.3 Key Implementation Notes

1. **Wind cell logic**: Wind only affects movement actions when drone is ON a wind cell. Hover is not affected.
2. **Boundary handling**: If movement would go off-grid or into X cell → drone stays, still loses 1 battery.
3. **Charging station entry vs hover**:
   - Entering C → battery becomes MAX, reward = +5
   - Hovering on C → battery += 2 (capped at MAX), regular action reward = -1
4. **Rescue target removal**: Once rescued, the cell behaves as F for all future states.
5. **Battery = 0 is absorbing**: No further actions possible, episode ends.

---

## 5. Dynamic Programming Algorithm

### 5.1 Algorithm Choice

**Value Iteration** *(selected for simplicity)*

### 5.2 Pseudocode

```
FUNCTION ValueIteration(env, gamma=0.95, theta=0.001):
    # Step 1: Initialize
    states = env.get_all_states()
    V = {s: 0.0 for s in states}
    iteration = 0

    # Step 2: Iterate until convergence
    REPEAT:
        delta = 0
        FOR each state s in states:
            IF s is terminal:
                CONTINUE

            v_old = V[s]

            # Compute value for each action
            action_values = []
            FOR each action a in env.get_valid_actions(s):
                value = 0
                FOR (prob, s_next, reward, done) in env.get_transition_prob(s, a):
                    IF done:
                        value += prob * reward
                    ELSE:
                        value += prob * (reward + gamma * V[s_next])
                action_values.append(value)

            V[s] = max(action_values)
            delta = max(delta, |v_old - V[s]|)

        iteration += 1
    UNTIL delta < theta

    # Step 3: Extract optimal policy
    policy = {}
    FOR each state s in states:
        IF s is terminal:
            CONTINUE
        best_action = argmax_a [ Σ P(s'|s,a) * (R + γ * V[s']) ]
        policy[s] = best_action

    RETURN V, policy, iteration
```

### 5.3 Convergence Tracking

Track and report:
- **Number of iterations** until convergence
- **Runtime** (wall-clock time using `time.time()`)
- **Final delta** (max value change in last iteration)
- **Delta history** per iteration (for convergence plot)

### 5.4 Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| γ (discount) | 0.95 | Balances urgency with planning |
| θ (threshold) | 0.001 | As specified in assignment |

---

## 6. Visualization Plan

### 6.1 Policy Grid (Deliverable 3)

- **Arrow map**: For a fixed (battery, rescue_status), show optimal action at each cell
  - ↑ ↓ ← → for movement, ● for hover
- **Color-coded cells**: S=green, D=red, R=gold, C=blue, W=cyan, X=gray
- **Multiple grids**: Show how policy changes at different battery levels

### 6.2 Trajectory Animation

- Simulate drone following π* from start state
- Show step-by-step movement on grid
- Display battery level, rescued targets at each step
- Can use matplotlib animation or frame-by-frame plots

### 6.3 Convergence Plot

- X-axis: iteration number
- Y-axis: delta (max value change)
- Show exponential decay toward θ

---

## 7. Analysis Plan

### 7.1 State-Value Heatmap (Deliverable 4)

**Slice 1**: Fix all rescue targets = not rescued, battery = MAX
- Plot V*(row, col) as 2D heatmap
- Expected: High near R cells, low near D cells

**Slice 2**: Fix all rescue targets = not rescued, battery = LOW (e.g., 3)
- Expected: High only near C cells (must recharge), low elsewhere

**Slice 3**: Fix target_0 = rescued, target_1 = not rescued, battery = MAX
- Expected: Policy focuses on remaining target

### 7.2 Patterns to Explain

- Why cells near rescue targets have high values
- Why cells near danger zones have low values
- How battery level dramatically changes the value landscape
- The "charging corridor" — states where the drone must prioritize charging
- How wind zones reduce value compared to equivalent non-wind cells

---

## 8. Scalability Discussion Outline

### 8.1 Curse of Dimensionality

| Scenario | States | Feasible for DP? |
|----------|--------|-------------------|
| 5×5, battery=10, 2 targets | ~1,100 | ✅ Yes |
| 6×6, battery=15, 3 targets | ~4,608 | ✅ Yes |
| 10×10, battery=20, 5 targets | ~672,000 | ⚠️ Slow |
| 20×20, battery=30, 10 targets | ~12.6 billion | ❌ Impossible |

### 8.2 Why DP Fails at Scale

- Must enumerate ALL states
- Must compute transitions for ALL (state, action) pairs
- Memory grows linearly with |S|, computation grows as |S| × |A|
- Adding one rescue target **doubles** the state space

### 8.3 Deep RL Alternatives

- Function approximation: Neural networks estimate V(s) or π(s)
- Don't need to enumerate states — generalize from samples
- Examples: DQN, PPO, A3C
- Trade-off: No optimality guarantee, but can handle massive state spaces

### 8.4 Real-World Connection

- Actual drones: continuous position, velocity, wind, sensor noise
- Partial observability: drone can't see entire grid
- Multi-agent: multiple drones coordinating
- DP is foundational theory; Deep RL is what scales to reality

---

## 9. File Structure

```
Part - 2 DP/
├── DESIGN_DOC.md              ← This document
├── drone_rescue_env.py        ← Environment class
├── dp_solver.py               ← Value Iteration implementation
├── visualisation.py           ← Policy arrows, heatmaps, trajectories
├── analysis.py                ← State-value analysis
├── main.py                    ← Main execution script
├── Part2_DroneRescue.ipynb    ← Final Jupyter notebook for submission
└── screenshots/               ← Virtual lab screenshots with timestamps
```

> **Note**: Final submission will be a single Jupyter notebook that integrates everything.
> The separate .py files are for modular development.

---

## 10. Design Decisions Log

| # | Date | Decision | Rationale | Alternatives Considered |
|---|------|----------|-----------|------------------------|
| 1 | 2026-05-23 | Use Value Iteration (not Policy Iteration) | Simpler to implement; single loop; assignment allows either | Policy Iteration (more iterations but each converges faster) |
| 2 | 2026-05-23 | γ = 0.95 | Standard choice; balances immediate rescue urgency with battery planning | γ=0.99 (more far-sighted), γ=0.9 (more greedy) |
| 3 | 2026-05-23 | State = tuple (row, col, battery, *rescue_status) | Minimal required state per assignment; hashable for dict lookup | Could add step_count to state (but increases state space significantly) |
| 4 | 2026-05-23 | Hover on wind cell = no wind effect | Hover is not a "movement action"; wind only disturbs movement per assignment wording | Could apply wind to hover too (stricter interpretation) |
| 5 | TBD | Grid layout placement | — | — |

---

## 11. Open Issues & Questions

- [ ] **Group ID not yet determined** — all config values are TBD
- [ ] **Hover on wind cell**: Does wind affect hover? Assumed NO (hover ≠ movement action)
- [ ] **Charging station reward**: Is +5 given every time you enter/hover, or only first entry?
     → Assumed: +5 every time (entering or hovering on C)
- [ ] **Step count in state**: Should step count be part of state for DP? 
     → Decision: NO (would massively increase state space; handle via episode simulation)
- [ ] **Discount factor**: Assignment doesn't specify γ — chosen 0.95, document justification

---

## 12. References

1. **Sutton & Barto** — *Reinforcement Learning: An Introduction* (2nd ed.), Chapters 3–4
2. **David Silver RL Lectures** — Lectures 1–3 (Introduction, MDPs, Planning by DP)
3. **Assignment PDF** — DRL NSP4 Assignment 1, Part #2 (Pages 5–10)
4. **OpenAI Gym Frozen Lake** — Practice environment for DP

---

*This is a living document. Update it as design decisions are made and implementation progresses.*
