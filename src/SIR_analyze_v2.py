import numpy as np
import matplotlib.pyplot as plt

size = 50
number_patient0 = 75

def while_func(infection_prob: float, recovery_prob: float):
    grid = np.zeros((size, size), dtype=int)
    
    # Infect initial patients
    init_infected = np.random.choice(range(size * size), number_patient0, replace=False)
    for id in init_infected:
        grid[id // size, id % size] = 1  # 0=S, 1=I, 2=R
    
    current_grid = grid.copy()
    next_grid = grid.copy()

    all_S = size * size - number_patient0
    all_I = number_patient0
    all_R = 0
    iterator = 0

    while all_R < size * size and iterator < 1000:
        for i in range(size):
            for j in range(size):
                state = current_grid[i, j]
                
                if state == 1:  # Infected
                    if np.random.rand() < recovery_prob:
                        next_grid[i, j] = 2
                        all_I -= 1
                        all_R += 1
                    else:
                        next_grid[i, j] = 1  # Remains infected
                elif state == 0:  # Susceptible
                    infection_risk = 0
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = (i + di) % size, (j + dj) % size  # Wrap around (torus)
                        if current_grid[ni, nj] == 1:
                            infection_risk += infection_prob
                    if np.random.rand() < infection_risk:
                        next_grid[i, j] = 1
                        all_S -= 1
                        all_I += 1
                    else:
                        next_grid[i, j] = 0  # Remains susceptible
                else:
                    next_grid[i, j] = 2  # Recovered stays recovered

        #print(f"S {all_S}, I {all_I}, R {all_R}, sum {all_S + all_I + all_R}")
        # Swap grids
        current_grid, next_grid = next_grid, current_grid
        iterator += 1

    return [all_S, all_R]


values = np.arange(0, 0.5, 0.01)
size2 = len(values)
grid_a_b = np.zeros((size2, size2), dtype=float)

for i_idx, i in enumerate(values):
    for j_idx, j in enumerate(values):
        tSUM_S = 0
        tSUM_R = 0

        for _ in range(10):
            tS, tR = while_func(i, j)
            tSUM_S += tS
            tSUM_R = tR

        grid_a_b[i_idx, j_idx] = tSUM_R/10 # lub tSUM_R / 10
        #print(f"{tSUM_R}")
    print(f"postęp {i_idx+1}/{size2}")

plt.figure(figsize=(8, 6))
plt.imshow(grid_a_b, cmap='jet', origin='lower', extent=[0.01, 0.49, 0.01, 0.49])
plt.colorbar(label='Średnia liczba R po zakończeniu')
plt.xlabel('infection_prob')
plt.ylabel('recovery_prob')
plt.title('Wpływ parametrów infekcji i wyzdrowienia na liczbę R')
plt.grid(False)
plt.show()