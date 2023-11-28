import math
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def objective_function(position):
    #Menghitung nilai fungsi objektif untuk suatu fungsi
    x = position[0]
    return x ** 2 - 10 * math.sin(2 * math.pi * x)

class Particle:
    def __init__(self, dimensi, initial_position):
        #Konstruktor kelas Particle untuk pembuatan partikel
        self.position = initial_position[:]
        #Membuat salinan independen dari posisi awal dan disetor ke position
        self.velocity = [0.0] * dimensi
        #Inisialisasi v awal partikel
        self.pbest = self.position[:]
        #Membuat salinan independen dari position untuk pbest awal
        self.pbest_value = objective_function(self.position)
        #pbest value awal dari partikel adalah obj func(position)

def update_velocity(particle, gbest, w, c1=2, c2=2):
    #Fungsi untuk mengupdadte kececpatan partikel.

    for i in range(len(particle.velocity)):
        cognitive = c1 * random.uniform(0, 1) * (particle.pbest[i] - particle.position[i])
        #Kecenderungan bergerak mengikuti pbest
        social = c2 * random.uniform(0, 1) * (gbest[i] - particle.position[i])
        #Kecenderungan bergerak mengikuti gbest
        old_velocity = particle.velocity[i]
        #Mengambil kecepatan sekarang
        new_velocity = w * old_velocity + cognitive + social
        #Kecepatan baru
        particle.velocity[i] = new_velocity
        #Update kecepatan partikel dengan kecepatan baru

def update_position(particle):
    #Fungsi untuk mengupdate posisi partikel.
    for i in range(len(particle.position)):
        new_position = particle.position[i] + particle.velocity[i]
        #Posisi baru = posisi partikel + kecepatan partikel
        particle.position[i] = max(-5.2, min(5.2, new_position))
        #Menerapkan batas posisi partikel untuk tetap berada pada rentang soal.

def generate_random_positions(dimensi, jumlah_posisi):
    #Fungsi untuk membuat angka random sebagai posisi awal partikel dengan batas (-5.2,5.2)
    return [[random.uniform(-5.2, 5.2) for _ in range(dimensi)] for _ in range(jumlah_posisi)]

def pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=None):
    #Algoritma Particle Swarm Optimization (PSO)
    particles = initial_particles or [Particle(dimensi, [0.0] * dimensi) for _ in range(jumlah_partikel)]
    """Jika initial particle tidak diinisialisasi (none), maka menjalankan list comprehension itu
    untuk membuat particle dengan nilai [0.0] tapi kalau tidak kosong ya ikuti isinya itu"""

    gbest = min(particles, key=lambda p: p.pbest_value).pbest[:]
    """gbest diambil dari nilai terkecil menggunakan fungsi (min) 
    dari atribut pbest_value terkecil dari tiap-tiap partikel
    lalu salin pbest[:]-nya tersebut menjadi nilai gbest"""

    table = PrettyTable()
    #Pembuatan Pretty Table dan Kolomnya apa saja
    table.field_names = ["Iterasi", "Posisi (x)", "f(x)", "pBest", "gBest", "v"]

    # List penyimpan data untuk visualisasi
    iteration_list = []
    position_list = []

    for iteration in range(jumlah_iterasi):
        iteration_list.append(iteration + 1)  #Tambahkan info ke list tadi
        current_positions = [particle.position[0] for particle in particles]
        position_list.append(current_positions) #Tambahkan info posisi ini ke list

        #Buat ngisi kolom
        fx_values = [objective_function(particle.position) for particle in particles]

        w = 0.9 - (iteration / jumlah_iterasi) * 0.4  # Menurunkan inertia weight tiap iterasi

        #Evaluasi fungsi objektif
        for particle in particles:
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

        for particle in particles: #Update dulu posisi partikelnya
            update_velocity(particle, gbest, w)

        row = [iteration + 1,
               [round(pos, 4) for pos in current_positions], #x
               [round(fx, 4) for fx in fx_values], #f(x)
               [round(pbest, 4) for pbest in [particle.pbest[0] for particle in particles]],#pbest
               [round(value, 4) for value in gbest], #gbest
               [round(velocity, 5) for velocity in [particle.velocity[0] for particle in particles]]#v
               ] #Menambahkan isi barisnya apa aja

        table.add_row(row) #barisnya ditambahin ke table


        for particle in particles: #Setelah itu update posisi
            update_position(particle)

    # Print table kalo udah selesai iterasinya
    print(table)

    #Plot Objective Function dan Posisi Partikel
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot objective function di kiri
    x_values = [i / 100 for i in range(-520, 521)] #Sumbu X
    y_values = [objective_function([x]) for x in x_values] #Sumbu Y
    ax1.plot(x_values, y_values, label='f(x)', color='blue')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')

    # Plot posisi partikel positions dikanan
    for i in range(jumlah_partikel):
        ax2.plot(iteration_list, [positions[i] for positions in position_list], label=f'Particle {i + 1}', marker='o')

    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Particle Position (x)')
    ax2.legend(loc='upper right')

    plt.suptitle('Objective Function and Particle Positions')
    plt.show()

    return gbest, objective_function(gbest)

if __name__ == "__main__":
    dimensi = 1 #Mau berapa dimensi ganti sesuai keinginan
    jumlah_partikel = 3 #Mau berapa partikel
    jumlah_iterasi = 300 #Mau berapa iterasi

    initial_positions = generate_random_positions(dimensi, 3) #Posisi awal partikel random
    #Bikin objek partikel terus di tampung ke particles
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]

    #hasil dan nilai optimum nanti keisi dengan gbest dan obj func (gbest) sesuai dengan apa yang di return def pso
    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: gBest={hasil}, f(x)={nilai_optimum}")
