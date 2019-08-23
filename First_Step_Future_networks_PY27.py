# -*- coding: utf-8 -*-

""" Adjusted to Python 2.7 """
import re
import Tkinter as tk
import ttk
import os

# Funkcja wykorzystywana przez GUI


def get_required_years_list():
    start_year = int(list_of_avail_years_start.get())
    stop_year = int(list_of_avail_years_stop.get())
    step = int(spin_step.get())

    if step == 0:

        required_years = sorted([str(start_year), str(stop_year)])

    else:
        if start_year == "":
            required_years = ["Ustaw rok początkowy"]
        elif stop_year == "":
            required_years = [year for year in range(start_year, min(max(list_of_years), start_year + 4 * step
                                                             + 1), step)]
        else:
            required_years = [year for year in range(start_year, stop_year + 1, step)]

    return required_years

# Funkcja wykorzystywana przez GUI


def update_preview():
    required_years_list = get_required_years_list()

    required_years_list_str = [str(year) for year in required_years_list]
    years_preview["text"] = ", ".join(required_years_list_str)

# Wyszukiwanie i pobieranie wśród atrybutów użytkownika dla odcinków tych oznaczających kategorię odcinka w danym roku


def retrive_all_years_from_ver():
    pattern = "(?:STAND_ROK_)(\d{4})"
    links_udas = Visum.Net.Links.Attributes
    years_in_ver_list = [int(re.findall(pattern, uda_year.Code)[0]) for uda_year in links_udas.GetAll
                            if re.match(pattern, uda_year.Code) != None]
    return years_in_ver_list


def generate_new_ver_file():

    # Zachowanie starej nazwy folderu VER z Project Directory i ustawienie biężącej ścieżki

    old_path = Visum.GetPath(2)  # 2 oznacza pliki VER

    Visum.SetPath(2, ".")  # Ustawienie jako folderu VER pliku gdzie znajduje się model
    # TODO sprawdzić gdzie to się zapisuje - poszło zgłoszenie na support

    base_ver_name = os.path.split(Visum.IO.CurrentVersionFile)[1]
    base_ver_name = base_ver_name.split(".")

    # Sprawdzenie i pobranie dostępnych lat znajdujących się już w modelu
    required_years = get_required_years_list()
    main_window.destroy()

    # Pobieranie informacji o roku
    for year in required_years:

        # Filtrowanie linków dla danego roku
        # uda_years_header - Nazwa atrybutu odcinka, która zawiera typ odcinka opowiązujący w danym roku

        uda_years_header = "STAND_ROK_" + str(year)

        # link_filter odpowiada za ustawienie filtra odcinków filtrującego odcinki, dla których następuje zmiana
        # kategorii w danym roku

        link_filter = Visum.Filters.LinkFilter()

        # Czyszczenie bieżącego filtra
        link_filter.Init()
        # Warunek pierwszy: typ odcinka w danym roku jest różny od obowiązującego typu odcinka
        link_filter.AddCondition("OP_NONE", False, uda_years_header, 12, "TYPENO", Position=-1)
        # Warunek drugi: typ odcinka w danym roku jest różny od 0
        link_filter.AddCondition("OP_AND", False, uda_years_header, 11, 0, Position=-1)
        # Warunek trzeci: parametr STAND_EDYTOWANY jest aktywny - oznacza to, że dane odcinki zostały
        # zmodyfikowane w tym etapie
        link_filter.AddCondition("OP_OR", False, "STAND_EDYTOWANY", 9, 1, Position=-1)  # 1 oznacza True
        # Założenie nawiasów na dwóch pierwszych warunkach
        link_filter.AddBrackets(1, 2)

        # Edycja kategorii odcinka

        # Obiekt zawierający wszystkie aktywne odcinki (odcinki spełniające warunki filtra)
        active_links = Visum.Net.Links.GetAllActive

        # Edycja każdego z odcinków, jeden po drugim
        for link in active_links:
            # Podczytanie nowego typu odcinka na podstawie UDA
            new_link_type = link.AttValue(uda_years_header)
            # Zmiana typu odcinka z wykorzystaniem nowego typu odcinka
            link.SetAttValue("TYPENO", int(new_link_type))
            # Zmiana parametru STAND_EDYTOWANY na True, jako że odcinek podległ edycji
            link.SetAttValue("STAND_EDYTOWANY", True)

        # Podczytanie parametrów domyślnych dla typu odcinka

        # TODO ustalić jakie parametry ostatecznie mają być podczytywane
        Visum.Net.Links.SetDefaultsFromLinkType(OnlyActive=True, Attributes=["CAPPRT", "V0PRT",
                                                                                "TSYSSET", "NUMLANES", "T_PUTSYS"])

        # Zapisanie pliku z nazwą rozszerzoną o rok

        Visum.SaveVersion(base_ver_name[0] + "_" + str(year) + "." + base_ver_name[1])

    Visum.SetPath(2, old_path)  # Przywrócenie wyjściowego ustawienia folderu plików VER


# GUI + główny skrypt

list_of_years = retrive_all_years_from_ver()

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