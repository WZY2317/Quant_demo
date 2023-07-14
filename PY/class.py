class student(object):
    __age = 0
    __num = 0
    name = None
    classroom = '102'
    head = "tttt"

    def __init__(self, age, num, name) -> None:
        self.__age = age
        self.__num = num
        self.name = name

    def __ahead(self) -> None:
        print(self.head)

    @classmethod
    def disPlaySchool(cls):
        cls.__ahead(cls)
        print("henu")

    @staticmethod
    def showname():

        print(student.classroom)


tom = student(11, 11, "tom")
# tom.__ahead()
student.disPlaySchool()
tom.disPlaySchool

student.showname()
print(student.__dict__)
print(student.__doc__)
print(student.name)
