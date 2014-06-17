# --------------------------------------------------------
# (c) Copyright 2014 by Jason DeLaat. 
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------

class VariableDefinition:
	def __init__(self, varName, code):
		self.varName = varName
		self.code = code

class _Variables: 
	def __init__(self):
		self.references = {}

	def addVariable(self, varName):
		self.__dict__[varName] = lambda: self.references[varName]

	def clearVariables(self):
		self.__dict__ = {}
		self.references = {}

	def updateVariable(self, varName, value):
		self.references[varName] = value
		return True

var = _Variables()
