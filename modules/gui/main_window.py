import json
import customtkinter as ctk
from pathlib import Path

import threading
import tkinter as tk
from .calculator.database.student import Student
from .button_func import ButtonFunc

DEFAULT_LANGUAGE_INDEX = 0
LANGUAGES = ["ru", "en"]
LANGUAGES_FILES = ["excel", "menu_buttons", "student_info"]

EVENTS_PATH = "./resourses/db/events.db"
INCOMING_PATH = "./resourses/db/incoming.db"
language_template = "./resourses/languages/{language}/{file_name}.json"

window_min_width, window_min_height = 800, 500
WHITE_COLOUR = "#FFFFFF"
DEFAULT_COLOUR = "#2B2B2B"
BUTTON_FG_COLOUR = "#3B3B3B"
FILE_MENU_COLOUR = "#144870"


class Window:
    def __init__(self):
        self.is_possible_to_export = False
        self.events_path = Path(EVENTS_PATH)
        self.incoming_path = Path(INCOMING_PATH)
        self.root = None
        self.languages = {}
        self.language_index = 0
        self.language = LANGUAGES[DEFAULT_LANGUAGE_INDEX]
        self.menu = None
        self.file_menu = None

        self.table = None
        self.file1_btn = None
        self.file2_btn = None
        self.calculate_btn = None
        self.student_info = None

        self.path1 = None
        self.path2 = None

        self.left_frame = None
        self.right_frame = None

        self.fio_label = None
        self.fio_info = None
        self.emails_label = None
        self.emails_info = None
        self.numbers_label = None
        self.numbers_info = None
        self.dislocation_label = None
        self.dislocation_info = None
        self.edu_program_label = None
        self.edu_program_info = None

        self.load_languages()
        self.init_root()
        self.init_menu()

        self.students = []
        self.intersection_list = []
        self.students_var = tk.Variable(value=self.students)

        self.init_widgets()

    def load_languages(self):
        for language in LANGUAGES:
            for file_name in LANGUAGES_FILES:
                text_path = language_template.format(language=language, file_name=file_name)
                data_folder = Path(text_path)
                with open(data_folder, "r", encoding="utf-8") as file:
                    if language not in self.languages:
                        self.languages[language] = {}
                    self.languages[language].update(**json.load(file))

    def init_root(self):
        self.root = ctk.CTk()
        self.root.geometry("{}x{}".format(window_min_width, window_min_height))
        self.root.resizable(True, True)
        self.root.minsize(window_min_width, window_min_height)
        self.root.configure(background=DEFAULT_COLOUR, bg=DEFAULT_COLOUR)

    def init_widgets(self):
        self.root.title(self.languages[self.language]["title"])
        # в левом верхнем углу располагается таблица с данными она занимает  2/3 ширины и 2/3 высоты
        # в левом нижнем углу располагаются 3 кнопки: файл1, файл2, посчитать

        for c in range(5):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.root.rowconfigure(index=r, weight=1)

        self.init_left_frame()
        self.init_right_frame()
        self.root.grid_propagate(False)
        self.root.configure(background=DEFAULT_COLOUR, bg=DEFAULT_COLOUR)

    def __init_binds(self):
        self.root.bind("<Control-e>", self.export_func)

    def init_left_frame(self):
        self.left_frame = ctk.CTkFrame(self.root)

        for c in range(3):
            self.left_frame.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.left_frame.rowconfigure(index=r, weight=1)

        self.left_frame.grid(row=0, column=0, columnspan=3, rowspan=4, sticky="news")

        self.table = tk.Listbox(self.left_frame, listvariable=self.students_var, background="#2A2A2A", borderwidth=0,
                                highlightthickness=0, foreground=WHITE_COLOUR)
        self.table.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="news")
        self.table.bind("<<ListboxSelect>>", self.student_selected)

        self.file1_btn = ctk.CTkButton(self.left_frame, text=self.languages[self.language]["file1"],
                                       command=self.get_path1, fg_color=BUTTON_FG_COLOUR, bg_color=DEFAULT_COLOUR)
        self.file1_btn.grid(row=3, column=0, sticky="news")

        self.file2_btn = ctk.CTkButton(self.left_frame, text=self.languages[self.language]["file2"],
                                       command=self.get_path2, fg_color=BUTTON_FG_COLOUR, bg_color=DEFAULT_COLOUR)
        self.file2_btn.grid(row=3, column=1, sticky="news")

        self.calculate_btn = ctk.CTkButton(self.left_frame,
                                           text=self.languages[self.language]["intersection"],
                                           command=self.calculate, fg_color=BUTTON_FG_COLOUR,
                                           bg_color=DEFAULT_COLOUR)
        self.calculate_btn.grid(row=3, column=2, sticky="news")
        self.left_frame.grid_propagate(False)

    def init_right_frame(self):
        self.right_frame = ctk.CTkFrame(self.root, bg_color=DEFAULT_COLOUR, fg_color=DEFAULT_COLOUR)
        self.right_frame.grid(row=0, column=3, columnspan=4, rowspan=4, sticky="news")
        labels_names = ["fio_label", "fio_info", "emails_label", "emails_info", "numbers_label", "numbers_info",
                        "dislocation_label", "dislocation_info", "edu_program_label", "edu_program_info"]
        labels_keys = ["fio", "emails", "numbers", "dislocation", "edu_program"]
        for i in range(0, len(labels_names), 2):
            label_lbl = tk.Label(self.right_frame, text="\n" + self.languages[self.language][labels_keys[i >> 1]],
                                 background=DEFAULT_COLOUR,
                                 foreground=WHITE_COLOUR, anchor="center", justify="center")
            info_lbl = tk.Label(self.right_frame, text="-",
                                background=DEFAULT_COLOUR,
                                foreground=WHITE_COLOUR, anchor="center", justify="center")
            setattr(self, labels_names[i], label_lbl)
            setattr(self, labels_names[i + 1], info_lbl)

            a = getattr(self, labels_names[i])
            a.pack_propagate(0)
            a.pack()
            a.grid_propagate(False)

            a = getattr(self, labels_names[i + 1])
            a.pack_propagate(0)
            a.pack()
            a.grid_propagate(False)
        self.right_frame.grid_propagate(False)

    def init_menu(self):
        self.menu = tk.Menu(self.root, background=DEFAULT_COLOUR, borderwidth=0, activeforeground=WHITE_COLOUR,
                            foreground=WHITE_COLOUR)
        self.root.configure(menu=self.menu, background=DEFAULT_COLOUR, bg=DEFAULT_COLOUR)
        # self.menu = ctk.CTkOptionMenu(self.root)
        self.file_menu = tk.Menu(self.menu, tearoff=0, background=DEFAULT_COLOUR, activeforeground=WHITE_COLOUR,
                                 foreground=WHITE_COLOUR)
        self.file_menu.add_command(label=self.languages[self.language]["export"],
                                   command=self.export_func, background=DEFAULT_COLOUR,
                                   activebackground=FILE_MENU_COLOUR)
        self.file_menu.add_command(label=self.languages[self.language]["switch_language"], command=self.switch_language,
                                   background=DEFAULT_COLOUR, activebackground=FILE_MENU_COLOUR)
        self.menu.configure(activebackground=FILE_MENU_COLOUR)
        self.menu.add_cascade(label=self.languages[self.language]["settings"], menu=self.file_menu)

    def mainloop(self):
        self.root.mainloop()

    def switch_language(self):
        self.language_index = (self.language_index + 1) % len(LANGUAGES)
        self.language = LANGUAGES[self.language_index]
        self.init_menu()
        self.init_widgets()

    def student_selected(self, evt):
        w = evt.widget
        try:
            index = int(w.curselection()[0])
        except IndexError:
            return
        self.set_student_info(self.intersection_list[index])

    def set_student_info(self, student):
        NEW_LINE = "\n"
        self.fio_info.configure(text=student.fio)
        self.emails_info.configure(text=f'{NEW_LINE}'.join(student.email_list) if len(student.email_list) != 0 else '-')
        self.numbers_info.configure(
            text=f'{NEW_LINE}'.join(student.number_list) if len(student.number_list) != 0 else '-')
        self.dislocation_info.configure(
            text=student.dislocation if ((student.dislocation is not None) and (student.dislocation != '')) else '-')
        self.edu_program_info.configure(text=f'{NEW_LINE}'.join(
            [Student.edu_program_value_to_ru(x) for x in student.educational_program_list]) if len(
            student.educational_program_list) != 0 else '-')

    def load_students(self, intersection_list):
        self.students = []
        self.intersection_list = intersection_list
        for i, student in enumerate(intersection_list, start=1):
            self.students.append(f"{'%3d' % i}. {student.fio}")
        self.students_var.set(self.students)

    def get_path1(self):
        self.path1 = ButtonFunc.choose_file(self.languages[self.language]["load_file1"], ".xlsx")
        if self.path1 is not None:
            self.path1 = self.path1.name
            self.file1_btn.configure(text=self.languages[self.language]["file_chosen"])

    def get_path2(self):
        self.path2 = ButtonFunc.choose_file(self.languages[self.language]["load_file2"], ".xlsx")
        if self.path2 is not None:
            self.path2 = self.path2.name
            self.file2_btn.configure(text=self.languages[self.language]["file_chosen"])

    def calculate(self):
        thread = threading.Thread(target=self.thread_calculate)
        thread.start()

    def thread_calculate(self):
        self.is_possible_to_export = False
        lst = ButtonFunc.intersection(self.path1, self.path2, self.language, self.languages, self.calculate_btn,
                                      self.events_path, self.incoming_path)
        if lst is None:
            return
        self.load_students(lst)
        self.reinit_file_buttons()
        self.is_possible_to_export = True

    def reinit_file_buttons(self):
        self.path1 = None
        self.path2 = None
        self.file1_btn.configure(text=self.languages[self.language]["file1"])
        self.file2_btn.configure(text=self.languages[self.language]["file2"])
        self.calculate_btn.configure(text=self.languages[self.language]["intersection"])

    def export_func(self, *kwargs):
        if not self.is_possible_to_export:
            ButtonFunc.create_message_box(self.languages[self.language]["cant_export_title"],
                                          self.languages[self.language]["cant_export_text"])
        else:
            ButtonFunc.convert_to_excel(self.intersection_list, self.language, self.languages)
