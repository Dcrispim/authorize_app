from typing import Callable


def rule(func:Callable)->Callable:
	def inner1(transaction:dict, **kwargs)-> dict: 
		if len(func(transaction,**kwargs)):
			try:
				transaction["violations"].append(func(transaction,**kwargs))
			except KeyError:
				transaction["violations"]=[]
				transaction["violations"].append(func(transaction,**kwargs))

		return transaction 

	return inner1

