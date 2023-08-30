from .keywords.keywords import StudentKeywords
from .keywords.keywords import training_programs_keywords


class Student:
    def __init__(self, characteristics):
        self.fio = ""
        self.status = None
        self.email_list = None
        self.number_list = None
        self.dislocation = None
        self.school = None
        self.post = None
        self.how_know_list = None
        self.educational_program_list = None
        self.courses_list = None
        self.mentions = None

        self.__init_fio(characteristics)
        self.__init_attr("status", StudentKeywords.STATUS, characteristics)
        self.__init_attr_list("email_list", StudentKeywords.EMAIL, characteristics, is_lower=True)
        self.__init_attr_list("number_list", StudentKeywords.NUMBER, characteristics)
        self.__init_attr("dislocation", StudentKeywords.DISLOCATION, characteristics)
        self.__init_attr("school", StudentKeywords.SCHOOL, characteristics)
        self.__init_attr("post", StudentKeywords.POST, characteristics)
        self.__init_attr_list("how_know_list", StudentKeywords.HOW_KNOW, characteristics)
        self.__init_attr_list("educational_program_list", StudentKeywords.EDUCATIONAL_PROGRAM, characteristics)
        self.__init_attr_list("courses_list", StudentKeywords.LIST_OF_COURSES, characteristics)
        self.__init_mentions(characteristics)

    def __init_fio(self, characteristics):
        if StudentKeywords.FIO in characteristics or StudentKeywords.NAME in characteristics or \
                StudentKeywords.SURNAME in characteristics or StudentKeywords.PATRONYMIC in characteristics:
            try:
                self.fio = characteristics[StudentKeywords.FIO]
            except KeyError:
                lst = [StudentKeywords.NAME, StudentKeywords.SURNAME, StudentKeywords.PATRONYMIC]
                self.fio = ""
                for el in lst:
                    if el in characteristics:
                        self.fio += f"{characteristics[el]} "
                self.fio = self.fio.strip()
        else:
            raise KeyError
        if self.fio is not None:
            self.fio = self.fio.strip().replace("'", '"')
        else:
            self.fio = ""

    def __init_mentions(self, characteristics):
        if StudentKeywords.MENTIONS in characteristics:
            self.mentions = characteristics[StudentKeywords.MENTIONS]
        else:
            self.mentions = None

    def __init_attr_list(self, attribute, keyword, characteristics,
                         is_lower = False):
        value = None
        if keyword in characteristics:
            if type(characteristics[keyword]) == list:
                value = characteristics[keyword]
            else:
                if characteristics[keyword] is not None:
                    value = [characteristics[keyword]]
        if value is not None:
            for i in range(len(value)):
                try:
                    value[i] = value[i].strip().replace("'", '"')
                    value[i] = value[i].lower() if is_lower else value[i]
                except AttributeError:
                    pass
        setattr(self, attribute, value)

    def __init_attr(self, attribute, keyword, characteristics):
        value = None
        if keyword in characteristics:
            if keyword == StudentKeywords.DISLOCATION and characteristics[keyword] == "None":
                pass
            value = characteristics[keyword]
        try:
            value = value.strip().replace("'", '"')
        except AttributeError:
            pass
        setattr(self, attribute, value)

    def to_json(self):
        return {
            "fio": self.fio, "status": self.status,
            "email": self.email_list, "number": self.number_list,
            "dislocation": self.dislocation, "school": self.school,
            "post": self.post, "how_know": self.how_know_list,
            "educational_program": self.educational_program_list,
            "list_of_courses": self.courses_list, "mentions": self.mentions
        }

    def join(self, student):
        if self.fio != student.fio:
            raise ValueError("FIO mismatch")
        for attr in self.__dict__:
            if getattr(self, attr) is None:
                setattr(self, attr, getattr(student, attr))
            elif getattr(student, attr) is not None:
                if type(getattr(self, attr)) == list:
                    getattr(self, attr).extend(getattr(student, attr))
                elif type(getattr(self, attr)) == dict:
                    getattr(self, attr).update(getattr(student, attr))

    def delete_repetitive(self):
        for attr in self.__dict__:
            attr_value = getattr(self, attr)
            if attr_value is None:
                continue
            try:
                for i in range(len(attr_value)):
                    if type(attr_value[i]) is str:
                        attr_value[i] = attr_value[i].lower().title()
            except Exception:
                continue

            try:
                attr_value = list(set(attr_value))
            except TypeError:
                pass

            for el in attr_value:
                if el == "" or el is None:
                    attr_value.remove(el)
            if len(attr_value) == 0:
                attr_value = None
            setattr(self, attr, attr_value)

    def mentions_to_list(self):
        if self.mentions is None:
            return ''
        lst = []
        for el in self.mentions:
            lst.append(f"{el[StudentKeywords.SHEET]}|{el[StudentKeywords.WORKBOOK]}|{el[StudentKeywords.ROW]}")
        return lst

    def educational_program_to_list(self):
        result = []
        for el in self.educational_program_list:
            result.append(el.value)
        return result

    @staticmethod
    def edu_program_value_to_ru(edu_program):
        for key in training_programs_keywords:
            if key.value.lower() == edu_program.lower():
                return training_programs_keywords[key][0].replace("|", "").upper()

    def to_sql(self):
        return f"('{self.fio}', '{self.status.value}', " \
               f"'{'|'.join(self.email_list) if self.email_list is not None else ''}', " \
               f"'{'|'.join(self.number_list) if self.number_list is not None else ''}', " \
               f"'{self.dislocation if self.dislocation is not None else ''}', " \
               f"'{self.school if self.school is not None else ''}', " \
               f"'{self.post if self.post is not None else ''}', " \
               f"'{'|'.join(self.how_know_list) if self.how_know_list is not None else ''}', " \
               f"'{'|'.join(self.educational_program_to_list()) if self.educational_program_list is not None else ''}', " \
               f"'{'|'.join(self.courses_list) if self.courses_list is not None else ''}', " \
               f"'{'||'.join(self.mentions_to_list())}')"
