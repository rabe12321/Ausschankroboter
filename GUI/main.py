# %% Imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import gui_elements as gui
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

cola = Image.open(FILEPATH + "colaFrame.png")  # TODO copyright?!
colaFoto = ImageTk.PhotoImage(cola)

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


# %% -----------------Funktionen---------------------------------------------------------------------------------------#
def showFrame(frame):
    frame.update()
    frame.tkraise()


def show_widget(frame):
    frame.place()


def hide_widget(frame):
    frame.place_forget()


def helpPage():  # TODO Help-Page bauen, evtl. pdf o. ä.
    # webbrowser.open_new(LOCALPATH_HS + 'HilfeSeiten.pdf')
    print("Hilfe-Pdf wird in Browser geöffnet")


def showAboutText():
    messagebox.showinfo('About',
                        'Bei weiteren Fragen wenden Sie sich an Prof.-Dr. A. Buschhaus.')  # TODO About-Text schreiben


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


def cola_unselect():
    global cola_selected
    cola_selected = False


def weizen_select():
    global weizen_selected
    weizen_selected = True
    if checkbox_cola.get_selected():
        checkbox_cola.click()


def weizen_unselect():
    global weizen_selected
    weizen_selected = False


def toggle_glaspos_selected(event):
    global glas_pos_selected
    glas_pos_selected = not glas_pos_selected
    if glas_pos_selected:
        selectBoxGlas.config(image=selectboxSelectedFoto)
    else:
        selectBoxGlas.config(image=selectboxUnselectedFoto)


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
                           command=lambda: showFrame(page1))
entwicklerMenu.add_command(label="Page2",
                           command=lambda: showFrame(page2))
entwicklerMenu.add_command(label="Page3",
                           command=lambda: showFrame(page3))

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

showFrame(page1)

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
                         command=lambda: showFrame(page2))
buttonStart.place(relx=0.5,
                  y=850,
                  anchor='center')


def commandselect():
    print("commandselect")


def commandunselect():
    print("commandunselect")


checkboxtest = gui.CheckBox(page1, 500, 500, "invisible_label.TLabel", True, commandselect, None)
checkboxtest.place(x=100, y=100)

# %% -----------------page2--------------------------------------------------------------------------------------------#
labelWeizen = ttk.Label(page2,
                        image=weizenFoto,
                        style="invisible_label.TLabel")
labelWeizen.place(x=30,
                  y=265)

labelCola = ttk.Label(page2,
                      image=colaFoto,
                      style="invisible_label.TLabel")
labelCola.place(x=320,
                y=265)

checkbox_weizen = gui.CheckBox(labelWeizen, 80, 80, "invisible_label.TLabel", False, weizen_select, weizen_unselect)
checkbox_weizen.place(x=90, y=590)

checkbox_cola = gui.CheckBox(labelCola, 80, 80, "invisible_label.TLabel", False, cola_select, cola_unselect)
checkbox_cola.place(x=90, y=590)

glasPosBoxFrame = ttk.Label(page2,
                            image=glasPosBoxFoto,
                            style="invisible_label.TLabel")
glasPosBoxFrame.place(x=610,
                      y=265)

glasPosBoxHideFrame = ttk.Label(page2,
                                image=glasPosBoxHideFoto,
                                style="invisible_label.TLabel")
glasPosBoxHideFrame.place(x=610,
                          y=265)

selectBoxGlas = ttk.Label(glasPosBoxFrame,
                          image=selectboxUnselectedFoto,
                          style="invisible_label.TLabel")
selectBoxGlas.place(x=583,
                    y=410)
selectBoxGlas.bind("<Button-1>", toggle_glaspos_selected)

# %% -----------------page3--------------------------------------------------------------------------------------------#
buttonStartBier = ttk.Button(page3, text="Bierglas steht drin",
                             command=lambda: showFrame(page3),
                             style='button.TButton')
buttonStartBier.place(x=1360,
                      y=700,
                      width=400,
                      height=200)

# %% -----------------start mainloop-----------------------------------------------------------------------------------#
root.mainloop()
