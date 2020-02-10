from datasetMaker import makeDataset
import os
from operations import OPERATIONS, addCreditOperation, isJson
import json

os_args = os.sys.argv[1:]
sys_args = {}

operations = []
_exclude = []

__DIRNAME__ = os.sys.path[0]

LIST_TYPES_OPERATIONS = {
    "1": addCreditOperation,
}


def parseArgs(list_args: list) -> dict:
    _args = {}
    for i in range(len(list_args)):
        if list_args[i][0] == "-":
            try:
                if list_args[i + 1][0] != "-":
                    _args[list_args[i]] = list_args[i + 1]
                    _exclude.append(list_args[i + 1])
            except IndexError:
                _args[list_args[i]] = True

        elif list_args[i] not in _exclude:
            _args[i] = list_args[i]

    return _args


def addFromFile(filePath):
    with open(filePath, "r") as File:
        response_transaction = []
        for line in File.readlines():
            transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(line))
            for subline in transaction:
                operations.append(str(subline).replace("'", '"'))
                response_transaction.append(str(subline).replace("'", '"'))
        return response_transaction


def saveInFile(file_content: list, save_path, mode="w"):
    with open(save_path, mode) as File:
        File.write(
            "\n".join([str(line) for line in file_content]).replace("'", '"').strip()
        )


sys_args.update(parseArgs(os_args))

_type_operation_ = "1" if "-type" not in sys_args.keys() else sys_args["-type"]


def tryAddOperationsWithArgs():
    _del = []
    for i in sys_args.keys():
        if str(i).isdigit():
            op = LIST_TYPES_OPERATIONS[_type_operation_](sys_args[i])
            operations.append(op)
            [print(str(line).replace("'", '"')) for line in op]
            _del.append(i)

    for i in _del:
        del sys_args[i]


# Cli Commands
def _f(arg, **kwargs):
    try:
        for line in addFromFile(arg):
            print(line)
    except FileNotFoundError as e:
        if "/" not in arg or "\\" not in arg:
            _f(os.path.join(__DIRNAME__, arg), **kwargs)
        else:
            print(f"No such file or directory: {e}")


def _save(arg, **kwargs):
    saveInFile(kwargs["operations"], arg)


def _append(arg, **kwargs):
    saveInFile(kwargs["operations"], arg, "a")


def _form(arg, **kwargs):
    _id = int(input("ID: "))
    _consumer_id = int(input("CONSUMER_ID: "))
    _score = int(input("SCORE: "))
    _income = int(input("INCOME: "))
    _requested_value = int(input("REQUESTED_VALUE: "))
    _installments = int(input("INSTALLMENTS: "))
    print("TIME:")
    _Y = int(input("    YEAR: "))
    _M = int(input("    MONTH: "))
    _D = int(input("    DAY: "))
    _h = int(input("    HOUR: "))
    _m = int(input("    MINUTE: "))
    _s = float(input("    SECOND: "))

    _op = {
        "transaction": {
            "id": _id,
            "consumer_id": _consumer_id,
            "score": _score,
            "income": _income,
            "requested_value": _requested_value,
            "installments": _installments,
            "time": f"{_Y:0>4}-{_M:0>2}-{_D:0>2}T{_h:0>2}:{_m:0>2}:{_s:.3f}Z",
        }
    }
    for key in _op["transaction"].keys():
        print(f'{key} --> {_op["transaction"][key]}')
    sv = input("Save? [S/N]")
    while True:
        if sv.lower() == "s" or sv.lower() == "y":
            print(LIST_TYPES_OPERATIONS[_type_operation_](str(_op)))
            break
        elif sv.lower() == "n":
            print("Cancel")
            break


def _loop(arg, **kwargs):
    while True:
        Input = input(":> ")

        if Input == "-q":
            break

        if isJson(Input):
            LIST_TYPES_OPERATIONS[_type_operation_](Input)
        else:
            input_args = parseArgs(Input.split())
            run_commands(input_args, **kwargs)


def _operations(arg, **kwargs):
    for op in kwargs["operations"]:
        print(kwargs["operations"][op])


def _c(arg, **kwargs):

    return os.system(input(":[sys]> "))


def _tests(arg, **kwargs):
    os.system(f'python3 {os.path.join(__DIRNAME__,"tests.py")}')

def _json(arg, **kwargs):
    with open(arg, "r") as File:
        json_file = json.load(File)

        response_transaction = []
        if type(json_file)==list:
            for line in json_file:
                transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(line))
                for subline in transaction:
                    operations.append(str(subline).replace("'", '"'))
                    response_transaction.append(str(subline).replace("'", '"'))
        
        if type(json_file)==dict:
            transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(json_file))
            for line in transaction:
                operations.append(str(line).replace("'", '"'))
                response_transaction.append(str(line).replace("'", '"'))

        [print(line) for line in response_transaction ]

# end Cli commands


def run_commands(list_args, **kwargs):
    _cmd = {
        "-f": _f,
        "-save": _save,
        "-append": _append,
        "-loop": _loop,
        "-op": _operations,
        "-c": _c,
        "-form": _form,
        "-tests": _tests,
        "-type": True,
        "-json":_json
    }

    for key in list_args.keys():
        try:
            _cmd[key](list_args[key], **kwargs)
        except KeyError as k:
            _key = str(k)
            print(
                f"Comando {_key if not _key.isdigit() else list_args[int(_key)]} não encontrado"
            )
        except TypeError as t:
            if type(list_args[key]) == bool:
                pass





tryAddOperationsWithArgs()

run_commands(sys_args, operations=OPERATIONS)
