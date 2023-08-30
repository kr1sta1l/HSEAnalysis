from enum import Enum


class StudentKeywords(Enum):
    FIO = "fio"
    NAME = "name"
    SURNAME = "surname"
    PATRONYMIC = "patronymic"
    STATUS = "status"
    EMAIL = "email"
    NUMBER = "number"
    DISLOCATION = "dislocation"
    SCHOOL = "school"
    POST = "post"
    HOW_KNOW = "how_know"
    EDUCATIONAL_PROGRAM = "educational_program"
    LIST_OF_COURSES = "list_of_courses"
    MENTIONS = "mentions"
    SHEET = "sheet"
    WORKBOOK = "workbook"
    ROW = "row"


class StudentStatus(Enum):
    SCHOOLBOY = 1
    STUDENT = 2
    PARENT = 3
    ANOTHER = 4


students_keywords = {
    StudentKeywords.FIO: ['|фио|', '|ученика|', '|фио|участника|'],
    StudentKeywords.NAME: ['|имя|', '|имя|ученика|', '|имя|участника|'],
    StudentKeywords.SURNAME: ['|фамилия|', '|фамилия|ученика|', '|фамилия|участника|'],
    StudentKeywords.PATRONYMIC: ['|отчество|', '|отчество|ученика|', '|отчество|участника|'],
    StudentKeywords.STATUS: ['|статус|', '|статус|ученика|', '|статус|участника|', '|ваш|статус|',
                             '|кем|вы|являетесь|'],
    StudentKeywords.EMAIL: ['|почта|', '|почта|ученика|', '|почта|участника|', '|email|', '|e-mail|'],
    StudentKeywords.NUMBER: ['|номер|', '|номер|ученика|', '|номер|участника|', '|телефон|', '|телефон|ученика|',
                             '|телефон|участника|'],
    StudentKeywords.DISLOCATION: ['|место|проживания|', '|город|', '|страна|', '|проживания|'],
    StudentKeywords.SCHOOL: ['|школа|', '|учебы|', '|школы|'],
    StudentKeywords.POST: ['|должность|', '|класс|'],
    StudentKeywords.HOW_KNOW: ['|узнали о|', '|как|узнали|', '|узнали|'],
    StudentKeywords.EDUCATIONAL_PROGRAM: ['|образовательная|программа|', '|программа|', '|интересующая|Оп|',
                                          '|интересующая|программа|',
                                          '|оп|', '|консультации|', '|консультация|', '|консультации|программы|'],
    # StudentKeywords.LIST_OF_COURSES: ['консультации', 'консультация']
}

students_banned_keywords = {
    StudentKeywords.FIO: ['сопровождающего'],
    StudentKeywords.NAME: ['сопровождающего', 'в чате'],
    StudentKeywords.SURNAME: ['сопровождающего'],
    StudentKeywords.PATRONYMIC: ['сопровождающего']
}


class TrainingPrograms(Enum):
    PMI = "PMI"
    PI = "PI"
    PAD = "PAD"
    KNAD = "KNAD"
    EAD = "EAD"
    ONE_OF_THEM = "ONE_OF_THEM"


doesnt_want_to_visit = ["|не|заинтересован|",
                        "|не|заинтересован|в|поступлении|на|эту|образовательную|программу|"]

training_programs_keywords = {TrainingPrograms.PMI: ['пми', 'прикладная|математика|и|информатика'],
                              TrainingPrograms.PI: ['пи', 'программная|инженерия'],
                              TrainingPrograms.PI: ['пи', 'программная|инженерия'],
                              TrainingPrograms.PAD: ['пад', 'прикладной|анализ|данных'],
                              TrainingPrograms.KNAD: ['кнад', 'компьютерные|науки|и|анализ|данных'],
                              TrainingPrograms.EAD: ['эад', 'экономика|и|анализ|данных']
                              }

parents_keywords = ["родительское|собрание", "родительское"]

student_status_keywords = {StudentStatus.SCHOOLBOY: ['школьник', 'школьница', 'абитуриент'],
                           StudentStatus.STUDENT: ['студент', 'студентка'],
                           StudentStatus.PARENT: ['родитель', 'мама', 'папа', 'родители']
                           }
