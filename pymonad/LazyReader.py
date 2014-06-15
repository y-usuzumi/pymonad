# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.Monad import *

class Reader(Monad):
	""" Represents a Functor for functions allowing authors to map functions over other functions. """

	def __init__(self, functionOrValue):
		""" 
		Stores or creates a function as the Functor's value.

		If 'functionOrValue' is a function, it is stored directly.
		However, if it is a value -- 7 for example -- then a function taking a single argument
		which always returns that value is created and that function is stored as the Functor's 
		value.

		In general, you won't create 'Reader' instances directly. Instead use the @curry
		decorator when defining functions. 'Reader' may not function as expected if 
		non-curried functions are used.

		"""

		if (callable(functionOrValue)):
			func = functionOrValue
		else:
			func = lambda _: functionOrValue

		super(Reader, self).__init__(func)

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

		if (callable(value)): return Reader(value)
		else: return value

	def __mul__(self, func):
		try: return func.fmap(self).fmap(force)
		except TypeError: return func.fmap(self)

	def fmap(self, aFunction):
		""" 
		Maps 'aFunction' over the function stored in the Functor itself.

		Mapping a function over another function is equivalent to function composition.
		In other words,
			composedFunc = curriedFunc1 * curriedFunc2
			composedFunc(parameter)
		is equivalent to
			composedFunc = lambda x: curriedFunc1(curriedFunc2(x))
			composedFunc(parameter)

		Both 'curriedFunc1' and 'curriedFunc2' must take only a single argument
		but either, or both, can be partially applied so they have only a single argument
		remaining.

		"""
		return Reader(lambda x: aFunction(self.getValue()(x)()))
	
	def amap(self, functorValue):
		""" Applies function stored in the functor to 'functorValue' creating a new function. """
		return Reader(lambda x: self(x)(functorValue(x)))

	def bind(self, function):
		""" Threads a single value through multiple function calls. """
		return Reader(lambda x: function(self.getValue()(x))(x))

	@classmethod
	def unit(cls, value):
		return Reader(lambda _: value)

	def force(self):
		return self.value()

def lazy(aFunction):
	""" 
	Turns a normal python function into a curried function.

	Most easily used as a decorator when defining functions:
		@curry
		def add(x, y): return x + y

	"""
	numArgs = aFunction.__code__.co_argcount
	def buildReader(argValues, numArgs):
		if (numArgs == 0): return lambda: aFunction(*argValues)
		else: return lambda x: buildReader(argValues + [x], numArgs - 1)
	return Reader(buildReader([], numArgs))

if __name__ == "__main__":
	from pymonad import *

	@lazy
	def neg(x): return -x

	@lazy
	def add(x, y): return x + y

	print(force(neg(5)))
	print(force(add(1, 2)))
	print(force(add(1)(2)))
	print("unforced: " + str((add(1) * add(2))(3)))
	print("forced: " + str(force((add(1) * add(2))(3))))

	@lazy
	def lazy_div(y, x):
		if y == 0: return Nothing
		else: return Just(x / y)

	@curry
	def div(y, x):
		if y == 0: return Nothing
		else: return Just(x / y)

	print(neg * Just(9))
	print(add * Just(9) & Just(9))
	print(force(div(2, 4)))
	print("Lazy div: " + str(Just(8) >> lazy_div(2)))
	print("Regular div: " + str(Just(8) >> div(2)))
