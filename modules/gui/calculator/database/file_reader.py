import openpyxl as op
from .keywords.keywords import students_keywords
from .keywords.keywords import training_programs_keywords
from .keywords.keywords import StudentKeywords
from .keywords.keywords import doesnt_want_to_visit
from .keywords.keywords import TrainingPrograms
from .keywords.keywords import student_status_keywords
from .keywords.keywords import StudentStatus
from .student import Student


class FileReader:
    def __init__(self, path, students_keywords,
                 training_programs_keywords, students_banned_keywords):
        self.path = path
        self.wb = op.load_workbook(self.path)
        self.students_keywords = students_keywords
        self.training_programs_keywords = training_programs_keywords
        self.students_banned_keywords = students_banned_keywords

    @staticmethod
    def create_association(line, keywords, training_programs_keywords, students_banned_keywords):
        """
        Создает словарь, где ключ - это название характеристики, а значение - это значение характеристики
        :param line: Строка из файла
        :param keywords: Словарь с ключевыми словами
        :param training_programs_keywords:
        :return: Словарь
        """
        association = {}
        flag2 = False
        for i, column in enumerate(line):
            flag = False

            if column is None:
                continue
            column_text = "|" + column.lower().replace(" ", "|") + "|"
            for key in keywords:
                for word in keywords[key]:
                    if word.lower() in column_text:
                        if key != StudentKeywords.EDUCATIONAL_PROGRAM:
                            doesnt_consists_banned_words = True
                            if key in students_banned_keywords:
                                for banned_keyword in students_banned_keywords[key]:
                                    if banned_keyword in column_text:
                                        doesnt_consists_banned_words = False
                            if doesnt_consists_banned_words:
                                association[i] = key
                        else:
                            for program in training_programs_keywords:
                                for program_translation in training_programs_keywords[program]:
                                    if program_translation in column_text:
                                        association[i] = program
                                        flag2 = True
                            if not flag2:
                                association[i] = TrainingPrograms.ONE_OF_THEM
                        flag = True
                        break
                if flag:
                    break
        return association

    @staticmethod
    def educational_program_prettify(data):
        lst = []
        for program in TrainingPrograms:
            if program in data:
                if program == TrainingPrograms.ONE_OF_THEM:
                    try:
                        value = "|" + data[program].strip().lower().split(" ", "|") + "|"
                    except AttributeError:
                        lst.append(TrainingPrograms.ONE_OF_THEM)
                        continue
                    for prog in training_programs_keywords:
                        if value in training_programs_keywords[program]:
                            lst.append(prog)
                elif data[program] is True:
                    lst.append(program)
        return lst

    def data_prettify(self, data):
        """
        Приводит данные к единому виду
        :param data: Данные
        :return: Приведенные данные
        """
        if StudentKeywords.DISLOCATION in data and data[StudentKeywords.DISLOCATION] == "None":
            pass
        data[StudentKeywords.FIO] = self.fio_prettify(data)
        try:
            del data[StudentKeywords.NAME]
            del data[StudentKeywords.SURNAME]
            del data[StudentKeywords.PATRONYMIC]
        except KeyError:
            pass
        if StudentKeywords.NUMBER in data:
            data[StudentKeywords.NUMBER] = self.number_prettify(str(data[StudentKeywords.NUMBER]))
        for OP in TrainingPrograms:
            if OP in data:
                if OP != TrainingPrograms.ONE_OF_THEM:
                    data[OP] = self.visit_prettify(data[OP])
                else:
                    result = self.transfer_visit(data[OP])
                    del data[OP]
                    data[result] = True
        if StudentKeywords.STATUS in data:
            data[StudentKeywords.STATUS] = self.status_prettify(data[StudentKeywords.STATUS])
        else:
            data[StudentKeywords.STATUS] = StudentStatus.ANOTHER
        data[StudentKeywords.EDUCATIONAL_PROGRAM] = self.educational_program_prettify(data)
        return data

    @staticmethod
    def number_prettify(number):
        """
        Приводит номер телефона к единому виду
        :param number: Номер телефона
        :return: Приведенный номер телефона
        """
        if number is None or number == "None":
            return None
        number = number.strip()
        number = number.split(".")[0]
        number = number.replace(" ", "")
        number = number.replace("-", "").replace("(", "").replace(")", "").replace("=", "").replace("+", "")
        if len(number) == 0:
            return None
        if number[0] == "8":
            number = "+7" + number[1:]
        elif number[0] == "7":
            number = "+" + number
        else:
            number = "+7" + number

        return number

    @staticmethod
    def visit_prettify(want_to_visit):
        """
        Приводит хочет ли посетить к единому виду
        :param want_to_visit: Хочет ли посетить
        :return: Приведенное хочет ли посетить
        """
        if want_to_visit is None:
            return False
        want_to_visit = "|" + want_to_visit.lower().replace(" ", "|") + "|"
        for word in doesnt_want_to_visit:
            if word in want_to_visit:
                return False
        return True

    @staticmethod
    def status_prettify(status):
        """
        Приводит статус к единому виду
        :param status: Статус
        :return: Приведенный статус
        """
        if status is None or type(status) != str:
            return StudentStatus.ANOTHER
        status = status.lower().replace(" ", "|")
        for key in student_status_keywords:
            if status in student_status_keywords[key]:
                return key
        return StudentStatus.ANOTHER

    @staticmethod
    def transfer_visit(what_want_to_visit):
        if what_want_to_visit is None:
            return TrainingPrograms.ONE_OF_THEM
        what_want_to_visit = what_want_to_visit.lower().replace(" ", "|")
        for training_program in training_programs_keywords:
            if what_want_to_visit in training_programs_keywords[training_program]:
                return training_program

    @staticmethod
    def fio_prettify(data):
        """
        Приводит ФИО к единому виду
        :param data:
        :return: Приведенное ФИО
        """
        if StudentKeywords.FIO in data:
            return data[StudentKeywords.FIO]
        result = []
        if (StudentKeywords.SURNAME in data) and (data[StudentKeywords.SURNAME] is not None) and (
                type(data[StudentKeywords.SURNAME]) == str):
            result.append(data[StudentKeywords.SURNAME])
        if (StudentKeywords.NAME in data) and (data[StudentKeywords.NAME] is not None) and (
                type(data[StudentKeywords.NAME]) == str):
            result.append(data[StudentKeywords.NAME])
        if (StudentKeywords.PATRONYMIC in data) and (data[StudentKeywords.PATRONYMIC] is not None) and (
                type(data[StudentKeywords.PATRONYMIC]) == str):
            result.append(data[StudentKeywords.PATRONYMIC])
        return " ".join(result)

    def read_workbook(self, path, slovar):
        self.path = path
        association = {}
        for sheet in self.wb:
            counter = 0
            for i, row in enumerate(sheet.iter_rows()):
                if i == 0:
                    association = self.create_association([cell.value for cell in row], students_keywords,
                                                          self.training_programs_keywords,
                                                          self.students_banned_keywords)
                    if len(association) == 0:
                        break
                    continue

                if counter == 5:
                    break
                if row[0].value is None:
                    counter += 1
                    continue
                else:
                    counter = 0

                characteristics = {}

                for key in association:
                    if row[key].value is not None:
                        characteristics[association[key]] = str(row[key].value)
                    else:
                        characteristics[association[key]] = None
                characteristics[StudentKeywords.MENTIONS] = [{
                    StudentKeywords.SHEET: sheet.title,
                    StudentKeywords.WORKBOOK: self.path,
                    StudentKeywords.ROW: i + 1
                }]
                characteristics = self.data_prettify(characteristics)
                student = Student(characteristics)
                code = student.fio
                if code in slovar:
                    slovar[code].append(student)
                else:
                    slovar[code] = [student]
        return slovar

    @staticmethod
    def join_repetitions(data):
        for key in data:
            if len(data[key]) == 1:
                continue
            for i in range(1, len(data[key])):
                data[key][0].join(data[key][i])
            data[key] = [data[key][0]]
            data[key][0].delete_repetitive()
