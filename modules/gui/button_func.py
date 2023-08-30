from pathlib import Path
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from .calculator.comparator import Comparator
from .calculator.excel_converter import ExcelConverter
from .calculator.database.student_database import StudentsDatabase


class ButtonFunc:
    def __init__(self):
        pass

    @staticmethod
    def convert_to_excel(intersection_list, language, languages):
        path = ButtonFunc.choose_file_to_save()
        try:
            path = Path(path.name)
        except Exception:
            path = None
        if path == "" or path is None or path == ():
            mb.showwarning(languages[language]["file_not_chosen"], languages[language]["file_not_chosen"])
            return None
        ExcelConverter.convert_to_excel(
            path, intersection_list,
            language, languages)
        mb.showinfo(languages[language]["export_finished"], languages[language]["export_finished"])

    @staticmethod
    def choose_file(title, extension):
        result = fd.askopenfile(title=title, defaultextension=extension)
        if result == "" or result is None or result == ():
            return None
        return result

    @staticmethod
    def choose_file_to_save(confirmoverwrite=True, defaultextension=".xlsx"):
        result = fd.asksaveasfile(confirmoverwrite=confirmoverwrite, defaultextension=defaultextension)
        if result is None:
            return None
        return result

    @staticmethod
    def intersection(path1, path2, language, languages,
                     calculate_button, data_path1, incoming_path2):
        if path1 is None or path2 is None:
            mb.showwarning(languages[language]["file_not_chosen"], languages[language]["file_not_chosen"])
            return None
        calculate_button.configure(text=languages[language]["calculating"], state="disabled")
        StudentsDatabase.save_data(path1, data_path1)
        StudentsDatabase.save_data(path2, incoming_path2)

        result = Comparator.intersection(data_path1, incoming_path2)
        calculate_button.configure(state="normal", text=languages[language]["intersection"])
        return result

    @staticmethod
    def create_message_box(title, text):
        mb.showwarning(title, text)
