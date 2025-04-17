from scipy.signal import convolve2d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

size = 50
number_patient0=75

def step(grid, infection_prob, recovery_prob):
    kernel = np.array([[0, 1, 0],
                       [1, 0, 1],
                       [0, 1, 0]])
    
    infected_neighbors = convolve2d((grid == 1).astype(int), kernel, mode='same', boundary='wrap')
    
    # R
    recovery = (grid == 1) & (np.random.rand(*grid.shape) < recovery_prob)
    
    # I
    infection_chance = 1 - (1 - infection_prob) ** infected_neighbors
    new_infections = (grid == 0) & (np.random.rand(*grid.shape) < infection_chance)
    
    # Update
    grid[recovery] = 2
    grid[new_infections] = 1
    return grid

def simulate(infection_prob, recovery_prob, max_iter=1000):
    grid = np.zeros((size, size), dtype=int)
    init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
    grid[np.unravel_index(init_infected, (size, size))] = 1

    for _ in range(max_iter):
        if np.sum(grid == 1) == 0:
            break
        grid = step(grid, infection_prob, recovery_prob)
        #print(f"{np.sum(grid == 0)}, {np.sum(grid == 2)}, {infection_prob}, {recovery_prob}")

    return np.sum(grid == 0), np.sum(grid == 2)

values = np.arange(0.01, 0.5, 0.01)
size2 = len(values)
grid_a_b = np.zeros((size2, size2), dtype=float)

for i_idx, i in enumerate(values):
    for j_idx, j in enumerate(values):
        tSUM_S = 0
        tSUM_R = 0

        for _ in range(10):
            tS, tR = simulate(i, j)
            tSUM_S += tS
            tSUM_R += tR

        grid_a_b[i_idx, j_idx] = tSUM_S/10  # lub tSUM_R / 10
        #print(f"{tSUM_S}, {tSUM_R},{i}, {j}")
    print(f"postęp {i_idx+1}/{size2}")

plt.figure(figsize=(8, 6))
plt.imshow(grid_a_b, cmap='jet', origin='lower', extent=[0.01, 0.49, 0.01, 0.49])
plt.colorbar(label='Średnia liczba S po zakończeniu')
plt.ylabel('infection_prob')
plt.xlabel('recovery_prob')
plt.title('Wpływ parametrów infekcji i wyzdrowienia na liczbę S')
plt.grid(False)
plt.show()