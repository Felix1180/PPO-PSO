import math
from prettytable import  PrettyTable

def objective_function(position):
    x,y = position
    return math.sin(3 * math.pi * x)**2 + (x - 1)**2 * (1 + math.sin(3 * math.pi * y)**2) + (y - 1)**2 * (1 + math.sin(2 * math.pi * y)**2)

class Particle:
    def __init__(self, dimensi, initial_position):
        self.position = initial_position[:]
        self.velocity = [0.0] * dimensi
        self.pbest = self.position[:]
        self.pbest_value = objective_function(self.position)

def update_velocity(particle, gbest, w=1, c1=0.5, c2=1):
    # Fungsi untuk mengupdate kecepatan partikel.

    for i in range(len(particle.velocity)):
        r1, r2 = 0.5, 0.5
        cognitive = c1 * r1 * (particle.pbest[i] - particle.position[i])  # Kecenderungan bergerak mengikuti pbest
        social = c2 * r2 * (gbest[i] - particle.position[i])  # Kecenderungan bergerak mengikuti Gbest
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
    table.field_names = ["Iterasi", "Posisi (x,y)", "f(x,y)", "gBest", "pBest", "v"]

    for iteration in range(0, jumlah_iterasi):  # Melakukan iterasi

        # Pencetakan nilai pada setiap iterasi

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
            update_velocity(particle, gbest)

        rounded_gbest = [round(value, 4) for value in gbest]

        row = [iteration + 1,
               [(round(pos[0], 3), round(pos[1], 3)) for pos in [particle.position for particle in particles]],
               [round(objective_function(particle.position), 4) for particle in particles],
               (round(gbest[0], 3), round(gbest[1], 3)),
               [(round(pbest[0], 3), round(pbest[1], 3)) for pbest in [particle.pbest for particle in particles]],
               [(round(velocity[0], 5), round(velocity[1], 5)) for velocity in [particle.velocity for particle in particles]]
               ]

        table.add_row(row)

        for particle in particles:  # Tiap partikel diupdate posisinya pada tiap iterasi
            update_position(particle)


    """Jadi akhir dari fungsi ini akan memberikan kita
    gbest(posisi) dan juga nilainya jika dimasukkan kedalam 
    objective function"""
    print(table)
    return rounded_gbest, round(objective_function(gbest), 4)

if __name__ == "__main__":
    dimensi = 2
    jumlah_partikel = 3
    jumlah_iterasi = 3

    initial_positions = [[1.0, 1.0], [-2.0, -1.0], [2.0, 2.0]]
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: (x, y)={hasil}, f(x, y)={nilai_optimum}")