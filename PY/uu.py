class Animals:
    def eat(self):
        print('i can eat')
    def call(self):
        print('i can call')


class Dog(Animals):
    def eat(self):
        print('i like fork')
    def subEat(self):
        super.eat()
class Cat(Animals):
    def eat(self):
        print('like fish')




Dg=Dog()
Dg.subEat()


