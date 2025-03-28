import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


size = 50  # Rozmiar siatki
infection_prob = 0.1  # Prawdopodobieństwo zakażenia sąsiada
recovery_prob = 0.1   # Prawdopodobieństwo wyzdrowienia
steps = 200  # Liczba kroków symulacji

grid = np.zeros((size, size), dtype=int)

#t0
initial_infected = np.random.choice(range(size*size), size*size // 100, replace=False)
for id in initial_infected:
    grid[id // size, id % size] = 1


history = [grid.copy()]
for _ in range(steps - 1):
    new_grid = history[-1].copy()
    for i in range(size):
        for j in range(size):
            if history[-1][i, j] == 1:  # chory
                if np.random.rand() < recovery_prob:
                    new_grid[i, j] = 0  # Wyzdrowienie
                else:
                    # Próba zakażenia sąsiadów (góra, dół, lewo, prawo)
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size and history[-1][ni, nj] == 0:
                            if np.random.rand() < infection_prob:
                                new_grid[ni, nj] = 1
    history.append(new_grid.copy())

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
mat = ax.matshow(history[0], cmap='viridis')

# Suwak do wyboru momentu w czasie
ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03])
slider = Slider(ax_slider, 'Krok', 0, steps - 1, valinit=0, valfmt='%d')

def update(val):
    step = int(slider.val)
    mat.set_data(history[step])
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
