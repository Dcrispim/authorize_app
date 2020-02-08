import unittest
from unittest import TestCase

from rules import *
from operations import addCreditOperation, OPERATIONS


class Test_Rules(TestCase):
    def setUp(self) -> None:
        self.OPERATIONS = []

        self.credit_trasaction_pass = {
            "transaction": {
                "id": 1,
                "consumer_id": 10,
                "score": 200,
                "income": 4000,
                "requested_value": 10000,
                "installments": 1200,
                "time": "2019-02-13T10:00:00.000Z",
            }
        }

    def test_pass_all(self):
        self.assertEqual(
            compromised_income(self.credit_trasaction_pass), self.credit_trasaction_pass
        )

    def test_compromised_income_fail(self):
        transaction = {}
        response = {}

        transaction.update(self.credit_trasaction_pass)
        transaction["transaction"]["installments"] = 1201

        response.update(transaction)
        response["violations"] = ["compromised-income"]

        self.assertEqual(compromised_income(transaction), response)

    def test_low_score_fail(self):
        transaction = {}
        response = {}

        transaction.update(self.credit_trasaction_pass)
        transaction["transaction"]["score"] = 199

        response.update(transaction)
        response["violations"] = ["low-score"]

        self.assertEqual(low_score(transaction), response)

    def test_minimum_installments_fail(self):
        transaction = {}
        response = {}

        transaction.update(self.credit_trasaction_pass)
        transaction["transaction"]["installments"] = 5

        response.update(transaction)
        response["violations"] = ["minimum-installments"]

        self.assertEqual(minimum_installments(transaction), response)

    def test_doubled_transactions_fail(self):

        db_operations = {"1": self.credit_trasaction_pass}
        response = {}
        transaction = {
            "transaction": {
                "id": 1,
                "consumer_id": 10,
                "score": 200,
                "income": 4000,
                "requested_value": 10000,
                "installments": 1200,
                "time": "2019-02-13T10:00:02.000Z",
            }
        }

        response.update(transaction)
        response["violations"] = ["doubled-transactions"]

        self.assertEqual(
            doubled_transactions(transaction, db_operations=db_operations), response
        )


class Test_Operations(TestCase):
    def setUp(self) -> None:
        self.dataset = [
            {
                "transaction": {
                    "id": 1,
                    "consumer_id": 10,
                    "score": 600,
                    "income": 4000,
                    "requested_value": 10000,
                    "installments": 1201,
                    "time": "2019-02-13T10:00:00.000Z",
                }
            },
            {
                "transaction": {
                    "id": 2,
                    "consumer_id": 10,
                    "score": 100,
                    "income": 4000,
                    "requested_value": 10000,
                    "installments": 15,
                    "time": "2019-03-13T10:00:00.000Z",
                }
            },
            {
                "transaction": {
                    "id": 3,
                    "consumer_id": 10,
                    "score": 500,
                    "income": 4000,
                    "requested_value": 10000,
                    "installments": 0,
                    "time": "2019-04-13T10:00:00.000Z",
                }
            },
            {
                "transaction": {
                    "id": 4,
                    "consumer_id": 10,
                    "score": 600,
                    "income": 4000,
                    "requested_value": 10000,
                    "installments": 1200,
                    "time": "2019-02-13T10:00:00.000Z",
                }
            }
        ]

    def tests_credit_operation(self):
        for operation in self.dataset:
            addCreditOperation(str(operation).replace("'",'"'))
        
        response = {
            "4":{
                "transaction": {
                    "id": 4,
                    "consumer_id": 10,
                    "score": 600,
                    "income": 4000,
                    "requested_value": 10000,
                    "installments": 1200,
                    "time": "2019-02-13T10:00:00.000Z",
                }
            }
        }
        self.assertEqual(response, OPERATIONS)


if __name__ == "__main__":
    unittest.main()
