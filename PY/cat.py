class Car(object):
    def __init__(self,brand) -> None:
        self.brand=brand
    def run(self):
        print('i can run')
    
class GasolineCar(Car):
    def __init__(self, brand) -> None:
        super().__init__(brand)
    def run(self):
        super.run()
        print('i can run with gas')
    
class EletricCar(Car):
    def __init__(self, brand) -> None:
        super().__init__(brand)
        self.battery=70

    def run(self):
        print('i can run with ele')


def service(obj):
    obj.run()

bmw=GasolineCar('宝马')
# bmw.run()
tesla=EletricCar('特斯拉')
# tesla.run()
service(bmw)
service(tesla)