import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button


size = 50  # Rozmiar siatki
infection_prob = 0.15  # Prawdopodobieństwo zakażenia sąsiada
recovery_prob = 0.1  # Prawdopodobieństwo wyzdrowienia
number_patient0 = 10 #liczba chorych na początku

grid = np.zeros((size, size), dtype=int)

init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
for id in init_infected:
    grid[id // size, id % size] = 1 # 0=S, 1=I, 2=R

grid2 = grid.copy()

all_S=size*size-number_patient0
all_I=number_patient0
all_R=0
iterator=0

#pierwsza wersja bez animacji obecnie nie wykorzystywana
def while_func():
    while(all_R<size*size and iterator<10):
        for i in range(size):
            for j in range(size):
                if(iterator%2==0):#parzyste iteracje
                    if(grid[i,j]==1):#infected
                        if np.random.rand() < recovery_prob:
                            grid2[i, j] = 2  #Infected->R
                            all_I=all_I-1
                            all_R=all_R+1
                    elif(grid[i,j]==0):
                        acumulate_prop = 0
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:#dół, góra, lewo, prawo
                            ni, nj = i + di, j + dj
                            if(ni<0):# drabinka if do zawijania płaszczyzny w torus
                                ni=size-1
                            if(ni>size-1):
                                ni=0
                            if(nj<0):
                                nj=size-1
                            if(nj>size-1):
                                nj=0
                            if(grid[ni,nj]==1):
                                acumulate_prop=acumulate_prop+infection_prob#dodawanie do siebie prawdopodobieństwa zachorowania od sąsiadów
                        if np.random.rand() < acumulate_prop:
                            grid2[i, j] = 1#zachorowanie
                if(iterator%2==1):#parzyste iteracje
                    if(grid2[i,j]==1):#infected
                        if np.random.rand() < recovery_prob:
                            grid[i, j] = 2  #Infected->R
                            all_I=all_I-1
                            all_R=all_R+1
                    elif(grid2[i,j]==0):
                        acumulate_prop = 0
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:#dół, góra, lewo, prawo
                            ni, nj = i + di, j + dj
                            if(ni<0):# drabinka if do zawijania płaszczyzny w torus
                                ni=size-1
                            if(ni>size-1):
                                ni=0
                            if(nj<0):
                                nj=size-1
                            if(nj>size-1):
                                nj=0
                            if(grid2[ni,nj]==1):
                                acumulate_prop=acumulate_prop+infection_prob#dodawanie do siebie prawdopodobieństwa zachorowania od sąsiadów
                        if np.random.rand() < acumulate_prop:
                            grid[i, j] = 1#zachorowanie
                            all_S=all_S-1
                            all_I=all_I+1
        print(f"S {all_S}, I {all_I}, R {all_R}, sum {all_S+all_I+all_R}")
        iterator=iterator+1

h_S, h_I, h_R = [], [], [] # tablice na liczbe osób w czasie
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5)) #dwa wykresy
plt.subplots_adjust(left=0.1, bottom=0.25)  # więcej miejsca na suwaki i przycisk
# Suwaki
ax_slider_beta = plt.axes([0.1, 0.1, 0.3, 0.03])
ax_slider_gamma = plt.axes([0.1, 0.15, 0.3, 0.03])
slider_beta = Slider(ax_slider_beta, 'Infection Prob', 0.01, 1.0, valinit=infection_prob, valstep=0.01)
slider_gamma = Slider(ax_slider_gamma, 'Recovery Prob', 0.01, 1.0, valinit=recovery_prob, valstep=0.01)

# Przycisk
ax_button = plt.axes([0.6, 0.1, 0.1, 0.05])
start_button = Button(ax_button, 'Start')

def start_simulation(event):
    global grid, all_S, all_I, all_R, h_S, h_I, h_R, number_patient0, ani

    infection_prob = slider_beta.val
    recovery_prob = slider_gamma.val

    # Resetowanie stanu
    grid = np.zeros((size, size), dtype=int)
    init_infected = np.random.choice(range(size * size), number_patient0, replace=False)
    for id in init_infected:
        grid[id // size, id % size] = 1

    all_S = size * size - number_patient0
    all_I = number_patient0
    all_R = 0
    h_S.clear()
    h_I.clear()
    h_R.clear()

    # Odtworzenie animacji
    try:
        ani.event_source.stop()
    except NameError:
        pass
    ani = animation.FuncAnimation(fig, update, frames=400, interval=100, blit=False, repeat=False)
    plt.draw()

start_button.on_clicked(start_simulation)


#animacja w matplotlib
#fig, ax = plt.subplots()
cmap = plt.cm.jet
im = ax1.imshow(grid, cmap=cmap, vmin=0, vmax=2)

legend_text = ax1.text(2, 2, '', color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.5))
susceptible_patch = mpatches.Patch(color=cmap(0.0), label=" (S)")
infected_patch = mpatches.Patch(color=cmap(0.5), label=" (I)")
recovered_patch = mpatches.Patch(color=cmap(1.0), label=" (R)")
ax1.set_title("Symulacja SIR")

ax1.legend(handles=[susceptible_patch, infected_patch, recovered_patch], loc="upper right")

ax2.set_xlim(0, 200)  #(liczba iteracji)
ax2.set_ylim(0, size * size)  #(liczba osób)
ax2.set_title("Liczba osób w czasie")
ax2.set_xlabel("Iteracja")
ax2.set_ylabel("Liczba osób")

line_S, = ax2.plot([], [], label="S ", color='b')
line_I, = ax2.plot([], [], label="I ", color='g')
line_R, = ax2.plot([], [], label="R ", color='r')
ax2.legend()

def update(frame):
    global all_I
    if (all_I==0 or frame >= 400):  # 400 frame ->END
        ani.event_source.stop()
        return
    global grid
    global all_R, all_S
    global h_S,h_I,h_R
    #global line_S,line_I,line_R
    infection_prob = slider_beta.val
    recovery_prob = slider_gamma.val

    new_grid = grid.copy()

    for i in range(size):
        for j in range(size):
            if grid[i, j] == 1:  # if I
                if np.random.rand() < recovery_prob:
                    new_grid[i, j] = 2  #I->R
                    all_I-=1
                    all_R+=1
            elif grid[i, j] == 0:  # if S
                infected_neighbors = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = (i + di) % size, (j + dj) % size #modulo zawija w torus
                    if grid[ni, nj] == 1:
                        infected_neighbors += 1
                
                if np.random.rand() < (1 - (1 - infection_prob) ** infected_neighbors):
                    new_grid[i, j] = 1  # S->I
                    all_S-=1
                    all_I+=1
    
    #print(f"S {all_S}, I {all_I}, R {all_R}, sum {all_S+all_I+all_R}")
    h_S.append(all_S)
    h_I.append(all_I)
    h_R.append(all_R)
    line_S.set_data(range(len(h_S)), h_S)
    line_I.set_data(range(len(h_I)), h_I)
    line_R.set_data(range(len(h_R)), h_R)
    ax2.set_xlim(0, max(200, len(h_S) + 10))

    legend_text.set_text(f' S: {all_S} \n I: {all_I} \n R: {all_R} ')
    grid = new_grid
    im.set_array(grid)
    return [im, line_S, line_I, line_R]

def sir_model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Parametry zbieżne z parametrami symulacji
N = size * size
beta = infection_prob
gamma = recovery_prob

# Początkowe warunki
I0 = number_patient0 / N
S0 = 1 - I0
R0 = 0
y0 = [S0, I0, R0]

t = np.linspace(0, 400, 400)  # 400 kroków czasowych

solution = odeint(sir_model, y0, t, args=(beta, gamma))
S_diff, I_diff, R_diff = solution.T * N  # Skalowanie do liczby osób

line_S_diff, = ax2.plot(t, S_diff, 'b--', label='S (ODE)')
line_I_diff, = ax2.plot(t, I_diff, 'g--', label='I (ODE)')
line_R_diff, = ax2.plot(t, R_diff, 'r--', label='R (ODE)')


#ani = animation.FuncAnimation(fig, update, frames=400, interval=100, blit=False, repeat=False)
#ani.save("animation.mp4", writer="ffmpeg")
plt.show()