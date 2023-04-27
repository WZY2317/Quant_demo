class Parent:
    ParentAttr = 100

    def __init__(self) -> None:
        print("父类的构造函数")

    def parentMethod(self):
        print("调用父类的方法")

    def myMethod(self):
        print('调用父类方法')

    def setAttr(self, attr):
        Parent.ParentAttr = attr

    def getAttr(self):
        print("父类属性", Parent.parentAttr)


class Child(Parent):

    def __init__(self) -> None:
        super().__init__()
        print("调用子类构造方法")

    def childMethod(self):
        print('调用子类方法')

    def myMethod(self):
        print('调用子类的方法')


class Animal(object):

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def call(self):
        print(self.name, "会叫")


class cat(Animal):

    def __init__(self, name, age, sex) -> None:
        super(cat, self).__init__(name, age)
        self.sex = sex

    def call(self):
        print(self.name, '喵喵')


class dog(Animal):

    def __init__(self, name, age, sex) -> None:
        super(dog, self).__init__(name, age)
        self.sex = sex

    def call(self):
        print(self.name, '汪汪')


def do(all):
    all.call()


# c = Child()
# c.parentMethod()
# c.setAttr(200)
# c.getAttr()

A = Animal('小黑', 3)
C = cat("tom", 3, "女")
D = dog("旺财", 4, '男')

for x in (A, C, D):
    do(x)
