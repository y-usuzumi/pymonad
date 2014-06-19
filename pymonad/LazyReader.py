# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Reader import *

class LazyReader(Reader):
	""" Represents a Functor for functions allowing authors to map functions over other functions. """

	def __call__(self, *args):
		"""
		Applies arguments to the curried function.

		Returns the result of the function if all arguments are passed. If fewer than
		the full argument set is passed in, returns a curried function which expects the
		remaining arguments. For example, a function 'func' which takes 3 arguments can be
		called in any of the following ways:
			func(1, 2, 3)
			func(1, 2)(3)
			func(1)(2, 3)
			func(1)(2)(3)

		"""
		value = self.getValue()
		numArgs = len(args)
		for a in args:
			try: value = value(a)
			except TypeError:
				raise TypeError("Too many arguments supplied to curried function.")

		if (callable(value)): 
			value = LazyReader(value)
		return value

	def __mul__(self, func):
		return func.fmap(self).fmap(force)

	@classmethod
	def unit(cls, value):
		return LazyReader(lambda _: value)

	def force(self):
		try: return self.value()
		except TypeError: return self

def lazy(aFunction):
	""" 
	Turns a normal python function into a curried function.

	Most easily used as a decorator when defining functions:
		@curry
		def add(x, y): return x + y

	"""
	numArgs = aFunction.__code__.co_argcount
	def buildReader(argValues, numArgs):
		if (numArgs == 0): return lambda: aFunction(*map(force, argValues))
		else: return lambda x: buildReader(argValues + [x], numArgs - 1)
	return LazyReader(buildReader([], numArgs))

if __name__ == "__main__":
	from pymonad import *

	@lazy
	def neg(x): return -x

	@lazy
	def add(x, y): return x + y

	print("forced bare function: " + str(force(neg(5))))
	print("unforced bare function: " + str(force(neg(5))))
	print(force(add(1, 2)))
	print(force(add(1)(2)))
	print("unforced composed function: " + str((add(1) * add(2))(3)))
	print("forced composed function: " + str(force((add(1) * add(2))(3))))

	@lazy
	def lazy_div(y, x):
		if y == 0: return Nothing
		else: return Just(x / y)

	@curry
	def div(y, x):
		if y == 0: return Nothing
		else: return Just(x / y)

	@lazy
	def add2(x): return Just(2 + x)

	print("binding single arugment lazy function: " + str(Just(9) >> add2))
	print(neg * Just(9))
	print(add * Just(9) & Just(9))
	print(force(div(2, 4)))
	print("Lazy div: " + str(Just(8) >> lazy_div(2)))
	print("Regular div: " + str(Just(8) >> div(2)))
