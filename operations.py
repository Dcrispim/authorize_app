import json
from typing import Dict
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


def addCreditOperation(operation: str) -> str:
    if isJson(operation):
        transaction = json.loads(operation)

        list_rules = [
            compromised_income,
            low_score,
            minimum_installments,
            doubled_transactions,
        ]

        operation_verified = verifyRules(
            transaction, list_rules, db_operations=OPERATIONS,
        )

        response = {
            "id": operation_verified["transaction"]["id"],
            "violations": operation_verified["violations"],
        }

        if len(operation_verified["violations"]) == 0:
            del operation_verified["violations"]
            OPERATIONS[
                str(operation_verified["transaction"]["id"])
            ] = operation_verified

        return str(response).replace("'", '"')
    else:
        raise TypeError(f"The '{operation}' is not a json line")