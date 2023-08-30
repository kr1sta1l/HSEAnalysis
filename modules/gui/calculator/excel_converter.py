from modules.gui.calculator.database.student import Student
from .database.keywords.keywords import StudentKeywords
import openpyxl


class ExcelConverter:
    def __init__(self):
        pass

    @staticmethod
    def convert_to_excel(path, students, language,
                         translation):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = translation[language]["students_sheet"]

        ExcelConverter.write_row(ws, 1, 1, ExcelConverter.create_first_line(language, translation))
        for i, student in enumerate(students, start=2):
            try:
                ExcelConverter.write_row(ws, i, 1, ExcelConverter.student_to_list(student))
            except Exception:
                continue

        wb.save(path)

    @staticmethod
    def create_first_line(language, translation):
        result = []
        language_keys = translation[language]
        columns_keys = ["fio", "emails", "numbers", "dislocation", "school", "how_know", "educational", "mentions"]
        for column_key in columns_keys:
            result.append(language_keys[column_key])
        return result

    @staticmethod
    def student_to_list(student):
        result = [
            student.fio,
            ExcelConverter.str_list_to_string(student.email_list),
            ExcelConverter.str_list_to_string(student.number_list),
            student.dislocation if student.dislocation is not None else "",
            student.school if student.school is not None else "",
            ExcelConverter.str_list_to_string(student.how_know_list),
            ExcelConverter.str_list_to_string(
                [Student.edu_program_value_to_ru(x) for x in student.educational_program_list]),
            ExcelConverter.student_mentions_to_sting(student.mentions)
        ]

        return result

    @staticmethod
    def str_list_to_string(lst):
        if lst is not None:
            string = ", ".join(lst)
        else:
            string = ""
        return string

    @staticmethod
    def student_mentions_to_sting(student_mentions):
        result = []
        for mention in student_mentions:
            result.append(
                f"{mention[StudentKeywords.WORKBOOK]}, {mention[StudentKeywords.SHEET]}, {mention[StudentKeywords.ROW]}")
        return ";\n".join(result)

    @staticmethod
    def write_row(write_sheet, row_num, starting_column, write_values):
        if isinstance(starting_column, str):
            starting_column = ord(starting_column.lower()) - 96
        for i, value in enumerate(write_values):
            write_sheet.cell(row_num, starting_column + i, value)
