class Hamster:
    def __init__(self,name,weight,color,caracter):
        self.name = name
        self.weight = weight
        self.color = color
        self.caracter= caracter
    def print_info(self):
        print('homyak',self.name)
        print('характер',self.caracter)
        print('вес',self.weight)
        print('цвет',self.color)
    def eat(self):
        print('homyak',self.name,'eats')
        self.weight += 10000000
        print('вес',self.weight)
        
animal = Hamster('Hamster combat',100000000000000000000000000000000000000,'white','angry+crazy')
animal.print_info()
for i in range(200):
    animal.eat()