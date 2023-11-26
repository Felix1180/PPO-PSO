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
    # Fungsi untuk mengupdate kecepatan partikel.

    for i in range(len(particle.velocity)):
        cognitive = c1 * random.uniform(0, 1) * (particle.pbest[i] - particle.position[i])  # Kecenderungan bergerak mengikuti pbest
        social = c2 * random.uniform(0, 1) * (gbest[i] - particle.position[i])  # Kecenderungan bergerak mengikuti Gbest
        # Simpan nilai v sebelum diperbarui
        old_velocity = particle.velocity[i]
        new_velocity = w * old_velocity + cognitive + social  # Update Kecepatan
        particle.velocity[i] = new_velocity  # Nilainya disetor ke atribut kecepatan suatu partikel

def update_position(particle):
    # Fungsi untuk mengupdate posisi partikel.

    for i in range(len(particle.position)):
        new_position = particle.position[i] + particle.velocity[i]
        # Pastikan nilai posisi berada dalam rentang [-10, 10]
        particle.position[i] = max(-10, min(10, new_position))

def generate_random_positions(dimensi, jumlah_posisi):
    # Fungsi untuk menghasilkan bilangan acak dalam rentang [-10, 10]
    return [[random.uniform(-10, 10) for _ in range(dimensi)] for _ in range(jumlah_posisi)]

def pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=None):
    # Algoritma Particle Swarm Optimization (PSO).
    particles = initial_particles or [Particle(dimensi, [0.0] * dimensi) for _ in range(jumlah_partikel)]
    """Jika initial particle tidak diinisialisasi
    (None) maka menjalankan list comprehension 
    (membuat particles dengan nilai [0.0])"""
    gbest = min(particles, key=lambda p: p.pbest_value).pbest[:]
    """gbest diambil dari nilai terkecil menggunakan fungsi (min) 
    dari atribut pbest_value terkecil dari tiap-tiap partikel
    lalu salin pbest[:]-nya tersebut menjadi nilai gbest"""

    table = PrettyTable()
    table.field_names = ["Iterasi", "Posisi (x,y)", "f(x,y)", "pBest", "gBest", "v"]

    iteration_list = []
    position_list = []

    for iteration in range(jumlah_iterasi):  # Melakukan iterasi
        iteration_list.append(iteration + 1)
        current_positions = [(particle.position[0], particle.position[1]) for particle in particles]
        position_list.append(current_positions)
        fx_values = [objective_function(particle.position) for particle in particles]

        w = 0.9 - (iteration / jumlah_iterasi) * 0.4  # Menurunkan inertia weight tiap iterasi

        for particle in particles:  # Tiap partikel juga akan di cek nilainya terkait fungsi objektif
            current_fitness = objective_function(particle.position)

            """Jika fitness sekarang lebih kecil dari nilai pbest,
            maka pbest dari partikel adalah posisi partikel sekarang 
            dan valuenya adalah fitness terkini"""
            if current_fitness < particle.pbest_value:
                particle.pbest = particle.position[:]
                particle.pbest_value = current_fitness

            """Kemudian jika current fitness juga lebih kecil
            dari pada nilai objektif function dari gbest
            maka si gbest nya diubah menjadi posisi partikel itu"""
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
               [(round(velocity[0], 5), round(velocity[1], 5)) for velocity in
                [particle.velocity for particle in particles]]
               ]

        table.add_row(row)

        for particle in particles:
            update_position(particle)

    """Jadi akhir dari fungsi ini akan memberikan kita
    gbest(posisi) dan juga nilainya jika dimasukkan kedalam 
    objective function"""
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
    jumlah_iterasi = 100

    initial_positions = generate_random_positions(dimensi, 3)  # Generate 3 posisi acak dalam dimensi 2
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: (x, y)={hasil}, f(x, y)={nilai_optimum}")