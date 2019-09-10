
class A:
	h = 1
	def __init__(self, x):
		self.x = x

	def __repr__(self):
		return "<A(x: '%d', h: '%d'>" % (self.x, self.h)

class B(A):
	def __init__(self, x):
		super().__init__(x)

	def __repr__(self):
		return "<B(x: '%d', h: '%d'>" % (self.x, self.h)


def initCls(cls, x):
	print(dir(cls))
	return cls(x)

a = initCls(A, 1)

a1 = A(1)
a2 = A(2)

print(a1)
print(a2)

b1 = B(10)
b2 = B(20)

print(b1)
print(b2)
