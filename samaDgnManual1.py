import math
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def objective_function(position):
    x = position[0]
    return x ** 2 - 10 * math.sin(2 * math.pi * x)

class Particle:
    def __init__(self, dimensi, initial_position):
        self.position = initial_position[:]
        self.velocity = [0.0] * dimensi
        self.pbest = self.position[:]
        self.pbest_value = objective_function(self.position)

def update_velocity(particle, gbest, w=1.0, c1=0.5, c2=1):
    for i in range(len(particle.velocity)):
        cognitive = c1 * r1 * (particle.pbest[i] - particle.position[i])
        social = c2 * r2 * (gbest[i] - particle.position[i])
        old_velocity = particle.velocity[i]
        new_velocity = w * old_velocity + cognitive + social
        particle.velocity[i] = new_velocity

def update_position(particle):
    for i in range(len(particle.position)):
        new_position = particle.position[i] + particle.velocity[i]
        particle.position[i] = max(-5.2, min(5.2, new_position))

def pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=None):
    particles = initial_particles or [Particle(dimensi, [0.0] * dimensi) for _ in range(jumlah_partikel)]
    gbest = min(particles, key=lambda p: p.pbest_value).pbest[:]

    table = PrettyTable()
    table.field_names = ["Iterasi", "Posisi (x)", "f(x)", "pBest", "gBest", "v"]

    # Lists to store data for visualization
    iteration_list = []
    position_list = []
    fx_list = []

    for iteration in range(jumlah_iterasi):
        iteration_list.append(iteration + 1)
        current_positions = [particle.position[0] for particle in particles]
        position_list.append(current_positions)
        fx_values = [objective_function(particle.position) for particle in particles]
        fx_list.append(fx_values)

        for particle in particles:
            current_fitness = objective_function(particle.position)

            if current_fitness < particle.pbest_value:
                particle.pbest = particle.position[:]
                particle.pbest_value = current_fitness

            if current_fitness < objective_function(gbest):
                gbest = particle.position[:]

        for particle in particles:
            update_velocity(particle, gbest)

        row = [iteration + 1,
               [round(pos, 4) for pos in current_positions],
               [round(fx, 4) for fx in fx_values],
               [round(pbest, 4) for pbest in [particle.pbest[0] for particle in particles]],
               [round(value, 4) for value in gbest],
               [round(velocity, 5) for velocity in [particle.velocity[0] for particle in particles]]
               ]

        table.add_row(row)

        for particle in particles:
            update_position(particle)

    # Print the table
    print(table)

    # Plot objective function and particle positions in the same figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot objective function on the left subplot (ax1)
    x_values = [i / 100 for i in range(-520, 521)]
    y_values = [objective_function([x]) for x in x_values]
    ax1.plot(x_values, y_values, label='f(x)', color='blue')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')

    # Plot particle positions on the right subplot (ax2)
    for i in range(jumlah_partikel):
        ax2.plot(iteration_list, [positions[i] for positions in position_list], label=f'Particle {i + 1}', marker='o')

    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Particle Position (x)')
    ax2.legend(loc='upper right')

    plt.suptitle('Objective Function and Particle Positions')
    plt.show()

    return gbest, round(objective_function(gbest), 4)

if __name__ == "__main__":
    dimensi = 1
    jumlah_partikel = 3
    jumlah_iterasi = 3
    r1, r2 = 0.5, 0.5

    initial_positions = [[0.0],[0.5],[1.0]]
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: gBest={hasil}, f(x)={nilai_optimum}")
