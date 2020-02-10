import json
from typing import Callable



def rule(func: Callable) -> Callable:
    """Decorator who adds violations if rule return it
	
	Arguments:
		func {Callable} -- Rule function
	
	Returns:
		Callable -- operation with violations added
	"""

    def inner1(operation: dict, **kwargs) -> dict:
        if len(func(operation, **kwargs)):
            if "violations" not in operation.keys():
                operation["violations"] = []
            operation["violations"].append(func(operation, **kwargs))

        return operation

    return inner1
