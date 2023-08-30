from .database.student_database import StudentsDatabase
from .database.student import Student
from .database.keywords.keywords import StudentKeywords


class Comparator:
    def __init__(self):
        pass

    @staticmethod
    def intersection(events_path, students_path):
        result = []
        events_db = StudentsDatabase(events_path)
        students_db = StudentsDatabase(students_path)

        events_list = events_db.get_all()
        students_list = students_db.get_all()
        k = 0

        for student in students_list:
            student_index = Comparator.is_student_in_events_list(student, events_list)
            if student_index != -1:
                try:
                    k += 1
                    student = Student(Comparator.dict_string_to_student_keywords(student))
                    prev_student = Student(Comparator.dict_string_to_student_keywords(events_list[student_index]))
                    Comparator.transfer_student_data(student, prev_student)
                    result.append(student)
                except Exception:
                    continue

        return result

    @staticmethod
    def transfer_student_data(student1, student2):
        """
        Transfer data from student2 to student1
        :param student1:
        :param student2:
        :return:
        """
        if student1.email_list is None:
            student1.email_list = []
        if student2.email_list is not None:
            for email in student2.email_list:
                student1.email_list.append(email)
            student1.email_list = [x for x in student1.email_list if x != ""]
            student1.email_list = list(set(student1.email_list))

        if student1.number_list is None:
            student1.number_list = []
        if student2.number_list is not None:
            for number in student2.number_list:
                student1.number_list.append(number)
            student1.number_list = list(set(student1.number_list))
            student1.number_list = [x for x in student1.number_list if x != ""]
        if student2.dislocation is not None:
            student1.dislocation = student2.dislocation
        if student1.mentions is None:
            student1.mentions = []
        if student2.mentions is not None:
            student1.mentions += student2.mentions

        if student2 is not None:
            student1.how_know_list += student2.how_know_list
            a = [x.split(";") for x in student1.how_know_list if x != ""]
            student1.how_know_list = []
            for el in a:
                for x in el:
                    student1.how_know_list.append(x.strip().lower())
            student1.how_know_list = list(set(student1.how_know_list))

    @staticmethod
    def dict_string_to_student_keywords(db_dict):
        dct = {
            "fio": StudentKeywords.FIO, "status": StudentKeywords.STATUS, "emails": StudentKeywords.EMAIL,
            "numbers": StudentKeywords.NUMBER, "dislocation": StudentKeywords.DISLOCATION,
            "school": StudentKeywords.SCHOOL, "post": StudentKeywords.POST, "how_know": StudentKeywords.HOW_KNOW,
            "educational_program": StudentKeywords.EDUCATIONAL_PROGRAM,
            "courses": StudentKeywords.LIST_OF_COURSES,
            "list_of_courses": StudentKeywords.LIST_OF_COURSES, "mentions": StudentKeywords.MENTIONS
        }
        list_keywords = [StudentKeywords.EMAIL, StudentKeywords.NUMBER, StudentKeywords.HOW_KNOW,
                         StudentKeywords.EDUCATIONAL_PROGRAM, StudentKeywords.LIST_OF_COURSES]
        result_dict = {}
        db_dict = dict(db_dict)
        for key in db_dict:
            if key in dct:
                student_key = dct[key]
                result_dict[student_key] = db_dict[key]
                if student_key in list_keywords:
                    result_dict[student_key] = result_dict[student_key].split("|")
                elif student_key == StudentKeywords.MENTIONS:
                    result_dict[student_key] = Comparator.mentions_to_list(result_dict[student_key])
        return result_dict

    @staticmethod
    def mentions_to_list(mentions):
        result_mention_list = []
        mention_dict_helper = mentions.split("||")

        for i in range(len(mention_dict_helper)):
            mention_dict = {}
            mention_dict_helper[i] = mention_dict_helper[i].split("|")
            mention_dict[StudentKeywords.SHEET] = mention_dict_helper[i][0]
            mention_dict[StudentKeywords.WORKBOOK] = mention_dict_helper[i][1]
            mention_dict[StudentKeywords.ROW] = int(mention_dict_helper[i][2])
            result_mention_list.append(mention_dict)
        return result_mention_list

    @staticmethod
    def is_student_in_events_list(student, events_list):
        student_emails = Comparator.convert_emails_to_list(student["emails"])
        student_fio = student["fio"].strip()
        for i, event_student in enumerate(events_list):
            if event_student["fio"].strip() == student_fio:
                return i
            if event_student["emails"] is not None:
                for email in Comparator.convert_emails_to_list(event_student["emails"]):
                    if email in student_emails:
                        return i
        return -1

    @staticmethod
    def convert_emails_to_list(emails):
        emails = emails.strip()
        emails = emails.split()
        if len(emails) == 1:
            emails = emails[0].split("|")
        return emails
