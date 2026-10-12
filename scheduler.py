import random

def Generating_popult(p, N__, TR):
    popult = []
    for _ in range(p):
        C = ''.join(random.choice('01') for _ in range(N__ * TR))
        popult.append(C)
    return popult

def Fitness(C, N__, TR):
    Overlapping = 0
    Consistency = 0
    for tr in range(TR):
        x = C[tr * N__:(tr + 1) * N__]
        num_courses = x.count('1')
        if num_courses > 1:
            Overlapping += (num_courses - 1)
            
    counting = [0] * N__
    for tr in range(TR):
        x = C[tr * N__:(tr + 1) * N__]
        for u in range(N__):
            if x[u] == '1':
                counting[u] += 1
                
    for count in counting:
        if count != 1:
            Consistency += abs(count - 1)
            
    Penalty = Overlapping + Consistency
    return -Penalty

def Parents(popult, fitenss):
    # Shift negative fitnesses so probabilities remain strictly positive
    min_fit = min(fitenss)
    shifted = [f - min_fit + 1 for f in fitenss]
    total_shifted = sum(shifted)
    pr = [s / total_shifted for s in shifted]
    parents = random.choices(popult, weights=pr, k=2)
    return parents

def crossover_1(p1, p2):
    w = random.randint(1, len(p1) - 1)
    off_1 = p1[:w] + p2[w:]
    off_2 = p2[:w] + p1[w:]
    return off_1, off_2

def crossover_2(p1, p2):
    w_1 = random.randint(1, len(p1) - 2)
    w_2 = random.randint(w_1 + 1, len(p1) - 1)
    off_1 = p1[:w_1] + p2[w_1:w_2] + p1[w_2:]
    off_2 = p2[:w_1] + p1[w_1:w_2] + p2[w_2:]
    return off_1, off_2

def Mutation(C, rate):
    mutation = ''.join(
        bit if random.random() > rate else ('1' if bit == '0' else '0')
        for bit in C
    )
    return mutation

def Genetic_Algorithm(N__, TR, p, m, rate):
    popult = Generating_popult(p, N__, TR)
    for _ in range(m):
        fitenss = [Fitness(chrom, N__, TR) for chrom in popult]
        new_popult = []
        for _ in range(p // 2):
            p1, p2 = Parents(popult, fitenss)
            off_1, off_2 = crossover_1(p1, p2)
            off_1 = Mutation(off_1, rate)
            off_2 = Mutation(off_2, rate)
            new_popult.extend([off_1, off_2])
        popult = new_popult
        
    best_C = max(popult, key=lambda chrom: Fitness(chrom, N__, TR))
    best_fitness = Fitness(best_C, N__, TR)
    return best_C, best_fitness

def main():
    print("Enter N (Courses) and T (Timeslots):")
    N__, TR = map(int, input().split())
    print(f"Enter {N__} course codes:")
    course_codes = [input().strip() for _ in range(N__)]
    
    p = 100
    m = 100
    rate = 0.01
    
    best_schedule, best_fitness = Genetic_Algorithm(N__, TR, p, m, rate)
    print("\nOptimal Chromosome:", best_schedule)
    print("Fitness Score:", best_fitness)

if __name__ == "__main__":
    main()
