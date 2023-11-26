import math
import random
from prettytable import PrettyTable

def objective_function(position):
    x = position[0]
    return x**2 - 10 * math.sin(2*math.pi*x)

class Particle:
    def __init__(self, dimensi, initial_position):
        self.position = initial_position[:]
        self.velocity = [0.0] * dimensi
        self.pbest = self.position[:]
        self.pbest_value = objective_function(self.position)

def update_velocity(particle, gbest, w=1, c1=0.5, c2=1):
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

def generate_random_positions(dimensi, jumlah_posisi):
    return [[random.uniform(-5.2, 5.2) for _ in range(dimensi)] for _ in range(jumlah_posisi)]

def pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=None):
    particles = initial_particles or [Particle(dimensi, [0.0] * dimensi) for _ in range(jumlah_partikel)]
    gbest = min(particles, key=lambda p: p.pbest_value).pbest[:]

    table = PrettyTable()
    table.field_names = ["Iterasi", "Posisi (x)", "f(x)", "pBest", "gBest", "v"]

    for iteration in range(jumlah_iterasi):
        for particle in particles:
            current_fitness = objective_function(particle.position)

            if current_fitness < particle.pbest_value:
                particle.pbest = particle.position[:]
                particle.pbest_value = current_fitness

            if current_fitness < objective_function(gbest):
                gbest = particle.position[:]

        for particle in particles:
            update_velocity(particle, gbest)

        rounded_gbest = [round(value, 4) for value in gbest]

        row = [iteration + 1,
               [round(pos, 4) for pos in [particle.position[0] for particle in particles]],
               [round(objective_function(particle.position), 4) for particle in particles],
               [round(pbest, 4) for pbest in [particle.pbest[0] for particle in particles]],
               [round(value, 4) for value in gbest],
               [round(velocity, 5) for velocity in [particle.velocity[0] for particle in particles]]
               ]

        table.add_row(row)

        for particle in particles:
            update_position(particle)

    print(table)
    return rounded_gbest, round(objective_function(gbest),4)

if __name__ == "__main__":
    dimensi = 1
    jumlah_partikel = 3
    jumlah_iterasi = 5
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)

    initial_positions = generate_random_positions(dimensi, 3)
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: gBest={hasil}, f(x)={nilai_optimum}")
