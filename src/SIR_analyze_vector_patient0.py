from scipy.signal import convolve2d
import numpy as np
import matplotlib.pyplot as plt

size = 50
patient0_values = [1, 5, 10, 25, 50, 75, 100, 200]  # różne liczby pacjentów 0

def step(grid, infection_prob, recovery_prob):
    kernel = np.array([[0, 1, 0],
                       [1, 0, 1],
                       [0, 1, 0]])
    
    infected_neighbors = convolve2d((grid == 1).astype(int), kernel, mode='same', boundary='wrap')
    
    recovery = (grid == 1) & (np.random.rand(*grid.shape) < recovery_prob)
    infection_chance = 1 - (1 - infection_prob) ** infected_neighbors
    new_infections = (grid == 0) & (np.random.rand(*grid.shape) < infection_chance)
    
    grid[recovery] = 2
    grid[new_infections] = 1
    return grid

def simulate(infection_prob, recovery_prob, number_patient0, max_iter=1000):
    grid = np.zeros((size, size), dtype=int)
    init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
    grid[np.unravel_index(init_infected, (size, size))] = 1

    for _ in range(max_iter):
        if np.sum(grid == 1) == 0:
            break
        grid = step(grid, infection_prob, recovery_prob)
    return np.sum(grid == 0), np.sum(grid == 2)

# Parametry
values = np.arange(0.01, 0.5, 0.03)
size2 = len(values)
num_patient_configs = len(patient0_values)
results = np.zeros((num_patient_configs, size2, size2), dtype=float)

for p_idx, patient0 in enumerate(patient0_values):
    print(f"Symulacja dla {patient0} pacjentów 0")
    for i_idx, i in enumerate(values):
        for j_idx, j in enumerate(values):
            tSUM_S = 0
            for _ in range(10):
                tS, _ = simulate(i, j, patient0)
                tSUM_S += tS
            results[p_idx, i_idx, j_idx] = tSUM_S / 10
        print(f"  Postęp: {i_idx + 1}/{size2}")

# Wizualizacja
fig, axes = plt.subplots(2, (len(patient0_values) + 1) // 2, figsize=(15, 10), constrained_layout=True)

for idx, patient0 in enumerate(patient0_values):
    ax = axes[idx // ((len(patient0_values) + 1) // 2)][idx % ((len(patient0_values) + 1) // 2)]
    im = ax.imshow(results[idx], cmap='jet', origin='lower', extent=[0.01, 0.49, 0.01, 0.49])
    ax.set_title(f'{patient0} pacjentów 0')
    ax.set_xlabel('recovery_prob')
    ax.set_ylabel('infection_prob')

fig.colorbar(im, ax=axes, shrink=0.6, location='right', label='Średnia liczba S po zakończeniu')
plt.suptitle('Wpływ liczby pacjentów 0 i parametrów infekcji/wyzdrowienia na liczbę S', fontsize=16)
plt.show()
