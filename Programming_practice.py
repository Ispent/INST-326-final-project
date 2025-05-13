"""Programming practice
"""
'''
class Car:
    """represents a car
    """
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")
        
    
toyota_corolla = Car('toyota', 'corolla', '2020')
toyota_corolla.display_info()
'''

class Student:
    """
    Represents a Student
    """
    def __init__(self, name, student_id, major):
        self.name = name
        self.student_id = student_id
        self.major = major
    
    def introduce(self):
        print(f"Hi, I'm {self.name} my student id is {self.student_id}, and I'm majoring in {self.major}.")
        
alex_student = Student('Alex', '12345', 'information science')
alex_student.introduce()