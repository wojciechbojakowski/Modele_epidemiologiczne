import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

size = 50
number_patient0 = 75

def sim_SIR(infection_prop:float, recovery_prop:float):# 0=S, 1=I, 2=R
    grid = np.zeros((size, size), dtype=int)

    init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
    for id in init_infected:
        grid[id // size, id % size] = 1 

    grid2 = grid.copy()

    all_S=size*size-number_patient0
    all_I=number_patient0
    all_R=0
    iterator=0
    h_S, h_I, h_R = [], [], [] # tablice na liczbe osób w czasie
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5)) #dwa wykresy

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
        nonlocal all_I
        if (all_I==0 or frame >= 400):  # 400 frame ->END
            ani.event_source.stop()
            return
        nonlocal grid
        nonlocal all_R, all_S
        nonlocal h_S,h_I,h_R
        #global line_S,line_I,line_R

        new_grid = grid.copy()

        for i in range(size):
            for j in range(size):
                if grid[i, j] == 1:  # if I
                    if np.random.rand() < recovery_prop:
                        new_grid[i, j] = 2  #I->R
                        all_I-=1
                        all_R+=1
                elif grid[i, j] == 0:  # if S
                    infected_neighbors = 0
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = (i + di) % size, (j + dj) % size #modulo zawija w torus
                        if grid[ni, nj] == 1:
                            infected_neighbors += 1
                    
                    if np.random.rand() < (1 - (1 - infection_prop) ** infected_neighbors):
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

    ani = animation.FuncAnimation(fig, update, frames=400, interval=100, blit=False, repeat=False)
    name = "animation/animationSIR"+str(infection_prop)+"-"+str(recovery_prop)+".mp4"
    ani.save(filename=name, writer="ffmpeg")

    return [all_S, all_R]

def while_func(infection_prob:float,recovery_prob:float):
    grid = np.zeros((size, size), dtype=int)

    init_infected = np.random.choice(range(size*size), number_patient0, replace=False)
    for id in init_infected:
        grid[id // size, id % size] = 1 # 0=S, 1=I, 2=R

    grid2 = grid.copy()

    all_S=size*size-number_patient0
    all_I=number_patient0
    all_R=0
    iterator=0
    while(all_R<size*size and iterator<1000):
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
                            all_S=all_S-1
                            all_I=all_I+1
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
    return [all_S,all_R]

values = np.arange(0, 0.5, 0.1)
size2 = len(values)
grid_a_b = np.zeros((size2, size2), dtype=float)

for i_idx, i in enumerate(values):
    for j_idx, j in enumerate(values):
        tSUM_S = 0
        tSUM_R = 0

        for _ in range(1):
            tS, tR = while_func(i, j)
            tSUM_S += tS
            tSUM_R = tR

        grid_a_b[i_idx, j_idx] = tSUM_R  # lub tSUM_R / 10
        print(f"{tSUM_R}")
    print(f"postęp {i_idx+1}/{size2}")

plt.figure(figsize=(8, 6))
plt.imshow(grid_a_b, cmap='jet', origin='lower', extent=[0.01, 0.49, 0.01, 0.49])
plt.colorbar(label='Średnia liczba S po zakończeniu')
plt.xlabel('infection_prob')
plt.ylabel('recovery_prob')
plt.title('Wpływ parametrów infekcji i wyzdrowienia na liczbę R')
plt.grid(False)
plt.show()