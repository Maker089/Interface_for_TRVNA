class Car():
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometry = 0

    def description_name(self):
        desc = str(self.year)+ ' ' + self.make + " " + self.model
        return desc

    def read_odometry(self):
        print("probeg awto" + str(self.odometry) + "km" )

    def update_odometry(self, km):
        if km >= self.odometry:
            self.odometry = km
        else:
            print("fuck you")

    def increment_odometry(self, km):
        self.odometry += km


class Battery():
    def __init__(self, battery=100):
        self.battery = 100

    def description_battery(self):
        print("Ostalos zarada " + str(self.battery))

class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()

    def description_name(self):
        desc = str(self.year) + ' ' + self.model
        return desc
