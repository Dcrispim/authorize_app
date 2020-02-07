import json
from rules import (
    compromised_income,
    doubled_transactions,
    low_score,
    minimum_installments,
)

TRANSACTIONS: dict = {}


def isJson(string: str) -> bool:
    try:
        jsonFile = json.loads(string)
        return True if (type(jsonFile) == dict or type(jsonFile) == list) else False
    except:
        return False


def verifyRules(transaction: dict, rules: list, index: int = 0, **kwargs) -> dict:
    """Ruturns True if transaction pass to all rules and False if not
    
        Arguments:
            transaction {dict} -- transaction dict {"transaction":dict, "status":dict}
            rules {list} -- list of Rule Functions [function, function]
        
        Keyword Arguments:
            index {int} -- internal index (default: {0})
        
        Returns:
            bool -- [description]
    """

    if len(rules) > 0:
        new_transaction: dict = rules[0](transaction, **kwargs)
        return verifyRules(new_transaction, rules[1:], index + 1, **kwargs)
    else:
        return transaction


def addTransaction(transaction: str):
    if isJson(transaction):
        trans = json.loads(transaction)
        transaction_verified = verifyRules(
            trans,
            [compromised_income, low_score, minimum_installments, doubled_transactions],
            db_transactions=TRANSACTIONS,
        )
        try:
            if not transaction_verified["violations"]:
                TRANSACTIONS[str(transaction_verified["transaction"]["id"])] = transaction_verified
                return {
                    "id": transaction_verified["transaction"]["id"],
                    "violations": [],
                    "status": "Success",
                }
        except KeyError:
            TRANSACTIONS[str(transaction_verified["transaction"]["id"])] = transaction_verified
            return {
                "id": transaction_verified["transaction"]["id"],
                "violations": [],
                "status": "Success",
            }

        return {
            "id": transaction_verified["transaction"]["id"],
            "violations": transaction_verified["violations"],
            "status": "Fail",
        }



