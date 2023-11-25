import math

def objective_function(position):
    # Menghitung nilai fungsi objektif untuk suatu posisi.

    x = position[0]
    return x**2 - 10 * math.sin(2*math.pi*x)

class Particle:
    def __init__(self, dimensi, initial_position):
        # Konstruktor kelas Particle untuk inisialisasi partikel.

        self.position = initial_position[:]  # Membuat salinan independen dari posisi awal dan disetor ke position
        self.velocity = [0.0] * dimensi  # Inisialisasi v awal ketika partikel dibuat
        self.pbest = self.position[:]  # Membuat salinan independen dari position
        self.pbest_value = objective_function(self.position)  # pbest_value adalah hasil dari obj func(posiiton)


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
        particle.position[i] += particle.velocity[i]

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

    for iteration in range(0, jumlah_iterasi):  # Melakukan iterasi

        # Pencetakan nilai pada setiap iterasi
        print(f"Iterasi {iteration+1}:\nx={[particle.position for particle in particles]}\n"
              f"f(x)={[objective_function(particle.position) for particle in particles]}")

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

        print(f"pbest={[particle.pbest for particle in particles]}")
        print(f"gbest={gbest}")

        for particle in particles:  # Tiap partikel diupdate kecepatan dan posisinya pada tiap iterasi
            update_velocity(particle, gbest)
            update_position(particle)

        print(f"v = {[particle.velocity for particle in particles]}\n")

    """Jadi akhir dari fungsi ini akan memberikan kita
    gbest(posisi) dan juga nilainya jika dimasukkan kedalam 
    objective function"""
    return gbest, objective_function(gbest)

if __name__ == "__main__":
    dimensi = 1  # Inisialiasi dimensi partikel
    jumlah_partikel = 3  # Banyaknya partikel
    jumlah_iterasi = 3  # Jumlah Iterasi

    initial_positions = [[0.0], [0.5], [1.0]]  # Inisialisasi posisi partikel
    particles = [Particle(dimensi, initial_position) for initial_position in initial_positions]
    # Membuat list particles berisi objek-objek Particle yang dihasilkan dari inisialisasi dengan posisi awal yang ada dalam initial_positions

    hasil, nilai_optimum = pso(dimensi, jumlah_partikel, jumlah_iterasi, initial_particles=particles)
    print(f"Hasil optimasi: gBest={hasil}, f(x)={nilai_optimum}")
    """Membuat 2 variable (hasil dan nilai optimum) yang nilainya didapat
    dari fungsi pso yang mengembalikan gbest dan nilai dari gbest
    jika dimasukkan kedalam objective functionnya
    Kemudian akan dicetak sebagai gbest dan juga nilai optimum"""