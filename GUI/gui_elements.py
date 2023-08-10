from filepath import FILEPATH
from PIL import Image, ImageTk
import tkinter.ttk as ttk


class CheckBox(ttk.Label):
    def __init__(self, frame, size_x, size_y, style, selected, command_select, command_unselect):
        self.__checkbox_selected = Image.open(FILEPATH + "Checkbox_selected.png")
        self.__checkbox_selected = self.__checkbox_selected.resize((size_x, size_y))
        self.__checkbox_selected_foto = ImageTk.PhotoImage(self.__checkbox_selected)

        self.__checkbox_unselected = Image.open(FILEPATH + "Checkbox_unselected.png")
        self.__checkbox_unselected = self.__checkbox_unselected.resize((size_x, size_y))
        self.__checkbox_unselected_foto = ImageTk.PhotoImage(self.__checkbox_unselected)

        self.__command_select = command_select
        self.__command_unselect = command_unselect

        super(CheckBox, self).__init__(frame,
                                       image=self.__checkbox_unselected_foto,
                                       style=style)

        self.__is_selected = selected

        if self.__is_selected:
            self.config(image=self.__checkbox_selected_foto)
            self.__is_selected = True

        self.bind("<Button-1>", self.click)

    def click(self, event=""):
        if event == "":
            event = self.event_info()
        if self.__is_selected:
            self.unselect(self.__command_unselect)
        else:
            self.select(self.__command_select)

    def select(self, command):
        self.config(image=self.__checkbox_selected_foto)
        self.__is_selected = True
        if command is None:
            pass
        else:
            command()

    def unselect(self, command):
        self.config(image=self.__checkbox_unselected_foto)
        self.__is_selected = False
        if command is None:
            pass
        else:
            command()

    def get_selected(self):
        return self.__is_selected

    def resize(self, size_x, size_y):
        self.__checkbox_selected = self.__checkbox_selected.resize((size_x, size_y))
        self.__checkbox_selected_foto = ImageTk.PhotoImage(self.__checkbox_selected)
        self.__checkbox_unselected = self.__checkbox_unselected.resize((size_x, size_y))
        self.__checkbox_unselected_foto = ImageTk.PhotoImage(self.__checkbox_unselected)


class SelectBox(ttk.Label):
    def __init__(self, frame, size_x, size_y, style, selected, command_select, command_unselect):
        self.__selectbox_selected = Image.open(FILEPATH + "selectbox_selected.png")
        self.__selectbox_selected = self.__selectbox_selected.resize((size_x, size_y))
        self.__selectbox_selected_foto = ImageTk.PhotoImage(self.__selectbox_selected)

        self.__selectbox_unselected = Image.open(FILEPATH + "selectbox_unselected.png")
        self.__selectbox_unselected = self.__selectbox_unselected.resize((size_x, size_y))
        self.__selectbox_unselected_foto = ImageTk.PhotoImage(self.__selectbox_unselected)

        self.__command_select = command_select
        self.__command_unselect = command_unselect

        super(SelectBox, self).__init__(frame,
                                        image=self.__selectbox_unselected_foto,
                                        style=style)

        self.__is_selected = selected

        if self.__is_selected:
            self.config(image=self.__selectbox_selected_foto)
            self.__is_selected = True

        self.bind("<Button-1>", self.click)

    def click(self, event=""):
        if event == "":
            event = self.event_info()
        if self.__is_selected:
            self.unselect(self.__command_unselect)
        else:
            self.select(self.__command_select)

    def select(self, command):
        self.config(image=self.__selectbox_selected_foto)
        self.__is_selected = True
        if command is None:
            pass
        else:
            command()

    def unselect(self, command):
        self.config(image=self.__selectbox_unselected_foto)
        self.__is_selected = False
        if command is None:
            pass
        else:
            command()

    def get_selected(self):
        return self.__is_selected

    def resize(self, size_x, size_y):
        self.__selectbox_selected = self.__selectbox_selected.resize((size_x, size_y))
        self.__selectbox_selected_foto = ImageTk.PhotoImage(self.__selectbox_selected)
        self.__selectbox_unselected = self.__selectbox_unselected.resize((size_x, size_y))
        self.__selectbox_unselected_foto = ImageTk.PhotoImage(self.__selectbox_unselected)


class BestellenButton(ttk.Label):
    def __init__(self, frame, size_x, size_y, style, command_press, command_release):
        self.__button = Image.open(FILEPATH + "bestellenButton.png")
        self.__button = self.__button.resize((size_x, size_y))
        self.__button_foto = ImageTk.PhotoImage(self.__button)

        self.__button_pressed = Image.open(FILEPATH + "bestellenButtonPressed.png")
        self.__button_pressed = self.__button_pressed.resize((size_x, size_y))
        self.__button_pressed_foto = ImageTk.PhotoImage(self.__button_pressed)

        self.__command_press = command_press
        self.__command_release = command_release


        super(BestellenButton, self).__init__(frame, image=self.__button_foto, style=style)

        self.__is_pressed = False

        self.bind("<ButtonPress-1>", self.press)
        self.bind("<ButtonRelease-1>", self.release)

    def press(self, event=""):
        if event == "":
            event = self.event_info()
        self.config(image=self.__button_pressed_foto)
        if self.__command_press is None:
            pass
        else:
            self.__command_press()
        self.__is_pressed = True

    def release(self, event=""):
        if event == "":
            event = self.event_info()
        self.config(image=self.__button_foto)
        if self.__command_release is None:
            pass
        else:
            self.__command_release()
        self.__is_pressed = False

    def resize(self, size_x, size_y):
        self.__button = self.__button.resize((size_x, size_y))
        self.__button_foto = ImageTk.PhotoImage(self.__button)
        self.__button_pressed = self.__button_pressed.resize((size_x, size_y))
        self.__button_pressed_foto = ImageTk.PhotoImage(self.__button_pressed)

class FertigButton(ttk.Label):
    def __init__(self, frame, size_x, size_y, style, command_press, command_release):
        self.__button = Image.open(FILEPATH + "bestellenButton.png")
        self.__button = self.__button.resize((size_x, size_y))
        self.__button_foto = ImageTk.PhotoImage(self.__button)

        self.__button_pressed = Image.open(FILEPATH + "bestellenButtonPressed.png")
        self.__button_pressed = self.__button_pressed.resize((size_x, size_y))
        self.__button_pressed_foto = ImageTk.PhotoImage(self.__button_pressed)

        self.__command_press = command_press
        self.__command_release = command_release


        super(FertigButton, self).__init__(frame, image=self.__button_foto, style=style)

        self.__is_pressed = False

        self.bind("<ButtonPress-1>", self.press)
        self.bind("<ButtonRelease-1>", self.release)

    def press(self, event=""):
        if event == "":
            event = self.event_info()
        self.config(image=self.__button_pressed_foto)
        if self.__command_press is None:
            pass
        else:
            self.__command_press()
        self.__is_pressed = True

    def release(self, event=""):
        if event == "":
            event = self.event_info()
        self.config(image=self.__button_foto)
        if self.__command_release is None:
            pass
        else:
            self.__command_release()
        self.__is_pressed = False

    def resize(self, size_x, size_y):
        self.__button = self.__button.resize((size_x, size_y))
        self.__button_foto = ImageTk.PhotoImage(self.__button)
        self.__button_pressed = self.__button_pressed.resize((size_x, size_y))
        self.__button_pressed_foto = ImageTk.PhotoImage(self.__button_pressed)


class SignalLamp(ttk.Label):

    def __init__(self, frame, size_x, size_y, style):
        self.__off = Image.open(FILEPATH + "signalOff.png")
        self.__off = self.__off.resize((size_x, size_y))
        self.__off_foto = ImageTk.PhotoImage(self.__off)

        self.__red = Image.open(FILEPATH + "signalRed.png")
        self.__red = self.__red.resize((size_x, size_y))
        self.__red_foto = ImageTk.PhotoImage(self.__red)

        self.__green = Image.open(FILEPATH + "signalGreen.png")
        self.__green = self.__green.resize((size_x, size_y))
        self.__green_foto = ImageTk.PhotoImage(self.__green)

        self.__blue = Image.open(FILEPATH + "signalBlue.png")
        self.__blue = self.__blue.resize((size_x, size_y))
        self.__blue_foto = ImageTk.PhotoImage(self.__blue)

        self.__yellow = Image.open(FILEPATH + "signalYellow.png")
        self.__yellow = self.__yellow.resize((size_x, size_y))
        self.__yellow_foto = ImageTk.PhotoImage(self.__yellow)

        self.__on_foto = self.__red_foto

        super(SignalLamp, self).__init__(frame, image=self.__off_foto, style=style)

        self.__is_active = False

    def reset(self):
        self.config(image=self.__off_foto)
        self.__is_active = False;

    def config_red(self):
        self.__on_foto = self.__red_foto
        self.__is_active = True

    def config_green(self):
        self.__on_foto = self.__green_foto
        self.__is_active = True

    def config_blue(self):
        self.__on_foto = self.__blue_foto
        self.__is_active = True

    def config_yellow(self):
        self.__on_foto = self.__yellow_foto
        self.__is_active = True

    def set(self):
        self.config(image=self.__on_foto)

    def get_active(self):
        return self.__is_active
