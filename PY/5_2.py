class Person():
    def __init__(self,name,age,address) -> None:
        self.name=name
        self.age=age
        self.address=address
    def eat(self):
        print("i can eat")
    def speak(self):
        print("i can speak")
   


class Teacher(Person):
    def __init__(self,name,age,address) -> None:
        self.name=name
        self.age=age
        self.address=address

    def eat(self):
        print("i can eat")
    def speak(self):
        print("i can speak")
    def __write(self):
        print("i can write")

class Student(Person):
    pass


class B(object):
    pass  # 这里自己写需要的方法

class A(B):
    pass

# p=Person('tom',18,'henan')
# teacher=Teacher('tom',28,'anhui')
# s1=Student('amy',17,'henan')
# s1.eat()
# s1.speak()
a=A()


