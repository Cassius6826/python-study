class Animal:

    def spark(self):
        pass

class Dog(Animal):

    def spark(self):
        print("汪汪汪")

class Cat(Animal):

    def spark(self):
        print("喵喵喵")

def make_noise(animal : Animal):
    animal.spark()

dog = Dog()
cat = Cat()

make_noise(dog)
make_noise(cat)