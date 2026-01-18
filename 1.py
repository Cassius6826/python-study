class Student:
    #构造器
    def __init__(self, name, age, gender, native_place, nationality):
        self.name = name
        self.age = age
        self.gender = gender
        self.native_place = native_place
        self.nationality = nationality
    #魔术方法   __str__   __lt__   __le__   __eq__   __gt__   __ge__   __ne__
    #__str__  返回对象的字符串表示
    #__lt__  小于
    #__le__  小于等于
    #__eq__  等于
    #__gt__  大于
    #__ge__  大于等于
    #__ne__  不等于
    def __str__(self):
        return f"Student(name={self.name}, age={self.age}, gender={self.gender}, native_place={self.native_place}, nationality={self.nationality})"

    def __lt__(self, other):
        return self.age < other.age

    def __le__(self, other):
        return self.age <= other.age

    def __eq__(self, other):
        return self.age == other.age

stu_1 = Student("zhangsan", 18, "male", "beijing", "china")
stu_2 = Student("lisi", 20, "female", "shanghai", "china")
print(stu_1)

print(stu_1 < stu_2)
print(stu_1 <= stu_2)
print(stu_1 == stu_2)
print(stu_1 > stu_2)
print(stu_1 >= stu_2)
print(stu_1 != stu_2)
