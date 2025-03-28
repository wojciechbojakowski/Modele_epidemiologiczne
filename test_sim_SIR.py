import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

size = 100  # Rozmiar siatki
infection_prob = 0.2  # Prawdopodobieństwo zakażenia sąsiada
recovery_prob = 0.02  # Prawdopodobieństwo wyzdrowienia
number_patient0 = 50  # liczba początkowych chorych

# Tworzenie siatki
grid = np.zeros((size, size), dtype=int)
init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
for id in init_infected:
    grid[id // size, id % size] = 1  # 0=S, 1=I, 2=R

# Konfiguracja wykresu
fig, ax = plt.subplots()
cmap = plt.cm.jet
im = ax.imshow(grid, cmap=cmap, vmin=0, vmax=2)

def update(frame):
    global grid
    new_grid = grid.copy()

    for i in range(size):
        for j in range(size):
            if grid[i, j] == 1:  # Jeśli zakażony
                if np.random.rand() < recovery_prob:
                    new_grid[i, j] = 2  # Wyzdrowienie
            elif grid[i, j] == 0:  # Jeśli podatny na infekcję
                # Sprawdzenie sąsiadów (zawijanie toroidalne)
                infected_neighbors = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ni, nj = (i + di) % size, (j + dj) % size
                    if grid[ni, nj] == 1:
                        infected_neighbors += 1
                
                if np.random.rand() < (1 - (1 - infection_prob) ** infected_neighbors):
                    new_grid[i, j] = 1  # Zakażenie

    grid = new_grid
    im.set_array(grid)  # Aktualizacja obrazu
    return [im]

# Tworzenie animacji
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=False)
plt.show()
