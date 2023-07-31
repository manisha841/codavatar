#object oriented programming in Python: object oriented programming is a programming technique which uses objects and classes to organize the code.
#classes are the blueprint or the templates while objects are the instances of class

class Employee:

    def __init__(self,name,id,mon_salary):
        self.name = name
        self.id = id
        self.mon_salary =mon_salary

    def annual_salary(self):
        return f'Annual salary of the employee is {self.mon_salary*12}'
    

emp = Employee('Manisha',12,1000000000)

#inheritance
class Animal:

    def bark(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass

class Dog(Animal):

    def doesbark(self):
        return True
    
class Elephant(Animal):

    def doeseat(self):
        return True

an = Animal()

do = Dog()
print(do.doesbark())

el = Elephant()
print(el.eat())

print(el.doeseat())


