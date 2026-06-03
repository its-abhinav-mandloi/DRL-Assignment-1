# Virtual Lab Execution Guide - Part 2 DP

**Objective**: Execute the notebook in the virtual lab to generate outputs, capture screenshots with timestamps, and export to PDF for submission.

---

## Step 1: Open Jupyter Notebook in Virtual Lab

```bash
cd "Part - 2 DP"
jupyter notebook Part2_DroneRescue_DP.ipynb
```

This will open the notebook in your browser (likely `http://localhost:8888` or similar).

---

## Step 2: Execute All Cells

Navigate through and run each cell in order:

1. **Imports and Setup** → Shows VM ID and execution time
2. **Environment Configuration** → Grid layout and parameters
3. **MDP Formulation** → (Markdown, no execution)
4. **Drone Rescue Environment Class** → Defines environment
5. **Test the Environment** → Initial state + manual tests
6. **Value Iteration** → Runs DP algorithm
7. **Simulate Optimal Policy** → Trajectory display
8. **Policy Visualisation** → Arrow plots
9. **State-Value Analysis** → Heatmaps
10. **DP Scalability Discussion** → Text output
11. **Summary** → Final stats

**Keyboard shortcut**: `Ctrl+Shift+Enter` to execute all cells in order.

---

## Step 3: Capture Screenshots with Timestamps

### Screenshot 1: Initial Execution (Top of Notebook)
- **Content**: VM ID printout + Execution time + Grid layout
- **File**: `screenshot_01_vm_info.png`
- **How**: Select cells 1-2 and take screenshot

### Screenshot 2: Value Iteration Output
- **Content**: Iteration logs showing all convergence steps
- **File**: `screenshot_02_convergence_logs.png`
- **How**: Scroll to Value Iteration cell output, take screenshot of iteration log

### Screenshot 3: Convergence Plot
- **Content**: The convergence_plot.png displayed inline
- **File**: `screenshot_03_convergence_plot.png`
- **How**: Auto-generated plot output

### Screenshot 4: Policy Visualizations
- **Content**: All 3 policy grids (full battery, low battery, one rescued)
- **File**: `screenshot_04_policy_grids.png`
- **How**: From Policy Visualisation cell

### Screenshot 5: Trajectory
- **Content**: The trajectory.png plot
- **File**: `screenshot_05_trajectory.png`
- **How**: From Policy Visualisation cell

### Screenshot 6: Heatmaps
- **Content**: All 4 heatmaps displayed
- **File**: `screenshot_06_heatmaps.png`
- **How**: From State-Value Analysis cell

### Screenshot 7: Final Summary
- **Content**: Convergence stats + deliverables checklist
- **File**: `screenshot_07_summary.png`
- **How**: Final Summary cell output

---

## Step 4: Export to PDF

1. **File** → **Download as** → **PDF via HTML**
   - Or: **File** → **Export Notebook As** → **PDF**

2. **Name**: `Part2_DroneRescue_DP_SUBMISSION.pdf`

3. **Verify PDF contains**:
   - ✅ VM ID and execution timestamp at top
   - ✅ MDP Formulation section
   - ✅ All code cells with outputs
   - ✅ Convergence logs (all iterations)
   - ✅ 9 plot images (convergence, 3 policies, trajectory, 4 heatmaps)
   - ✅ State-value observations
   - ✅ DP scalability discussion
   - ✅ Summary table

---

## Step 5: Prepare Final Submission

Create a submission folder with:

```
Submission_Part2_DP/
├── Part2_DroneRescue_DP_SUBMISSION.pdf          # Main deliverable
├── screenshots/
│   ├── screenshot_01_vm_info.png
│   ├── screenshot_02_convergence_logs.png
│   ├── screenshot_03_convergence_plot.png
│   ├── screenshot_04_policy_grids.png
│   ├── screenshot_05_trajectory.png
│   ├── screenshot_06_heatmaps.png
│   └── screenshot_07_summary.png
├── EXECUTION_LOG.txt                            # Copy-paste of console output
└── README.txt                                    # Execution details
```

---

## Step 6: What to Expect in Output

### Convergence Log Sample
```
=============================================================
DELIVERABLE 2: Dynamic Programming — Value Iteration
=============================================================

Total states to evaluate: 2944

  Iteration    1 | delta = 38.99525000
  Iteration    2 | delta = 19.00000000
  Iteration    3 | delta = 18.05000000
  ...
  Iteration   10 | delta = 0.00140203
  Iteration   11 | delta = 0.00006589
  → Converged at iteration 11

--- Value Iteration Results ---
Converged in 11 iterations
Runtime: ~0.8 seconds
Final delta: 0.000066
Total states: 2944

V*(start state) = 30.1699
π*(start state) = Right
```

### Grid Rendering
```
Battery: 15/15 | Rescued: [0, 0] | Position: (0,0)
     C0    C1    C2    C3    C4
R0  [ S ][ · ][ 💨][ · ][ ☠ ]
R1  [ · ][ ▓ ][ · ][ 🧑][ · ]
R2  [ ☠ ][ · ][ ⚡][ · ][ 💨]
R3  [ · ][ ☠ ][ · ][ · ][ · ]
R4  [ ▓ ][ · ][ 🧑][ · ][ · ]
```

### Trajectory Output
```
Step-by-step trajectory:
  Step  0: pos=(0,0) bat=15 rescued=[0, 0] → Right  (R=-1)
  Step  1: pos=(0,1) bat=14 rescued=[0, 0] → Down   (R=-1)
  Step  2: pos=(1,1) bat=13 rescued=[0, 0] → Right  (R=-1)
  Step  3: pos=(1,3) bat=12 rescued=[1, 0] → Down   (R=+20)
  ...
  Step 10: pos=(2,2) bat=5 rescued=[1, 0] → Hover   (R=+5)
  ...
```

---

## Troubleshooting

### Issue: "matplotlib not found"
**Solution**: In virtual lab terminal, run:
```bash
pip install matplotlib numpy
```

### Issue: VM ID shows as `<UPDATE_THIS>`
**Solution**: Make sure you're running in the virtual lab, not locally. The code uses `os.uname().nodename` which only works on Unix-like systems.

### Issue: Plots not displaying
**Solution**: Ensure all cells executed. Try:
1. `Kernel` → `Restart & Run All`
2. Save notebook
3. Export to PDF

### Issue: Convergence takes too long
**Solution**: Normal. 5×5 grid with 2,944 states typically converges in about 10-15 iterations (~1 second).

---

## Final Submission Checklist

- [ ] Notebook executed in virtual lab
- [ ] All cells ran without errors
- [ ] VM ID printed at startup
- [ ] Convergence logs show all iterations
- [ ] All 9 plots displayed (convergence, policies, trajectory, heatmaps)
- [ ] PDF exported with all content
- [ ] Screenshots captured with timestamps (optional but recommended)
- [ ] Folder structure organized
- [ ] No sensitive information in submission
- [ ] File names match assignment requirements
- [ ] Ready to submit by 8th June 2026 (2 days before deadline)

---

## Submission Instructions

**Where to submit**: (Check assignment details or course portal)
- Usually: Assignment submission folder in learning management system
- Format: PDF only (per assignment instructions)
- Size limit: Check if any (usually 50-100 MB OK for notebook + images)

**What to submit**:
1. **Primary**: `Part2_DroneRescue_DP_SUBMISSION.pdf` 
2. **Optional but recommended**: Screenshots folder with timestamped images

**Deadline**: 8th June 2026 (submit 2 days early as instructed)

---

## Example VM ID Output

When notebook runs in virtual lab, you'll see:
```
============================================================
Part 2: Autonomous Drone Rescue Using Dynamic Programming
============================================================
Group ID        : 151
Execution Time  : 2026-05-25 14:23:45
Virtual Machine ID: node-vm-12345.lab.university.edu
============================================================
```

This proves execution in virtual lab (required by assignment).

---

## Contact Instructors (if issues arise)

- Subash: subasharun@wilp.bits-pilani.ac.in
- Divya K: divyak@wilp.bits-pilani.ac.in
- Dincy R Arikkat: dincyrarikkat@wilp.bits-pilani.ac.in

**Note**: Use official email with clarification request format from assignment PDF.

---

**Document Created**: 2026-05-23  
**For Group ID**: 151 (5×5 grid configuration)
