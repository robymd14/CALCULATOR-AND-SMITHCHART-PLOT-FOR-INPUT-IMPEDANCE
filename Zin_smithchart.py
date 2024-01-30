

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import plotly.graph_objects as go
import math

# Mendeklarasikan Zin sebagai variabel global
Zin = 0.0

# Dictionary untuk mapping satuan ke faktor konversi
unit_conversion = {
    'meter': 1,
    'kilometer': 1000,
    'centimeter': 0.01,
    'decimeter': 0.1,
    'millimeter': 0.001,
    'Hz': 1,
    'KHz': 1000,
    'MHz': 1000000,
    'GHz': 1000000000
}

def validate_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_to_base_unit(value, unit):
    return value * unit_conversion[unit]

def calculate_and_plot():
    # Mendapatkan nilai-nilai yang dibutuhkan (zl, zo, L, Frekuensi, Satuan L, Satuan f)
    zl_real = entry_zl_real.get()
    zl_imag = entry_zl_imag.get()

    zo = entry_zo.get()
    zo_imag = entry_zo_imag.get()

    L_value = entry_L.get()
    f_value = entry_f.get()

    # Validasi input
    inputs = [zl_real, zl_imag, zo, zo_imag, L_value, f_value]
    for value in inputs:
        if not validate_input(value):
            messagebox.showerror("Error", "Nilai yang diinput harus berupa angka !")
            return

    zl_real = float(zl_real)
    zl_imag = float(zl_imag)
    zo = float(zo)
    zo_imag = float(zo_imag)
    L_value = float(L_value)
    f_value = float(f_value)

    L_unit = combo_L_unit.get()
    f_unit = combo_f_unit.get()

    # Konversi nilai L dan f ke satuan dasar
    L_base = convert_to_base_unit(L_value, L_unit)
    f_base = convert_to_base_unit(f_value, f_unit)

    # Menghitung Impedansi input 
    zl = complex(zl_real, zl_imag)
    zo_z = complex(zo, zo_imag)

    c = 300000000  # kecepatan cahaya atau kecepatan gelombang (v)
    lamda = c / f_base
    pi_pembulatan = round(math.pi, 4)
    beta = (2 * pi_pembulatan) / lamda
    beta_L = beta * L_base
    global Zin  # Menggunakan variabel Zin yang dideklarasikan di luar fungsi
    Zin_not_normalisasi = ((zl + 1j * zo_z * math.tan(beta_L)) / (zo + zl * 1j * math.tan(beta_L)))
    Zin = 50 * ((zl + 1j * zo_z * math.tan(beta_L)) / (zo + zl * 1j * math.tan(beta_L)))

    # Menampilkan hasil di label
    label_Zin_not_normalisasi.config(text=f"Nilai impedansi input smithchart (Zin') (normalisasi): {Zin_not_normalisasi:.4f}", font=('inter', 10))
    label_Zin_normalisasi.config(text=f"Nilai Impedansi input (Zin) (denormalisasi): {Zin:.4f}", font=('inter', 10))

    # Menggambar Smith Chart
    draw_smith_chart(Zin_not_normalisasi)

    # Update GUI
    window.update_idletasks()

    # Kembalikan nilai Zin
    return Zin

def draw_smith_chart(Zin_not_normalisasi):
    global Zin  # Menggunakan variabel Zin yang dideklarasikan di luar fungsi

    # Membuat Smith Chart
    fig = go.Figure()

    fig.add_trace(go.Scattersmith(
        imag=[Zin_not_normalisasi.imag],
        real=[Zin_not_normalisasi.real],
        marker_symbol='circle',
        marker_size=20,
        marker_color="blue",
        text=f'Impedansi input (Zin): {Zin_not_normalisasi:.4f}',
        hoverinfo='text',
        name="Impedansi Input normalisasi (Zin')"  # Set the name of the trace
    ))

    # Menyesuaikan tampilan Smith Chart
    fig.update_layout(
        smith=dict(
            realaxis_gridcolor='purple',
            imaginaryaxis_gridcolor='green',
            domain=dict(x=[0.45, 1]),
        ),
        polar=dict(
            bgcolor="lightblue"
        )
    )

    # Menambahkan judul menggunakan annotation
    fig.update_layout(
        annotations=[
            dict(
                text="Plot Smith Chart Impedansi Input ",
                x=0.00,
                y=1,
                showarrow=False,
                font=dict(size=25),
            ),
            dict(
                text=f"Impedansi Input Smithchart (Zin') (normalisasi) = {Zin_not_normalisasi:.4f}",
                x=0.00,
                y=0.90,
                showarrow=False,
                font=dict(size=15),
            ),
            dict(
                text=f"Impedansi Input (Zin = Zin'x Zo) (denormalisasi)  = {Zin:.4f}",
                x=0.00,
                y=0.85,
                showarrow=False,
                font=dict(size=15),
            )
        ]
    )

    fig.update_smiths(bgcolor="lavender")
    # Menampilkan Smith Chart pada GUI
    fig.show()

# Membuat aplikasi GUI menggunakan Tkinter
window = tk.Tk()
window.title("Kalkulator Impedansi Input dan Plot Smith Chart")
window.configure(bg="lightblue") 

# Membuat label, entry, dan satuan untuk zl bagian real
label_zl_real = Label(window, text="Masukkan nilai Impedansi Beban (Zl) (Real):", font=('inter', 10), bg="lightblue")
label_zl_real.grid(row=0, column=0, padx=5, pady=5)
entry_zl_real = ttk.Entry(window)
entry_zl_real.grid(row=0, column=1, padx=5, pady=5)
label_satuanzl_real = Label(window, text="Ω", bg="lightblue", font=('inter', 10))
label_satuanzl_real.grid(row=0, column=2, padx=5, pady=5)

# Membuat label, entry, dan satuan untuk zl bagian imajiner
label_zl_imag = Label(window, text="Masukkan nilai Impedansi Beban (Zl) (Imaginer):", font=('inter', 10), bg="lightblue")
label_zl_imag.grid(row=1, column=0, padx=5, pady=5)
entry_zl_imag = ttk.Entry(window)
entry_zl_imag.grid(row=1, column=1, padx=5, pady=5)
label_satuanzl_imag = Label(window, text="Ω", bg="lightblue", font=('inter', 10))
label_satuanzl_imag.grid(row=1, column=2, padx=5, pady=5)

# Membuat label, entry, dan satuan untuk zo real
label_zo = Label(window, text="Masukkan nilai Impedansi Karakteristik Zo (Real):", font=('inter', 10), bg="lightblue")
label_zo.grid(row=2, column=0, padx=5, pady=5)
entry_zo = ttk.Entry(window)
entry_zo.grid(row=2, column=1, padx=5, pady=5)
label_satuanZo_real = Label(window, text="Ω", bg="lightblue", font=('inter', 10))
label_satuanZo_real.grid(row=2, column=2, padx=5, pady=5)

# Membuat label, entry, dan satuan untuk zo imajiner
label_zo_imag = Label(window, text="Masukkan nilai Impedansi Karakteristik Zo (Imaginer):", font=('inter', 10), bg="lightblue")
label_zo_imag.grid(row=3, column=0, padx=5, pady=5)
entry_zo_imag = ttk.Entry(window)
entry_zo_imag.grid(row=3, column=1, padx=5, pady=5)
label_satuanZo_imag = Label(window, text="Ω", bg="lightblue", font=('inter', 10))
label_satuanZo_imag.grid(row=3, column=2, padx=5, pady=5)

# Membuat label, entry, dan combobox satuan untuk Panjang gelombang (L)
label_L = Label(window, text="Masukkan nilai Panjang Kabel (L):", font=('inter', 10), bg="lightblue")
label_L.grid(row=4, column=0, padx=5, pady=5)
entry_L = ttk.Entry(window)
entry_L.grid(row=4, column=1, padx=5, pady=5)

combo_L_unit = ttk.Combobox(window, values=['meter', 'kilometer', 'centimeter', 'decimeter', 'milimeter'])
combo_L_unit.set('meter')  # Pilihan default
combo_L_unit.grid(row=4, column=2, padx=5, pady=5)

# Membuat label, entry, dan combobox satuan untuk frekuensi (f)
label_f = Label(window, text="Masukkan nilai Frekuensi (f):", font=('inter', 10), bg="lightblue")
label_f.grid(row=5, column=0, padx=5, pady=5)
entry_f = ttk.Entry(window)
entry_f.grid(row=5, column=1, padx=5, pady=5)

combo_f_unit = ttk.Combobox(window, values=['Hz', 'KHz', 'MHz', 'GHz'])
combo_f_unit.set('Hz')  # Pilihan default
combo_f_unit.grid(row=5, column=2, padx=5, pady=5)

# Tombol untuk menghitung dan menampilkan Smith Chart
calculate_button = Button(window, text="Hitung dan Tampilkan Smith Chart", command=calculate_and_plot, bg="#9999ff")
calculate_button.grid(row=7, column=0, columnspan=3, pady=10)

# Label untuk menampilkan hasil impedansi input normalisasi dan belum normalisasi
label_Zin_not_normalisasi = Label(window, text="Nilai Impedansi input smithchart (Zin') (normalisasi) ?", font=('inter', 10), bg="lightblue")
label_Zin_not_normalisasi.grid(row=9, column=0, columnspan=4)

label_Zin_normalisasi = Label(window, text="Nilai Impedansi input (Zin) (denormalisasi) ?", font=('inter', 10), bg="lightblue")
label_Zin_normalisasi.grid(row=10, column=0, columnspan=4)

window.mainloop()

