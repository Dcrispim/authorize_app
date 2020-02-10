import json
from typing import Callable, Dict
from rules import (
    compromised_income,
    doubled_transactions,
    low_score,
    minimum_installments,
)

OPERATIONS: dict = {}

def isJson(string: str) -> bool:
    try:
        jsonFile = json.loads(string)
        return True if (type(jsonFile) == dict or type(jsonFile) == list) else False
    except:
        return False


def verifyRules(operation: dict, rules: list, index: int = 0, **kwargs) -> dict:
    """Ruturns True if operation pass to all rules and False if not
    
        Arguments:
            operation {dict} -- operation dict {"transaction":dict, "status":dict}
            rules {list} -- list of Rule Functions [function, function]
        
        Keyword Arguments:
            index {int} -- internal index (default: {0})
        
        Returns:
            bool -- [description]
    """

    if len(rules) > 0:
        new_operation: dict = rules[0](operation, **kwargs)
        return verifyRules(new_operation, rules[1:], index + 1, **kwargs)
    else:
        if "violations" not in operation.keys():
            operation["violations"] = []
        return operation


def makeOperations(json_operations: str, list_rules: list, database) -> list:
    if isJson(json_operations.replace("'", '"')):
        list_operations = json.loads(json_operations.replace("'", '"'))
        finish_operations = []

        if type(list_operations) == list:
            for op in list_operations:
                line = verifyRules(op, list_rules, database=database,)

                finish_operations.append(line)

        elif type(list_operations) == dict:
            finish_operations.append(
                verifyRules(list_operations, list_rules, database=database,)
            )

        return finish_operations
    else:
        raise TypeError(f"The '{json_operations}' is not a json line")



#Operations
def addCreditOperation(json_operation:str) -> list:
    list_rules = [compromised_income, doubled_transactions, low_score, minimum_installments]

    responses = []

    for line in makeOperations(json_operation, list_rules, database=OPERATIONS):
        line_transaction = line["transaction"]

        if len(line["violations"])==0:
            OPERATIONS[line_transaction["id"]] = line_transaction
        
        responses.append({"id":line_transaction["id"],"violations":line["violations"] })
    
    return responses


#End Operations