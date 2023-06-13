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

        super(CheckBox, self).__init__(frame,
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
