# Genetic Algorithm Course Scheduling Optimizer

A constraint-satisfaction optimization engine solving university timetable scheduling using **Genetic Algorithms (GA)** in Python. The system represents schedule assignments as flattened binary bitstrings and evolves candidate allocations by minimizing timeslot clashes and course assignment inconsistencies.

---

## 📌 Problem Formulation

Given $N$ distinct academic courses and $T$ available timeslots, a valid schedule must assign each course to exactly one timeslot while ensuring no two courses overlap in the same timeslot.

### Chromosome Representation
- Chromosome length: $N \times T$ bits.
- Divided into $T$ sequential segments of length $N$.
- Bit at index $(t \times N + i) = 1$ indicates that course $i$ is scheduled in timeslot $t$.

### Fitness Function & Penalties
The objective is to minimize total constraint violations:
$$\text{Penalty}_{\text{total}} = \text{Penalty}_{\text{overlap}} + \text{Penalty}_{\text{consistency}}$$

$$\text{Fitness}(C) = -\text{Penalty}_{\text{total}}$$

1. **Overlap Penalty:** If more than one course is assigned to timeslot $t$, adds $(\text{count}_t - 1)$.
2. **Consistency Penalty:** For each course $i$, penalizes deviations from exactly one assignment: $\vert{}\text{occurrences}_i - 1\vert{}$.
3. An optimal, conflict-free schedule achieves $\text{Fitness} = 0$.

---

## 🧬 Genetic Operators

- **Selection:** Roulette-wheel probability distribution normalized across non-positive fitness ranges.
- **Crossover:** Single-point and two-point crossover slicing.
- **Mutation:** Configurable bit-flip mutation rate across all loci.

---

## 🛠️ Usage

```bash
python main.py
