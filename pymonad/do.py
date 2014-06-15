from pymonad.Container import force, var

def do(*monadicStatements):
	result = force(monadicStatements[0])
	for statement in monadicStatements[1:]:
		try: result = force(result >> statement)
		except TypeError: result = force(statement)
	var.clearVariables()
	return result

if __name__ == "__main__":
	from pymonad import *

	@lazy
	def add(x, y): return x + y

	@lazy
	def div(y, x):
		if y == 0: return Nothing
		else: return Just(x // y)

	x = do(
		"x" | Just(8),
		"y" | div(2, var.x),
		add * Just(var.x) & Just(var.y),
		#Just(9)
	)

	print(x)

	try:
		print(var.x)
		print(var.y)
	except: print("You should see this because the 'var' variables aren't accessible outside of a do block.")

	try:
		x = do( Just(var.x) )
	except:
		print("And you should see this, because 'var' variables are local to the do block where they're created.")

	@lazy
	def mul(x, y): return Right(x * y)

	x = do( "x" | Right(2)
	      , mul(2)
		  #, "y" | Left("error")
		  , "y" | mul(3, var.x)
		  , mul(var.x, var.y)
		  , add * Right(var.x) & Right(var.y)
	)

	print(x)

	#@lazy
	#def plusMinus(x):
	#	return List(x, -x)

	#x = do( "x" | List(1, 2, 3)
	#      , plusMinus(var.x)
	#	  #, add * List(1, 2, 3) & List(1, 2, 3)
	#)

	#print(x)
