from pymonad.Container import force, var, VariableDefinition
from pymonad.LazyReader import lazy

monad = None

def do(withMonad, *monadicStatements):
	global monad
	monad = withMonad
	def build_do_expression(ms):
		if len(ms) == 1 and isinstance(ms[0], VariableDefinition): return force(ms[0].code)
		elif len(ms) == 1: return force(ms[0])
		elif isinstance(ms[0], VariableDefinition): return force(ms[0].code) >> (lambda x: var.updateVariable(ms[0].varName, x) and build_do_expression(ms[1:]))
		else: return force(ms[0]) >> build_do_expression(ms[1:])
			
	result = build_do_expression(monadicStatements)
	var.clearVariables()
	monad = None
	return result


@lazy
def mreturn(value):
	return monad.unit(value)

if __name__ == "__main__":
	from pymonad import *

	@lazy
	def neg(x): 
		return -x

	@lazy
	def smallerThanFive(num):
		if num >= 5: return Left("Oops! Too big.")
		else: return Right(num)

	x = do( Either
		  , "x" | mreturn(4)
		  , "y" | Right(8)
		  , smallerThanFive(var.y)
		  , smallerThanFive(var.x)
	)

	print(x)

	@lazy
	def add(x, y): return x + y

	@lazy
	def div(y, x):
		if y == 0: return Nothing
		else: return Just(x // y)

	x = do( Maybe
	      , Just(8)
	      , div(2, 10)
		  , "x" | Just(16)
		  , "x" | div(2, var.x)
		  , div(var.x, 32)
		  , mreturn(var.x)
	)

	print(x)

	@lazy
	def plusMinus(x):
		return List(x, -x)

	x = do( List
		  , "x" | List(1, 2, 3)
	      , plusMinus(var.x)
	)

	print(x)

	@lazy
	def add(x, y):
		return StringWriter(x + y, "Added " + str(x) + " and " + str(y) + ".")

	x = do( StringWriter
	      , "x" | mreturn(1)
		  , "y" | mreturn(2)
		  , "z" | add(var.x, var.y)
		  , add(var.y, var.z)
	)

	print(x)
