class MyObject:
    def __init__(self):
        self.var1 = 5
        self.var2 = 6
        self.var7 = "test"

    def test(self):
        pass
    
my_object = MyObject()
for property, value, in vars(my_object).items():
    print(property, ":", type(value))