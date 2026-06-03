# ✅ Part 2 DP — Virtual Lab Submission Checklist

> **Deadline: 8th June, 2026** | Submit 2 days before = **6th June**

---

## 🔴 CRITICAL (Must-Do Before Submission)

### 1. Run in Virtual Lab & Capture Screenshots

The assignment PDF (highlighted in yellow) **mandates** screenshots from the virtual lab with a visible timestamp.

**Steps:**
1. Open the BITS virtual lab portal
2. Launch Jupyter Notebook
3. Open `Part2_DroneRescue_DP_executed.ipynb`
4. **Kernel → Restart & Run All**
5. Take screenshots showing:
   - The **timestamp** printed at the top of the notebook output (Cell 1)
   - The **VM hostname/ID** printed at the top
   - Key outputs: convergence table, policy grid, heatmaps
6. Save screenshots with filenames like `vlab_screenshot_1.png`, `vlab_screenshot_2.png`

### 2. VM ID + Timestamp Already in Notebook ✅

The first code cell already prints:
```python
print(f"Execution Time  : {time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Virtual Machine ID: {os.uname().nodename}")
```
This will auto-print the VM ID and timestamp when run in the virtual lab.

### 3. Export as PDF

The assignment requires **PDF format only**.

```bash
# Option 1: From Jupyter menu
File → Download as → PDF via LaTeX

# Option 2: Via terminal in virtual lab
jupyter nbconvert --to pdf Part2_DroneRescue_DP_executed.ipynb

# Option 3: Export to HTML first, then print to PDF
jupyter nbconvert --to html Part2_DroneRescue_DP_executed.ipynb
# Open HTML in browser → Ctrl+P → Save as PDF
```

> ✅ You already have `Part2_DroneRescue_DP_executed.html` in the repo — open it in a browser and **Print → Save as PDF** as the quickest path.

---

## 🟡 VERIFY Before Export

| Item | Status | Notes |
|------|--------|-------|
| VM ID + Timestamp printed at top of notebook | ✅ Code exists | Must show actual VM output after running |
| All cells executed with outputs visible | ✅ `_executed.ipynb` exists | Re-run in virtual lab |
| Every function has a docstring/comment | ✅ All functions documented | 1 mark deducted if missing |
| `reset()`, `step()`, `render()` implemented | ✅ Present | Deliverable 1 |
| Value Iteration convergence printed (every iteration) | ✅ Present | Deliverable 2 |
| Convergence iterations, runtime, final delta shown | ✅ Present | Deliverable 2 |
| Policy visualisation with arrows (3 scenarios) | ✅ 3 PNGs saved | Deliverable 3 |
| Trajectory plot saved | ✅ `trajectory.png` | Deliverable 3 |
| State-value heatmaps (4 slices) | ✅ 4 PNGs saved | Deliverable 4 |
| DP Scalability Discussion in notebook | ✅ Deliverable 5 cell | Curse of Dimensionality + Deep RL |
| File naming: `Team # - DP` format | ⚠️ Rename PDF | PDF must follow naming convention |
| Virtual lab screenshots attached in PDF | 🔴 **TODO** | Must paste screenshots into PDF |

---

## 📁 Final PDF Should Contain

1. **Header cell** — Group ID, VM ID, Timestamp (from virtual lab run)
2. All code cells with outputs
3. Convergence table (every iteration printed)
4. Policy grid plots (3 battery scenarios)
5. Trajectory plot
6. Value heatmaps (4 scenarios)
7. Scalability discussion text
8. **Virtual lab screenshots** with timestamps appended at the end

---

## 📝 Submission File Naming

Per assignment instructions:
```
Team 151 - DP.pdf
```

---

## ⚠️ Scoring Criteria Reminder

From the assignment PDF, key factors include:
- Creativity, Originality, Uniqueness
- Code Modularity ✅ (class-based, modular functions)
- Representation ✅ (multiple visualisations)
- Reproducibility ✅ (`np.random.seed(151)` is set before the stochastic policy rollout)
- **Similarity to AI tool solutions** — reviewers check for this; ensure your explanations and comments are in your own words
