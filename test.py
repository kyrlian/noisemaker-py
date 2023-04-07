#!python3

class MyObj:
    def __init__(self, content=[], name="default"):
        self.content=content
        self.name=name
    def describe(self):
        print(f"content:{self.content}, name:{self.name}")

a = MyObj(name="obj1")
a.content=[1]
a.describe()
b = MyObj(name="obj2")
b.describe()
c = MyObj()
c.describe()
