# %% Imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

import gui_elements
import gui_elements as gui
from threading import Thread
import time
from tkPDFViewer2 import tkPDFViewer as pdf
import RPi.GPIO as GPIO
import sys

from filepath import *

# %% -----------------Farben definieren--------------------------------------------------------------------------------#
# col_Blue = '#%02x%02x%02x' % (1, 105, 196)  # RGB values
col_Blue = '#%02x%02x%02x' % (18, 123, 202)  # RGB values TEC blue
col_Grey = '#%02x%02x%02x' % (200, 200, 200)  # RGB values
col_HSRTGrey = '#%02x%02x%02x' % (102, 102, 102)  # RGB values
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
tecLogo = tecLogo.resize((300, 113))
tecLogoFoto = ImageTk.PhotoImage(tecLogo)

hsrtLogo = Image.open(FILEPATH + "HSRT_Logo.png")
hsrtLogo = hsrtLogo.resize((467, 113))
hsrtLogoFoto = ImageTk.PhotoImage(hsrtLogo)

buttonStart = Image.open(FILEPATH + "Buttonstart.png")
buttonStartFoto = ImageTk.PhotoImage(buttonStart)

buttonStartPress = Image.open(FILEPATH + "Buttonstart_ausgefuellt.png")
buttonStartPressFoto = ImageTk.PhotoImage(buttonStartPress)

weizen = Image.open(FILEPATH + "weizenFrame.png")
weizenFoto = ImageTk.PhotoImage(weizen)
weizenHide = Image.open(FILEPATH + "weizenHideFrame.png")
weizenHideFoto = ImageTk.PhotoImage(weizenHide)

cola = Image.open(FILEPATH + "colaFrame.png")
colaFoto = ImageTk.PhotoImage(cola)
colaHide = Image.open(FILEPATH + "colaHideFrame.png")
colaHideFoto = ImageTk.PhotoImage(colaHide)

colaGlas = Image.open(FILEPATH + "colaGlas.png")
colaGlasFoto = ImageTk.PhotoImage(colaGlas)

bierGlas = Image.open(FILEPATH + "bierGlas.png")
bierGlasFoto = ImageTk.PhotoImage(bierGlas)

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
root.tk.call("source", FILEPATH_STYLE)
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
page2 = ttk.Frame(root)  # Auswahl Getränk, Bestellung, Status

# %% -----------------Globale Variablen--------------------------------------------------------------------------------#
flag_ausschank = False
cola_selected = False
weizen_selected = False
glas_pos_selected = False
bestellung_aufgegeben = False

blinker_value = False
blinker_lamps = []

# Outputs
doBier = 6
doCola = 13
doStartAusschankInvert = 19
do4 = 26

# Inputs
di1 = 12
di2 = 16
diAusschankAktiv = 20
diLichtschranke = 21


# %% -----------------Funktionen---------------------------------------------------------------------------------------#
def blinker():
    global blinker_value
    global blinker_lamps
    while 1:
        blinker_value = not blinker_value
        for blinker_lamp in blinker_lamps:
            if blinker_value:
                blinker_lamp.set()
            else:
                blinker_lamp.reset()
        time.sleep(0.5)


def handle_gpio():
    # init GPIOs

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(doBier, GPIO.OUT)
    GPIO.setup(doCola, GPIO.OUT)
    GPIO.setup(doStartAusschankInvert, GPIO.OUT)
    GPIO.setup(do4, GPIO.OUT)
    GPIO.setup(di1, GPIO.IN)
    GPIO.setup(di2, GPIO.IN)
    GPIO.setup(diAusschankAktiv, GPIO.IN)
    GPIO.setup(diLichtschranke, GPIO.IN)

    GPIO.output(doBier, GPIO.HIGH)
    GPIO.output(doCola, GPIO.HIGH)
    GPIO.output(doStartAusschankInvert, GPIO.LOW)
    GPIO.output(do4, GPIO.HIGH)


def handle_inputs():
    global flag_ausschank
    global bestellung_aufgegeben
    global blinker_lamps

    while True:
        if GPIO.input(diLichtschranke) == GPIO.HIGH:
            lamp_licht_offen.set()
        else:
            lamp_licht_offen.reset()

        if GPIO.input(diAusschankAktiv) == GPIO.LOW and bestellung_aufgegeben and not flag_ausschank: # Ausschank läuft
            blinker_lamps.append(lamp_ausschank_aktiv)
            flag_ausschank = True
        if GPIO.input(diAusschankAktiv) == GPIO.HIGH and flag_ausschank: # Ausschank beendet
            blinker_lamps.remove(lamp_ausschank_aktiv)
            lamp_ausschank_fertig.set()
            flag_ausschank = False
            bestellung_aufgegeben = False
            lamp_ausschank_aktiv.reset()
            messagebox.showinfo('Fertig',
                                'Ausschankvorgang beendet. Bitte volles Glas entnehmen und OK drücken.')
            reset_to_start()

        time.sleep(0.3)


def show_frame(frame):
    frame.update()
    frame.tkraise()


def show_page2():
    page2.update()
    page2.tkraise()


def reset_to_start():
    global cola_selected
    global weizen_selected
    global glas_pos_selected
    global bestellung_aufgegeben
    global blinker_lamps
    global flag_ausschank
    global lamp_ausschank_aktiv
    global lamp_getr_bestellt
    global lamp_ausschank_fertig
    global doCola
    global doBier
    global doStartAusschankInvert
    global labelCola
    global checkbox_cola
    global labelWeizen
    global checkbox_weizen
    global page1

    cola_unselect()
    weizen_unselect()
    glas_unselect()
    bestellung_aufgegeben = False
    if flag_ausschank:
        blinker_lamps.remove(lamp_ausschank_aktiv)
    lamp_ausschank_aktiv.reset()
    lamp_getr_bestellt.reset()
    lamp_ausschank_fertig.reset()
    GPIO.output(doCola, GPIO.HIGH) # reset GPIO
    GPIO.output(doBier, GPIO.HIGH) # reset GPIO
    GPIO.output(doStartAusschankInvert, GPIO.LOW) # reset GPIO
    show_frame(labelCola)
    show_frame(checkbox_cola)
    show_frame(labelWeizen)
    show_frame(checkbox_weizen)
    show_frame(page1)


def helpPage():  # TODO Help-Page bauen, evtl. pdf o. ä.
    # webbrowser.open_new(LOCALPATH_HS + 'HilfeSeiten.pdf')
    print("Hilfe-Pdf wird in Browser geöffnet")


def showAboutText():
    messagebox.showinfo('About',
                        'Diese Roboterzelle wurde im Rahmen von Abschluss- und Projektarbeiten entwickelt. '
                        'Bei weiteren Fragen wenden Sie sich an Prof. Dr. Arnd Buschhaus.')



def closeWindow():
    #os.system('clear')
    print('Programm wird nun beendet.\n'
          'Dieses Fenster schließt sich nach erfolgreichem Beenden'
          ' automatisch.\nDas kann einen Moment dauern...')
    root.destroy()
    GPIO.cleanup() # GPIO-Instanzen aufräumen


def disable_event():
    pass


def cola_select():
    global cola_selected
    cola_selected = True
    if checkbox_weizen.get_selected():
        checkbox_weizen.click()
    show_frame(glasPosBoxFrame)
    show_frame(colaGlasFrame)
    lamp_getr_gew.set()


def cola_unselect():
    global cola_selected
    cola_selected = False
    lamp_getr_gew.reset()
    show_frame(glasPosBoxHideFrame)
    if checkbox_cola.get_selected():
        checkbox_cola.click()
    if selectbox_glas.get_selected():
        selectbox_glas.click()


def weizen_select():
    global weizen_selected
    weizen_selected = True
    if checkbox_cola.get_selected():
        checkbox_cola.click()
    show_frame(glasPosBoxFrame)
    show_frame(bierGlasFrame)
    lamp_getr_gew.set()


def weizen_unselect():
    global weizen_selected
    weizen_selected = False
    lamp_getr_gew.reset()
    show_frame(glasPosBoxHideFrame)
    if checkbox_weizen.get_selected():
        checkbox_weizen.click()
    if selectbox_glas.get_selected():
        selectbox_glas.click()


def glas_select():
    global glas_pos_selected
    glas_pos_selected = True
    show_frame(button_bestellen)
    lamp_glas_pos_done.set()


def glas_unselect():
    global glas_pos_selected
    glas_pos_selected = False
    show_frame(button_bestellen_hide)
    lamp_glas_pos_done.reset()


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
        GPIO.output(doCola, GPIO.LOW) # set GPIO
        GPIO.output(doStartAusschankInvert, GPIO.HIGH)  # set GPIO
    if checkbox_weizen.get_selected():
        checkbox_weizen.click()
        GPIO.output(doBier, GPIO.LOW) # set GPIO
        GPIO.output(doStartAusschankInvert, GPIO.HIGH)  # set GPIO
    lamp_getr_gew.set()
    lamp_glas_pos_done.set()
    lamp_getr_bestellt.set()
    time.sleep(0.5)
    GPIO.output(doCola, GPIO.HIGH) # reset GPIO
    GPIO.output(doBier, GPIO.HIGH) # reset GPIO
    GPIO.output(doStartAusschankInvert, GPIO.LOW) # reset GPIO


# %% -----------------Popup-Fenster------------------------------------------------------------------------------------#
def open_popupHelp():
    return
    popup_help = tk.Toplevel(root)
    popup_help.geometry("1000x1000")
    popup_help.title("Hilfe")
    pdf_page = pdf.ShowPdf()
    help_page = pdf_page.pdf_view(popup_help,
                                  height=1000,
                                  width=1000,
                                  pdf_location="help.pdf")
    help_page.pack(anchor="center")


# %% -----------------Menüband-----------------------------------------------------------------------------------------#
menu = tk.Menu(master=root)
root.config(menu=menu)

entwicklerMenu = tk.Menu(menu)
menu.add_cascade(label="Go to", menu=entwicklerMenu)
entwicklerMenu.add_command(label="Page1",
                           command=lambda: reset_to_start())
entwicklerMenu.add_command(label="Page2",
                           command=lambda: show_frame(page2))


helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Hilfeseite öffnen", command=open_popupHelp)

aboutMenu = tk.Menu(menu)
menu.add_cascade(label="About", menu=aboutMenu)
aboutMenu.add_command(label="Über diese Anwendung",
                      command=showAboutText)

quitMenu = tk.Menu(menu)
menu.add_cascade(label="Quit", menu=quitMenu)
quitMenu.add_command(label="Fenster schließen",
                     command=closeWindow)

# %% -----------------all pages----------------------------------------------------------------------------------------#
for frame in (page1, page2):
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
    label.place(x=1423,
                y=30)

    label = ttk.Label(frame,
                      text="Ausschankroboter",
                      style="invisible_label.TLabel",
                      font=('Arial', 50),
                      foreground=col_HSRTGrey,
                      anchor='n')
    label.place(x=590,
                y=50)

show_frame(page1)

# %% -----------------page1--------------------------------------------------------------------------------------------#
Willkommen_label = ttk.Label(page1,
                             text="Willkommen",
                             font=(None, 100),
                             anchor='center',
                             background=col_Grey,
                             foreground=col_HSRTGrey)
Willkommen_label.place(x=-420,
                       y=390,
                       width=1920,
                       height=300)


buttonStart = gui_elements.StartButton(page1, 800, 630, "invisible_label.TLabel", None, show_page2)
buttonStart.place(relx=0.71,
                  y=600,
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

colaGlasFrame = ttk.Label(glasPosBoxFrame, image=colaGlasFoto, style="invisible_label.TLabel")
colaGlasFrame.place(x=90, y=90)
bierGlasFrame = ttk.Label(glasPosBoxFrame, image=bierGlasFoto, style="invisible_label.TLabel")
bierGlasFrame.place(x=90, y=90)

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

label_1 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Getränk ausgewählt", font=("Arial", 30))
label_1.place(anchor="e", x=430, y=70)
lamp_getr_gew = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_getr_gew.place(anchor="w", x=460, y=70)
lamp_getr_gew.config_green()

label_2 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Glas positioniert", font=("Arial", 30))
label_2.place(anchor="e", x=430, y=200)
lamp_glas_pos_done = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_glas_pos_done.place(anchor="w", x=460, y=200)
lamp_glas_pos_done.config_green()

label_3 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Getränk bestellt", font=("Arial", 30))
label_3.place(anchor="e", x=430, y=330)
lamp_getr_bestellt = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_getr_bestellt.place(anchor="w", x=460, y=330)
lamp_getr_bestellt.config_green()

label_4 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Ausschank läuft", font=("Arial", 30))
label_4.place(anchor="e", x=430, y=460)
lamp_ausschank_aktiv = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_ausschank_aktiv.place(anchor="w", x=460, y=460)
lamp_ausschank_aktiv.config_yellow()

label_5 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Lichtschranke offen", font=("Arial", 30))
label_5.place(anchor="e", x=430, y=720)
lamp_licht_offen = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_licht_offen.place(anchor="w", x=460, y=720)
lamp_licht_offen.config_red()

label_6 = ttk.Label(statusFrame, style="invisible_label.TLabel", text="Ausschank fertig", font=("Arial", 30))
label_6.place(anchor="e", x=430, y=590)
lamp_ausschank_fertig = gui.SignalLamp(statusFrame, 100, 100, "invisible_label.TLabel")
lamp_ausschank_fertig.place(anchor="w", x=460, y=590)
lamp_ausschank_fertig.config_green()

# %% -----------------start mainloop-----------------------------------------------------------------------------------#
thread_blinker = Thread(target=blinker)
thread_blinker.setDaemon(True)
thread_blinker.start()

thread_gpio = Thread(target=handle_gpio)
thread_gpio.setDaemon(True)
thread_gpio.start()

thread_inputs = Thread(target=handle_inputs)
thread_inputs.setDaemon(True)
thread_inputs.start()

root.mainloop()
