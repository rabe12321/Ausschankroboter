# Imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


def showFrame(frame):
    frame.update()
    frame.tkraise()

def helpPage():
    # webbrowser.open_new(LOCALPATH_HS + 'HilfeSeiten.pdf')
    print("Hilfe-Pdf wird in Browser geöffnet")

def showAboutText():
    messagebox.showinfo('About', 'Diese Applikation ist im Rahmen einer Bachelorarbeit von Paul Stephan entstanden.\n'
                                 'Der Industrieroboter der Firma FANUC wird verwendet, um Portraits zu zeichnen.\n'
                                 'Eine Kamera nimmt ein Bild auf und am Rechner wird anschließend dieses Bild verarbeitet.\n'
                                 'Es entsteht ein Kantenbild, aus welchem Koordinatenwerte für den Roboter erstellt werden.\n'
                                 'Eine für den Roboter ausführbare Datei wird zum Schluss an den Roboter gesendet.\n'
                                 'Bei weiteren Fragen wenden Sie sich an Prof.-Dr. A. Buschhaus.')


def closeWindow():
    os.system('cls')
    print('Programm wird nun beendet.\n'
          'Dieses Fenster schließt sich nach erfolgreichem Beenden'
          ' automatisch.\nDas kann einen Moment dauern...')
    root.destroy()

# Hauptfenster
root = tk.Tk()
root.title("Automatisiertes Portraitzeichnen")
root.attributes('-fullscreen', True)

# Style der Widgets konfigurieren
style = ttk.Style()
style.theme_use("clam")
style.configure("BW.TLabel", foreground="black",
                background="#cdcdcd", font=("Arial", 25))
style.configure("TButton", font=("Arial", 30))
style.configure("button.TButton", font=("Arial", 40, "bold"),
                foreground="white", background="#797979",
                relief='raised')
style.configure("buttonHelp.TButton", font=("Arial", 14, "bold"),
                foreground="white", background="#797979",
                relief='raised')
style.configure("startBild.TLabel", background="black")

# Frames definieren
page1 = ttk.Frame(root) # Startseite
page2 = ttk.Frame(root) # Auswahl Getränk
page3 = ttk.Frame(root) # Bierglas reinstellen und Lichtschranke schalten und bestätigen
page4 = ttk.Frame(root) # Colaglas reinstellen und Lichtschranke schalten und bestätigen
page5 = ttk.Frame(root) # Getränk in Arbeit
page6 = ttk.Frame(root) # Getränk fertig, Glas entnehmen

# Menuband
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
entwicklerMenu.add_command(label="Page5",
                           command=lambda: showFrame(page5))
entwicklerMenu.add_command(label="Page6",
                           command=lambda: showFrame(page6))

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

# Bild für den Hintergrund öffnen und allen Frames
# dieses Bild zuweisen
guiHintergrund = Image.open("images\GUI_Hintergrund.png")
guiHintergrundFoto = ImageTk.PhotoImage(guiHintergrund)

for frame in (page1, page2, page3, page4, page5, page6):
    frame.place(x=0, y=0, width=1920, height=1060)
    label = ttk.Label(frame, image=guiHintergrundFoto, borderwidth=0)
    label.place(x=0, y=0)

showFrame(page1)


#----------------Page1----------------#
buttonStart = ttk.Button(page1, text="Start",
                         command=lambda: showFrame(page2),
                         style='button.TButton')
buttonStart.place(x=1360, y=700, width=400, height=200)


#----------------Page2----------------#
buttonBier = ttk.Button(page2, text="Bier",
                         command=lambda: showFrame(page3),
                         style='button.TButton')
buttonBier.place(x=760, y=700, width=400, height=200)

buttonCola = ttk.Button(page2, text="Cola",
                         command=lambda: showFrame(page4),
                         style='button.TButton')
buttonCola.place(x=1360, y=700, width=400, height=200)


#----------------Page3----------------#
buttonStartBier = ttk.Button(page3, text="Bierglas steht drin",
                         command=lambda: showFrame(page5),
                         style='button.TButton')
buttonStartBier.place(x=1360, y=700, width=400, height=200)


#----------------Page4----------------#
buttonStartCola = ttk.Button(page4, text="Colaglas steht drin",
                         command=lambda: showFrame(page5),
                         style='button.TButton')
buttonStartCola.place(x=1360, y=700, width=400, height=200)


#----------------Page5----------------#
buttonNurEntwicklung = ttk.Button(page5, text="nur Entwicklung",
                         command=lambda: showFrame(page6),
                         style='button.TButton')
buttonNurEntwicklung.place(x=1360, y=700, width=400, height=200)


#----------------Page6----------------#
buttonBackToStart = ttk.Button(page6, text="zurück zum Start",
                         command=lambda: showFrame(page2),
                         style='button.TButton')
buttonBackToStart.place(x=1360, y=700, width=400, height=200)



root.mainloop()
