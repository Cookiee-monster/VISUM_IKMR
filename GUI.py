import tkinter as tk
from tkinter import ttk

list_of_years = sorted([2019, 2020, 2021])


def get_required_years_list():

    start_year = int(list_of_avail_years_start.get())
    stop_year = int(list_of_avail_years_stop.get())
    step = int(spin_step.get())

    if step == 0:
        required_years = [str(start_year), str(stop_year)]
    else:
        if start_year == "":
            required_years = "Ustaw rok początkowy"
        elif stop_year == "":
            required_years = [year for year in range(start_year, min(max(list_of_years), start_year + 4 * step
                                                             + 1), step)]
        else:
            required_years = [year for year in range(start_year, stop_year + 1, step)]

    return required_years

def update_preview():
    required_years_list = get_required_years_list()

    required_years_list_str = [str(year) for year in required_years_list]
    years_preview["text"] = ", ".join(required_years_list_str)


def generate_new_ver_file():
    print("Powiedzmy, że działa")
    main_window.destroy()


main_window = tk.Tk()
main_window.geometry("450x210")
main_window.title("IKMR - Etap I - tworzenie przyszłych sieci")

label_start_year = tk.Label(main_window, text="Rok bazowy:").grid(row=0, column=0, padx=20, pady=20)
list_of_avail_years_start = ttk.Combobox(main_window, values=list_of_years)
list_of_avail_years_start.grid(row=0, column=2, padx=5, pady=20)

label_stop_year = tk.Label(main_window, text="Rok końcowy:").grid(row=1, column=0, padx=20)
list_of_avail_years_stop = ttk.Combobox(main_window, values=list_of_years)
list_of_avail_years_stop.grid(row=1, column=2, padx=5)

label_spin_step = tk.Label(main_window, text="Krok dla kolejnych lat:").grid(row=2, column=0, padx=50, pady=20)
spin_step = tk.Spinbox(main_window, from_ = 0, to = 10, width=5)
spin_step.grid(row=2, column=2, padx=10, pady=20)

label_years_preview = tk.Label(main_window, text="Wybrane lata").grid(row=3, column=0)
years_preview = tk.Message(main_window, width=200, text="")
years_preview.grid(row=3, column=2)

button_preview = tk.Button(main_window, text="Podgląd lat", command=update_preview).grid(row=4, column=0, pady=5)
button_execute = tk.Button(main_window, text="OK", command=generate_new_ver_file).grid(row=4, column=1, pady=5)
button_cancel = tk.Button(main_window, text="Anuluj", command=main_window.destroy).grid(row=4, column=2, pady=5)

main_window.mainloop()
