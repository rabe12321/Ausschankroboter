# %% Imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import gui_elements as gui
from threading import Thread
import time
import sys

from filepath import FILEPATH

# %% -----------------Farben definieren--------------------------------------------------------------------------------#
# col_Blue = '#%02x%02x%02x' % (1, 105, 196)  # RGB values
col_Blue = '#%02x%02x%02x' % (18, 123, 202)  # RGB values TEC blue
col_Grey = '#%02x%02x%02x' % (200, 200, 200)  # RGB values
col_GlobalBackground = '#%02x%02x%02x' % (200, 200, 200)  # RGB light grey

# %% -----------------Hauptfenster erstellen---------------------------------------------------------------------------#
root = tk.Tk()
root.title("Ausschankroboter")
root.attributes('-fullscreen', True)
root.configure(background=col_GlobalBackground)

# %% -----------------Bilddateien importieren--------------------------------------------------------------------------#
guiHintergrund = Image.open(FILEPATH + "GUI_Hintergrund.png")
guiHintergrundFoto = ImageTk.PhotoImage(guiHintergrund)

tecLogo = Image.open(FILEPATH + "TEC_logo.png")
tecLogo = tecLogo.resize((400, 150))
tecLogoFoto = ImageTk.PhotoImage(tecLogo)

hsrtLogo = Image.open(FILEPATH + "HSRT_Logo.png")
hsrtLogo = hsrtLogo.resize((622, 150))
hsrtLogoFoto = ImageTk.PhotoImage(hsrtLogo)

buttonStart = Image.open(FILEPATH + "Buttonstart.png")
buttonStartFoto = ImageTk.PhotoImage(buttonStart)

buttonStartPress = Image.open(FILEPATH + "Buttonstart_ausgefuellt.png")
buttonStartPressFoto = ImageTk.PhotoImage(buttonStartPress)

weizen = Image.open(FILEPATH + "weizenFrame.png")  # TODO copyright?!
weizenFoto = ImageTk.PhotoImage(weizen)
weizenHide = Image.open(FILEPATH + "weizenHideFrame.png")  # TODO copyright?!
weizenHideFoto = ImageTk.PhotoImage(weizenHide)

cola = Image.open(FILEPATH + "colaFrame.png")  # TODO copyright?!
colaFoto = ImageTk.PhotoImage(cola)
colaHide = Image.open(FILEPATH + "colaHideFrame.png")  # TODO copyright?!
colaHideFoto = ImageTk.PhotoImage(colaHide)

rectTop = Image.open(FILEPATH + "rectTop.png")
rectTopFoto = ImageTk.PhotoImage(rectTop)

glasPosBox = Image.open(FILEPATH + "glasPosBox.png")
glasPosBoxFoto = ImageTk.PhotoImage(glasPosBox)
glasPosBoxHide = Image.open(FILEPATH + "glasPosBoxHide.png")
glasPosBoxHideFoto = ImageTk.PhotoImage(glasPosBoxHide)

selectboxSelected = Image.open(FILEPATH + "selectbox_selected.png")
selectboxSelected = selectboxSelected.resize((80, 80))
selectboxSelectedFoto = ImageTk.PhotoImage(selectboxSelected)

selectboxUnselected = Image.open(FILEPATH + "selectbox_unselected.png")
selectboxUnselected = selectboxUnselected.resize((80, 80))
selectboxUnselectedFoto = ImageTk.PhotoImage(selectboxUnselected)

bestellenButtonHide = Image.open(FILEPATH + "bestellenHideButton.png")
bestellenButtonHideFoto = ImageTk.PhotoImage(bestellenButtonHide)

statusFrame = Image.open(FILEPATH + "statusFrame.png")
statusFrameFoto = ImageTk.PhotoImage(statusFrame)

# %% -----------------Styles konfigurieren-----------------------------------------------------------------------------#
style = ttk.Style()
# style.theme_use('clam')

# ttk azure theme anwenden: für grundlegendes Design, danach individuelle Anpassungen
root.tk.call("source", FILEPATH + "..\\azure.tcl")
root.tk.call("set_theme", "light")

# alle Pages Hintergrundfarbe
style.configure("global_page_style.TFrame",
                background=col_GlobalBackground)

# Label allgemein
style.configure("BW.TLabel",
                foreground="black",
                background="#cdcdcd",
                font=("Segoe UI", 25))

# Label Hintergrund wie alle Pages
style_invisible_label = ttk.Style()
style_invisible_label.configure("invisible_label.TLabel",
                                background=col_GlobalBackground)

# Button allgemein
style.configure("TButton",
                font=("Arial", 30))

# Start-Label
style.configure("labelStart.TLabel",
                font=(None, 40),
                background=col_GlobalBackground,
                foreground='white'
                )

# Start-Button
styleButtonStart = ttk.Style()
styleButtonStart.configure("buttonStart.TButton",
                           font=("Arial", 40, "bold"),
                           activeforeground="blue",
                           activebackground="red",
                           borderwidth=0,
                           relief='none')

# %% -----------------Pages/Frames erstellen---------------------------------------------------------------------------#
page1 = ttk.Frame(root)  # Startseite
page2 = ttk.Frame(root)  # Auswahl Getränk
page3 = ttk.Frame(root)  # Bierglas reinstellen und Lichtschranke schalten und bestätigen

# %% -----------------Globale Variablen---------------------------------------------------------------------------------#
cola_selected = False
weizen_selected = False
glas_pos_selected = False
bestellung_aufgegeben = False

blinker_value = False
blinker_lamps = []
# %% -----------------Funktionen---------------------------------------------------------------------------------------#
def blinker():
    global blinker_value
    while 1:
        blinker_value = not blinker_value
        for blinker_lamp in blinker_lamps:
            if blinker_value:
                blinker_lamp.set()
            else:
                blinker_lamp.reset()
        time.sleep(0.5)

def handle_gpio():
    while 1:
        #TODO write outputs to and read inputs from Raspberry Pi
        print("ich bin der GPIO Handler")
        time.sleep(1)

def show_frame(frame):
    frame.update()
    frame.tkraise()


def helpPage():  # TODO Help-Page bauen, evtl. pdf o. ä.
    # webbrowser.open_new(LOCALPATH_HS + 'HilfeSeiten.pdf')
    print("Hilfe-Pdf wird in Browser geöffnet")


def showAboutText():
    messagebox.showinfo('About',
                        'Bei weiteren Fragen wenden Sie sich an Prof. Dr. A. Buschhaus.')  # TODO About-Text schreiben


def closeWindow():
    os.system('cls')
    print('Programm wird nun beendet.\n'
          'Dieses Fenster schließt sich nach erfolgreichem Beenden'
          ' automatisch.\nDas kann einen Moment dauern...')
    root.destroy()


def disable_event():
    pass


def show_labelStart_press(event):
    labelStart.config(image=buttonStartPressFoto)


def show_labelStart_release(event):
    labelStart.configure(image=buttonStartFoto)


def cola_select():
    global cola_selected
    cola_selected = True
    if checkbox_weizen.get_selected():
        checkbox_weizen.click()
    show_frame(glasPosBoxFrame)


def cola_unselect():
    global cola_selected
    cola_selected = False
    show_frame(glasPosBoxHideFrame)
    if selectbox_glas.get_selected():
        selectbox_glas.click()


def weizen_select():
    global weizen_selected
    weizen_selected = True
    if checkbox_cola.get_selected():
        checkbox_cola.click()
    show_frame(glasPosBoxFrame)


def weizen_unselect():
    global weizen_selected
    weizen_selected = False
    show_frame(glasPosBoxHideFrame)
    if selectbox_glas.get_selected():
        selectbox_glas.click()


def glas_select():
    global glas_pos_selected
    glas_pos_selected = True
    show_frame(button_bestellen)


def glas_unselect():
    global glas_pos_selected
    glas_pos_selected = False
    print(glas_pos_selected)
    show_frame(button_bestellen_hide)


def bestellen_press():
    global bestellung_aufgegeben
    bestellung_aufgegeben = True
    show_frame(glasPosBoxHideFrame)
    show_frame(labelColaHide)
    show_frame(labelWeizenHide)
    show_frame(button_bestellen_hide)
    if selectbox_glas.get_selected():
        selectbox_glas.click()
    if checkbox_cola.get_selected():
        checkbox_cola.click()
    if checkbox_weizen.get_selected():
        checkbox_weizen.click()

"""
def toggle_glaspos_selected(event):
    global glas_pos_selected
    glas_pos_selected = not glas_pos_selected
    if glas_pos_selected:
        selectBoxGlas.config(image=selectboxSelectedFoto)
    else:
        selectBoxGlas.config(image=selectboxUnselectedFoto)
"""

# %% -----------------Popup-Fenster------------------------------------------------------------------------------------#
def open_popupConfirm():
    popup_confirm = tk.Toplevel(root)
    popup_confirm.geometry("750x250")
    popup_confirm.title("Glas einstellen und Lichtschranke schließen")
    popup_confirm.protocol("WM_DELETE_WINDOW", disable_event)


# %% -----------------Menüband-----------------------------------------------------------------------------------------#
menu = tk.Menu(master=root)
root.config(menu=menu)

entwicklerMenu = tk.Menu(menu)
menu.add_cascade(label="Entwickleroptionen", menu=entwicklerMenu)
entwicklerMenu.add_command(label="Page1",
                           command=lambda: show_frame(page1))
entwicklerMenu.add_command(label="Page2",
                           command=lambda: show_frame(page2))
entwicklerMenu.add_command(label="Page3",
                           command=lambda: show_frame(page3))

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Hilfeseite öffnen", command=helpPage)

aboutMenu = tk.Menu(menu)
menu.add_cascade(label="About", menu=aboutMenu)
aboutMenu.add_command(label="Über diese Anwendung",
                      command=showAboutText)

quitMenu = tk.Menu(menu)
menu.add_cascade(label="Quit", menu=quitMenu)
quitMenu.add_command(label="Fenster schließen",
                     command=closeWindow)

# %% -----------------all pages----------------------------------------------------------------------------------------#
for frame in (page1, page2, page3):
    frame.place(x=0, y=0, width=1920, height=1060)
    frame.config(style="global_page_style.TFrame")

    label = ttk.Label(frame,
                      image=tecLogoFoto,
                      borderwidth=0,
                      style="invisible_label.TLabel")
    label.place(x=30,
                y=30)

    label = ttk.Label(frame,
                      image=hsrtLogoFoto,
                      borderwidth=0,
                      style="invisible_label.TLabel")
    label.place(x=1268,
                y=30)

show_frame(page1)

# %% -----------------page1--------------------------------------------------------------------------------------------#
Willkommen_label = ttk.Label(page1,
                             text="Willkommen",
                             font=(None, 100),
                             anchor='center',
                             background=col_Grey,
                             foreground='white')
Willkommen_label.place(x=0,
                       y=390,
                       width=1920,
                       height=300)

labelStart = ttk.Label(page1,
                       # TODO bind das Label, image ändern wenn Maus drüber, nächste Seite aufrufen mit showFrame() wenn geklickt
                       image=buttonStartFoto,
                       text="Start",
                       compound="center",
                       font=('Segoe UI', 30),
                       style='labelStart.TLabel')
labelStart.place(relx=0.5,
                 y=850,
                 anchor='center')
labelStart.bind("<ButtonPress>", show_labelStart_press)
labelStart.bind("<ButtonRelease>", show_labelStart_release)

buttonStart = ttk.Button(page1,
                         image=buttonStartFoto,
                         text="Start",
                         compound='center',
                         style="buttonStart.TButton",
                         command=lambda: show_frame(page2))
buttonStart.place(relx=0.5,
                  y=850,
                  anchor='center')


# %% -----------------page2--------------------------------------------------------------------------------------------#
labelWeizen = ttk.Label(page2, image=weizenFoto, style="invisible_label.TLabel")
labelWeizen.place(x=30, y=240)
labelWeizenHide = ttk.Label(page2, image=weizenHideFoto, style="invisible_label.TLabel")
labelWeizenHide.place(x=30, y=240)
show_frame(labelWeizen)

labelCola = ttk.Label(page2, image=colaFoto, style="invisible_label.TLabel")
labelCola.place(x=355, y=240)
labelColaHide = ttk.Label(page2, image=colaHideFoto, style="invisible_label.TLabel")
labelColaHide.place(x=355, y=240)
show_frame(labelCola)

checkbox_weizen = gui.CheckBox(labelWeizen, 80, 80, "invisible_label.TLabel", False, weizen_select, weizen_unselect)
checkbox_weizen.place(x=107, y=670)
checkbox_cola = gui.CheckBox(labelCola, 80, 80, "invisible_label.TLabel", False, cola_select, cola_unselect)
checkbox_cola.place(x=107, y=670)

glasPosBoxFrame = ttk.Label(page2, image=glasPosBoxFoto, style="invisible_label.TLabel")
glasPosBoxFrame.place(x=680, y=240)
glasPosBoxHideFrame = ttk.Label(page2, image=glasPosBoxHideFoto, style="invisible_label.TLabel")
glasPosBoxHideFrame.place(x=680, y=240)

selectbox_glas = gui.SelectBox(glasPosBoxFrame, 80, 80, "invisible_label.TLabel", False, glas_select, glas_unselect)
selectbox_glas.place(x=470, y=485)

button_bestellen = gui.BestellenButton(page2, 590, 157, "invisible_label.TLabel", None, bestellen_press)
button_bestellen.place(x=680, y=870)
button_bestellen_hide = ttk.Label(page2, image=bestellenButtonHideFoto, style="invisible_label.TLabel")
button_bestellen_hide.place(x=680, y=870)


statusFrame = ttk.Label(page2, image=statusFrameFoto, style="invisible_label.TLabel")
statusFrame.place(x=1300, y=240)

lamp_lichtschranke = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_lichtschranke.place(x=460, y=30)
lamp_lichtschranke.config_red()
lamp_lichtschranke.set()

lamp_2 = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_2.place(x=460, y=160)
lamp_2.config_blue()
blinker_lamps.append(lamp_2)

lamp_3 = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_3.place(x=460, y=290)
lamp_3.config_green()
lamp_3.set()

lamp_4 = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_4.place(x=460, y=420)
lamp_4.config_yellow()
blinker_lamps.append(lamp_4)



"""
blinker_lamps.append(lichtschranke_status)
blinker_lamps.remove(lichtschranke_status)
lichtschranke_status.set()
"""


# %% -----------------page3--------------------------------------------------------------------------------------------#
buttonStartBier = ttk.Button(page3, text="Bierglas steht drin",
                             command=lambda: show_frame(page3),
                             style='button.TButton')
buttonStartBier.place(x=1360,
                      y=700,
                      width=400,
                      height=200)

# %% -----------------start mainloop-----------------------------------------------------------------------------------#
thread_blinker = Thread(target=blinker)
thread_blinker.setDaemon(True)
thread_blinker.start()

thread_gpio = Thread(target=handle_gpio)
thread_gpio.setDaemon(True)
thread_gpio.start()

root.mainloop()
