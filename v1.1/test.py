class test:
    a = 0
    def __init__(self, a):
        self.a = a

b = test(2)
print(b.a)
print(test.a)