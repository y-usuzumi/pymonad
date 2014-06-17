# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

from pymonad.DoVariables import var, VariableDefinition

class Container(object):
	""" Represents a wrapper around an arbitrary value and a method to access it. """

	def __init__(self, value):
		""" 
		Wraps the given value in the Container. 
		
		'value' is any arbitrary value of any type including functions.

		"""
		self.value = value
	
	def getValue(self):
		""" Returns the value held by the Container. """
		return self.value

	def __eq__(self, other):
		return self.value == other.value

	def __ror__(self, varName):
		var.addVariable(varName)
		return VariableDefinition(varName, self)

def force(value):
	try: return value.force()
	except AttributeError: 
		try: return value()
		except TypeError: return value
