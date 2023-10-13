import sqlite3
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from users import (
    delete_entry_from_db,
    save_entry_into_db,
    select_user,
    select_all,
)
from users import User

from gui import SmartHomeApp
from weather import Weather
from lights import Light

# from thermostat import Thermostat

if __name__ == "__main__":
    app = SmartHomeApp()

    widgets_to_destroy = []

    ############################
    #######    WEATHER    ######
    ############################

    def open_weather():
        global widgets_to_destroy
        for widget in widgets_to_destroy:
            widget.destroy()
        widgets_to_destroy = []

        weather = Weather()
        Weather_label = tk.Label(
            app, text=f"Weather forcast on hourly base", anchor="center"
        )
        Weather_label.place(x=260, y=20)

        putanja = "photos/temperature.png"
        fotografija = Image.open(putanja)
        photo = ImageTk.PhotoImage(fotografija)
        image_label1 = tk.Label(app, image=photo)
        image_label1.place(x=200, y=200)
        current_temperature_label = tk.Label(
            app, text=f"Current Temperature: {weather.current_temperature}", anchor="w"
        )
        current_temperature_label.place(x=170, y=330)
        # print(f"Current Temperature: {weather.current_temperature}")
        image_label1.photo = photo

        putanja = "photos/sunrise.png"
        fotografija = Image.open(putanja)
        photo = ImageTk.PhotoImage(fotografija)
        image_label2 = tk.Label(app, image=photo)
        image_label2.place(x=400, y=200)
        sunrise_time_label = tk.Label(
            app, text=f"Sunrise Time: {weather.sunrise_time}", anchor="center"
        )
        sunrise_time_label.place(x=380, y=330)
        # print(f"Sunrise Time: {weather.sunrise_time}")
        image_label2.photo = photo

        putanja = "photos/sunset.png"
        fotografija = Image.open(putanja)
        photo = ImageTk.PhotoImage(fotografija)
        image_label3 = tk.Label(app, image=photo)
        image_label3.place(x=200, y=410)
        sunset_time_label = tk.Label(
            app, text=f"Sunset Time: {weather.sunset_time}", anchor="center"
        )
        sunset_time_label.place(x=180, y=540)
        # print(f"Sunset Time: {weather.sunset_time}")
        image_label3.photo = photo

        putanja = "photos/overcast.png"
        fotografija = Image.open(putanja)
        photo = ImageTk.PhotoImage(fotografija)
        image_label4 = tk.Label(app, image=photo)
        image_label4.place(x=400, y=410)
        overcast_label = tk.Label(
            app, text=f"Overcast: {weather.overcast}", anchor="center"
        )
        overcast_label.place(x=410, y=540)
        image_label4.photo = photo

        exit = tk.Button(app, text="Exit", command=menu)
        exit.place(x=610, y=550, width=50, height=40)

        widgets_to_destroy.extend(
            [
                Weather_label,
                image_label1,
                image_label2,
                image_label3,
                image_label4,
                current_temperature_label,
                sunrise_time_label,
                sunset_time_label,
                overcast_label,
                exit,
            ]
        )

    ############################
    #######    LIGHTS    #######
    ############################

    svjetla = ["Svjetlo1", "Svjetlo2"]
    svjetlo_indi = {}

    for svjetlo in svjetla:
        svjetlo_obj = Light(svjetlo)
        svjetlo_indi[svjetlo] = {}
        svjetlo_indi[svjetlo]["light_obj"] = svjetlo_obj
        svjetlo_indi[svjetlo]["var_auto"] = tk.BooleanVar()
        svjetlo_indi[svjetlo]["var_ovc"] = tk.BooleanVar()

    def set_auto_vars():
        global svjetlo_indi

        for svjetlo in svjetlo_indi.values():
            svjetlo["var_auto"].set(svjetlo["light_obj"].auto)
            svjetlo["var_ovc"].set(svjetlo["light_obj"].ovc)

    running = True

    def return_to_menu():
        global running
        running = False
        menu()

    def indikator_bg():
        global svjetlo_indi
        global running
        if running:
            for svjetlo in svjetlo_indi.values():
                if svjetlo["light_obj"].on_off:
                    svjetlo["indikator"].config(bg="#FFD600")
                else:
                    svjetlo["indikator"].config(bg="#212121")
            app.after(1000, indikator_bg)

    def btn_on_off(light):
        global svjetlo_indi
        light.turn_on_off()
        set_auto_vars()
        open_lights_control()
        # for svjetlo in svjetlo_indi.values():
        #         svjetlo["btns"][0].invoke()
        #         svjetlo["btns"][1].invoke()

    def open_lights_control():
        global widgets_to_destroy
        for widget in widgets_to_destroy:
            widget.destroy()
        # widgets_to_destroy = []

        global svjetla
        global svjetlo_indi
        global running
        running = True
        set_auto_vars()  # Setting values svjetlo_indi[svjetlo]["var_ovc"] svjetlo_indi[svjetlo]["var_auto"]

        i = 0
        for svjetlo in svjetlo_indi.keys():
            svjetlo_obj = svjetlo_indi[svjetlo]["light_obj"]

            label = tk.Label(app, text=svjetlo, font=("Arial Bold", 16))
            label.place(relx=0.05, rely=0.2 + i * 0.1, anchor="sw")

            indikator = tk.Label(app, relief=SOLID)
            indikator.place(
                relx=0.35, rely=0.2 + i * 0.1, width=40, height=40, anchor="sw"
            )

            svjetlo_indi[svjetlo]["indikator"] = indikator

            ch_box_auto_time = tk.Checkbutton(
                app,
                text="Automatic",
                variable=svjetlo_indi[svjetlo]["var_auto"],
                command=svjetlo_obj.set_auto,
            )
            ch_box_auto_time.place(relx=0.5, rely=0.2 + i * 0.1, anchor="sw")
            ch_box_auto_ovc = tk.Checkbutton(
                app,
                text="Overcast Auto",
                variable=svjetlo_indi[svjetlo]["var_ovc"],
                command=svjetlo_obj.overcast_f_on_off,
            )
            ch_box_auto_ovc.place(relx=0.75, rely=0.2 + i * 0.1, anchor="sw")
            svjetlo_indi[svjetlo]["btns"] = [ch_box_auto_time, ch_box_auto_ovc]

            on_off_button = tk.Button(
                app, text="On/Off", command=lambda light=svjetlo_obj: btn_on_off(light)
            )
            on_off_button.place(relx=0.8, rely=0.2 + i * 0.1)

            widgets_to_destroy.extend(
                [label, indikator, ch_box_auto_time, ch_box_auto_ovc, on_off_button]
            )
            i += 1

        indikator_bg()  # ovo treba palit samo kad stisnem na ch button, staviti f-ju koja mjenja u klasi i pali ovo
        exit_button = tk.Button(app, text="Back", command=return_to_menu)
        exit_button.place(x=50, y=50)
        widgets_to_destroy.append(exit_button)

    ###############################
    # TEMPERATURE CONTROL #
    ###############################

    def open_temp_control():
        pass

    ###############################
    # MAIN MENU #
    ###############################

    def menu():
        global widgets_to_destroy
        for widget in widgets_to_destroy:
            widget.destroy()
        # widgets_to_destroy = []

        buttons = {
            "open_lights_control": "Lights",
            "open_temp_control": "Temperature",
            "open_weather": "Weather",
        }
        i = 0
        for command, text in buttons.items():
            button = tk.Button(
                app, text=text, command=lambda command=command: globals()[command]()
            )
            button.place(x=(190 + i * 105), y=300, width=100, height=100)
            i += 1
            widgets_to_destroy.append(button)
        button = tk.Button(app, text="ADMIN", command=open_admin)
        button.place(x=100, y=50, width=100, height=50)
        widgets_to_destroy.append(button)

    ############################
    ####### ADMIN PANEL   ######                       TODO poravnanja namjestiti jos
    ############################

    list_of_users_from_db = tk.Variable()
    user_in_editig = User
    user_name = tk.StringVar()
    user_surname = tk.StringVar()
    user_pin = tk.IntVar()
    user_active = tk.IntVar()
    list_of_users = tk.Listbox()
    users = []

    entry_vars = [user_name, user_surname, user_pin, user_active]

    def users_list_update():
        global users
        if users == []:
            users = select_all()
        user_names = ["Lista svih korisnika"]
        for user in users:
            user_names.append(f"{user}")
        list_of_users_from_db.set(value=user_names)

    def save_entry():
        global user_in_editig
        global users

        user = (user_pin.get(), user_name.get(), user_surname.get(), user_active.get())
        if user_in_editig in users:
            user = tuple(list(user) + [user_in_editig.id])
            users.remove(user_in_editig)
            user_in_editig = User(user)
            save_entry_into_db(user)

        else:
            save_entry_into_db(user)
            user = tuple(list(user) + [len(users)])
            user_in_editig = User(user)

        users.append(user_in_editig)
        users_list_update()

    def cancel_entry():
        global user_in_editig
        user_in_editig = User
        user_name.set("")
        user_surname.set("")
        user_pin.set("")
        user_active.set(1)

    def delete_entry():
        global user_in_editig
        delete_entry_from_db(user_in_editig.pin)
        users.remove(user_in_editig)
        users_list_update()

    def list_of_users_select(event):
        global user_in_editig
        global entry_vars
        selected = list_of_users.curselection()
        print(selected)
        if len(selected) == 0:
            pass
        else:
            selected_user = (list_of_users.get(selected)).split(" ")

            for user in users:
                if selected_user == [user.name, user.surname]:
                    user_in_editig = user
                    user_name.set(user.name)
                    user_surname.set(user.surname)
                    user_pin.set(user.pin)
                    user_active.set(user.active)

    def open_admin():
        global widgets_to_destroy
        for widget in widgets_to_destroy:
            widget.destroy()
        widgets_to_destroy = []

        users_list_update()
        admin_panel_frame = tk.LabelFrame(
            app,
            text="Upravljanje dodijeljenim ključevima",
            borderwidth=1,
            relief="solid",
        )
        admin_panel_frame.place(x=350, y=300, anchor="center", width=560, height=250)

        list_of_users = tk.Listbox(
            admin_panel_frame,
            listvariable=list_of_users_from_db,
            width=30,
            selectmode=tk.SINGLE,
        )
        list_of_users.place(x=15, y=10, width=250, height=220)
        list_of_users.bind("<<ListboxSelect>>", list_of_users_select)

        # Frame gdje se nalaze tk.Entry sa informacijama korisnika

        user_edit_frame = tk.Frame(admin_panel_frame)
        user_edit_frame.place(x=280, y=10, width=260, height=220)

        person = ["Ime", "Prezime", "PIN (4 broja)", "Aktivan"]

        # Labels iz liste person
        row_num_info = 0
        for info in person:
            label = tk.Label(user_edit_frame, text=info, font=("Manrope", 12))
            label.place(relx=0.1, rely=0.1 + row_num_info * 0.2, anchor="e")
            row_num_info += 1

        row_num_info = 0

        global entry_vars

        # ovo pravi kućice za izmjenu podataka
        for entry_var in entry_vars:
            if entry_var == user_active:
                entry = tk.Checkbutton(user_edit_frame, variable=entry_var)
                entry.place(relx=0.4, rely=0.1 + row_num_info * 0.2, anchor="e")
            else:
                entry = tk.Entry(
                    user_edit_frame, textvariable=entry_var, font=("Manrope", 12)
                )
                entry.place(relx=0.4, rely=0.1 + row_num_info * 0.2, anchor="e")
            row_num_info += 1

        buttons_options = {
            save_entry: "Spremi",
            cancel_entry: "Odustani",
            delete_entry: "Izbriši",
        }
        # Gumbovi
        col_num = 0
        for button_f, button_option in buttons_options.items():
            button = tk.Button(
                user_edit_frame, text=button_option, command=button_f, width=10
            )
            button.place(relx=0.1 + col_num * 0.25, rely=0.9, anchor="e")
            col_num += 1

        exit_button = tk.Button(app, text="Back", command=menu)
        exit_button.place(x=50, y=50)

        widgets_to_destroy.extend([admin_panel_frame, exit_button])

    ######################
    ##### ENTER PIN  #####              R J E Š E N O
    ######################

    pin_digits = []
    current_digit = 0
    pin = ""

    def button_pin_press(n):
        global pin
        global current_digit
        if current_digit < 4:
            pin_digits[current_digit].config(text="*")
            current_digit += 1
        pin += n

    def delete():
        global pin
        global current_digit
        for i in range(4):
            pin_digits[i].config(text="")
        pin = ""
        current_digit = 0

    def pin_panel():
        global widgets_to_destroy
        for widget in widgets_to_destroy:
            widget.destroy()
        widgets_to_destroy = []

        for i in range(4):
            pin_digit = tk.Label(
                app,
                text="",
                width=2,
                height=1,
                relief="ridge",
                font=("Manrope", 12),
            )
            pin_digit.place(x=(260 + 45 * i), y=380, width=40, height=40)
            pin_digits.append(pin_digit)
            widgets_to_destroy.append(pin_digit)

        buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "<", "0"]

        x = y = 0

        for button_text in buttons:
            if button_text == "<":
                button = tk.Button(
                    app, text=button_text, command=delete, font=("Manrope", 12)
                )
            else:
                button = tk.Button(
                    app,
                    text=button_text,
                    font=("Manrope", 12),
                    command=lambda btn=button_text: button_pin_press(btn),
                )
            button.place(x=(285 + x * 45), y=(180 + y * 45), width=40, height=40)
            x += 1
            if x > 2:
                x = 0
                y += 1

            widgets_to_destroy.append(button)

        login_btn = tk.Button(
            app, text="Log In", font=("Manrope", 12), command=login_check
        )
        login_btn.place(relx=0.5, rely=0.8, anchor="center", width=100, height=45)
        widgets_to_destroy.append(login_btn)

    ####################
    #####  LOGIN  ######            R J E Š E N O
    ####################

    def login_check():
        global pin

        if len(pin) == 4:
            pin = int(pin)
            user = select_user(pin)
            print(user.pin)
            if user.active == 1:
                menu()
            else:
                messagebox.showinfo(
                    "Obavijest",
                    "Niste Aktivan korisnik, zatražite aktivaciju od ADMINA",
                )
        else:
            messagebox.showinfo("Obavijest", "Neispravan PIN")

    def open_login():
        login.destroy()
        pin_panel()

    login = tk.Button(app, text="Login", command=open_login)
    login.place(x=310, y=430, width=100, height=135)
    widgets_to_destroy.append(login)

    app.mainloop()
