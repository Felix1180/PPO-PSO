import math
import random
from matplotlib import pyplot as plt
from prettytable import PrettyTable

def objective_function(position):
    x,y = position
    return math.sin(3 * math.pi * x)**2 + (x - 1)**2 * (1 + math.sin(3 * math.pi * y)**2) + (y - 1)**2 * (1 + math.sin(2 * math.pi * y)**2)

class Particle:
    def __init__(self, dimensi, initial_position):
        self.position = initial_position[:]
        self.velocity = [0.0] * dimensi
        self.pbest = self.position[:]
        self.pbest_value = objective_function(self.position)

def update_velocity(particle, gbest, w, c1=2, c2=2):
    for i in range(len(particle.velocity)):
        cognitive = c1 * random.uniform(0, 1) * (particle.pbest[i] - particle.position[i])
        social = c2 * random.uniform(0, 1) * (gbest[i] - particle.position[i])
        old_velocity = particle.velocity[i]
        new_velocity = w * old_velocity + cognitive + social
        particle.velocity[i] = new_velocity

def update_position(particle):

    for i in range(len(particle.position)):
        new_position = particle.position[i] + particle.velocity[i]
        particle.position[i] = max(-10, min(10, new_position))

def generate_random_positions(dimensi, jumlah_posisi):

    return [[random.uniform(-10, 10) for _ in range(dimensi)] for _ in range(jumlah_posisi)]

def pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=None):
    particles = initial_particles or [Particle(dimensi, [0.0] * dimensi) for _ in range(jumlah_partikel)]
    gbest = min(particles, key=lambda p: p.pbest_value).pbest[:]

    table = PrettyTable()
    table.field_names = ["Iterasi", "Posisi (x,y)", "f(x,y)", "pBest", "gBest", "v"]

    iteration_list = []
    position_list = []

    for iteration in range(jumlah_iterasi):
        iteration_list.append(iteration + 1)
        current_positions = [(particle.position[0], particle.position[1]) for particle in particles]
        position_list.append(current_positions)
        fx_values = [objective_function(particle.position) for particle in particles]

        w = 0.9 - (iteration / jumlah_iterasi) * 0.4

        for particle in particles:
            current_fitness = objective_function(particle.position)

            if current_fitness < particle.pbest_value:
                particle.pbest = particle.position[:]
                particle.pbest_value = current_fitness

            if current_fitness < objective_function(gbest):
                gbest = particle.position[:]

        for particle in particles:
            update_velocity(particle, gbest, w)

        rounded_gbest = [round(value, 4) for value in gbest]

        row = [iteration + 1,
               [(round(pos[0], 4), round(pos[1], 4)) for pos in current_positions],
               [round(fx, 4) for fx in fx_values],
               [(round(pbest[0], 4), round(pbest[1], 4)) for pbest in [particle.pbest for particle in particles]],
               (round(gbest[0], 3), round(gbest[1], 3)),
               [(round(velocity[0], 5), round(velocity[1], 5)) for velocity in [particle.velocity for particle in particles]]
               ]

        table.add_row(row)

        for particle in particles:
            update_position(particle)

    print(table)

    # Plot objective function
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    x_values = [i / 100 for i in range(-1000, 1001)]
    y_values = [objective_function([x, gbest[1]]) for x in x_values]
    ax1.plot(x_values, y_values, label='f(x, y)', color='blue')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x, y)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')

    # Plot particle positions
    for i in range(jumlah_partikel):
        ax2.plot(iteration_list, [positions[i][0] for positions in position_list], label=f'Particle {i + 1} (x)',
                 marker='o')
        ax2.plot(iteration_list, [positions[i][1] for positions in position_list], label=f'Particle {i + 1} (y)',
                 marker='x')

    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Particle Position')
    ax2.legend(loc='upper right')

    plt.suptitle('Objective Function and Particle Positions')
    plt.show()

    return rounded_gbest, round(objective_function(gbest), 4)

if __name__ == "__main__":
    dimensi = 2
    jumlah_partikel = 3
    jumlah_iterasi = 300

    initial_positions = generate_random_positions(dimensi, 3)
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: (x, y)={hasil}, f(x, y)={nilai_optimum}")