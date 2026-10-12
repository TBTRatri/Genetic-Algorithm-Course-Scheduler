import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Genetic Algorithm Course Scheduler",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Genetic Algorithm Course Scheduler")
st.markdown("Constraint-satisfaction timetabling optimizer evolving binary chromosomes to eliminate course clashes.")

col_in, col_res = st.columns([1, 1.2])

with col_in:
    st.subheader("⚙️ Configuration")
    courses_text = st.text_area("Courses (comma-separated):", value="CSE110, MAT110, PHY112, CSE220")
    courses = [c.strip() for c in courses_text.split(",") if c.strip()]
    num_courses = len(courses)
    
    timeslots = st.number_input("Number of Timeslots (T):", min_value=1, max_value=10, value=max(len(courses), 4))
    pop_size = st.slider("Population Size:", min_value=20, max_value=200, value=100, step=10)
    generations = st.slider("Generations (Iterations):", min_value=10, max_value=300, value=100, step=10)
    mutation_rate = st.slider("Mutation Rate:", min_value=0.001, max_value=0.1, value=0.01, step=0.005)
    
    run_btn = st.button("🚀 Run Genetic Algorithm", type="primary")

def calculate_fitness_breakdown(chrom, n_c, n_t):
    overlap = 0
    for t in range(n_t):
        slot = chrom[t * n_c : (t + 1) * n_c]
        c_count = slot.count('1')
        if c_count > 1:
            overlap += (c_count - 1)
            
    course_counts = [0] * n_c
    for t in range(n_t):
        slot = chrom[t * n_c : (t + 1) * n_c]
        for idx in range(n_c):
            if slot[idx] == '1':
                course_counts[idx] += 1
                
    consistency = sum(abs(c - 1) for c in course_counts)
    total_penalty = overlap + consistency
    return -total_penalty, overlap, consistency, course_counts

def select_parents(population, fitness_scores):
    min_fit = min(fitness_scores)
    shifted = [f - min_fit + 1 for f in fitness_scores]
    total = sum(shifted)
    probs = [s / total for s in shifted]
    return random.choices(population, weights=probs, k=2)

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]

def mutate(chrom, rate):
    return ''.join(
        bit if random.random() > rate else ('1' if bit == '0' else '0')
        for bit in chrom
    )

if run_btn:
    # Genetic Algorithm Loop
    chrom_len = num_courses * timeslots
    population = [''.join(random.choice('01') for _ in range(chrom_len)) for _ in range(pop_size)]
    
    best_chrom = None
    best_fit = -999999
    
    progress = st.progress(0)
    for g in range(generations):
        fitness_vals = [calculate_fitness_breakdown(c, num_courses, timeslots)[0] for c in population]
        
        for c, f in zip(population, fitness_vals):
            if f > best_fit:
                best_fit = f
                best_chrom = c
                
        if best_fit == 0:
            break
            
        new_pop = []
        for _ in range(pop_size // 2):
            p1, p2 = select_parents(population, fitness_vals)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1, mutation_rate)
            c2 = mutate(c2, mutation_rate)
            new_pop.extend([c1, c2])
        population = new_pop
        progress.progress((g + 1) / generations)
        
    with col_res:
        st.subheader("📊 Optimal Schedule Found")
        b_fit, ov, con, c_counts = calculate_fitness_breakdown(best_chrom, num_courses, timeslots)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Best Fitness", b_fit)
        m2.metric("Overlap Penalty", ov)
        m3.metric("Consistency Penalty", con)
        
        st.markdown(f"**Chromosome String:** `{best_chrom}`")
        
        # Build tabular schedule
        grid = {f"Timeslot {t+1}": [] for t in range(timeslots)}
        for t in range(timeslots):
            slot_bits = best_chrom[t * num_courses : (t + 1) * num_courses]
            scheduled = [courses[i] for i, b in enumerate(slot_bits) if b == '1']
            grid[f"Timeslot {t+1}"].append(", ".join(scheduled) if scheduled else "— (Free)")
            
        df_schedule = pd.DataFrame(grid).T
        df_schedule.columns = ["Assigned Courses"]
        st.dataframe(df_schedule, use_container_width=True)
