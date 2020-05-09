class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def f(obj, a, b):
    if isinstance(obj, A):
        obj.a = a
        obj.b = b

f(A(3,5), 6, 9)