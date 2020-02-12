from typing import Union
from datasetMaker import makeDataset
import os
from operations import OPERATIONS, addCreditOperation, isJson
import json

os_args = os.sys.argv[1:]
sys_args = {}

response_operations = []
_exclude = []

__DIRNAME__ = os.sys.path[0]

LIST_TYPES_OPERATIONS = {
    "1": addCreditOperation,
}


def parseArgs(list_args: list) -> dict:
    """get a list of args and convert do dict of all args and values
    """    
    _args = {}
    for i in range(len(list_args)):
        if list_args[i][0] == "-":
            try:
                _next_arg = list_args[i + 1]
                if _next_arg[0] != "-":
                    if _next_arg[0]=="'" or _next_arg[0]=='"':
                        arg_parts = []
                        firstKey = _next_arg[0]
                        for word in list_args[i+1:]:
                            arg_parts.append(word)
                            _exclude.append(word)
                            if word[-1] == firstKey:
                                break
                        _args[list_args[i]] = ' '.join(arg_parts)[1:-1]
                        
                    else:
                        _args[list_args[i]] = list_args[i + 1]
                        _exclude.append(list_args[i + 1])
                else:
                    _args[list_args[i]] = True

            except IndexError:
                _args[list_args[i]] = True

        elif list_args[i] not in _exclude:
            _args[i] = list_args[i]

    return _args


def addFromFile(filePath):
    """Adds the current operation response of each line on filePath  on response_operations
    """    
    with open(filePath, "r") as File:
        response_transaction = []
        for line in File.readlines():
            transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(line))
            for subline in transaction:
                response_operations.append(str(subline).replace("'", '"'))
                response_transaction.append(str(subline).replace("'", '"'))
        return response_transaction


def saveInFile(file_content:Union[dict,list] , save_path, mode="w"):
    """Save file_content on save_path
    """ 

    with open(save_path, mode) as File:
        if type(file_content)==list:
            File.write(
                "\n".join([str(line) for line in file_content]).replace("'", '"').strip()
            )
        elif type(file_content)==dict:
            File.write(
                "\n".join([str(file_content[line]) for line in file_content]).replace("'", '"').strip()
            )


def tryAddOperationsWithArgs():
    """try run the current operaiton with the args without keys 
    """ 
    _del = []
    for i in sys_args.keys():
        if str(i).isdigit():
            op = LIST_TYPES_OPERATIONS[_type_operation_](sys_args[i])
            response_operations.append(op)
            [print(str(line).replace("'", '"')) for line in op]
            _del.append(i)

    for i in _del:
        del sys_args[i]


# Cli Commands
def _f(arg, list_args={}, **kwargs):
    try:
        for line in addFromFile(arg):
            print(line)
    except FileNotFoundError as e:
        if "/" != arg[0] or "\\" != arg[0]:
            _f(os.path.join(__DIRNAME__, arg), **kwargs)
        else:
            print(f"No such file or directory: {e}")


def _save(arg, list_args={}, **kwargs):
    saveInFile(kwargs["operations"], arg)

def _saveh(arg, list_args={}, **kwargs):
    saveInFile(kwargs["history"], arg)





def _append(arg, list_args={}, **kwargs):
    saveInFile(kwargs["operations"], arg, "a")


def _form(arg, list_args={}, **kwargs):
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


def _loop(arg, list_args={}, **kwargs):
    while True:
        Input = input(":> ")

        if Input == "-q":
            break

        if isJson(Input):
            LIST_TYPES_OPERATIONS[_type_operation_](Input)
        else:
            input_args = parseArgs(Input.split())
            print(input_args)
            run_commands(input_args, **kwargs)


def _operations(arg, list_args={}, **kwargs):
    for op in kwargs["operations"]:
        print(kwargs["operations"][op])


def _c(arg, list_args={}, **kwargs):

    return os.system(input(":[sys]> "))


def _tests(arg, list_args={}, **kwargs):
    os.system(f'python3 {os.path.join(__DIRNAME__,"tests.py")}')

def _json(arg, list_args={}, **kwargs):
    with open(arg, "r") as File:
        json_file = json.load(File)

        response_transaction = []
        if type(json_file)==list:
            for line in json_file:
                transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(line))
                for subline in transaction:
                    response_operations.append(str(subline).replace("'", '"'))
                    response_transaction.append(str(subline).replace("'", '"'))
        
        if type(json_file)==dict:
            transaction = LIST_TYPES_OPERATIONS[_type_operation_](str(json_file))
            for line in transaction:
                response_operations.append(str(line).replace("'", '"'))
                response_transaction.append(str(line).replace("'", '"'))

        [print(line) for line in response_transaction ]


def _mkdt(arg, list_args={}, **kwargs):
    limit = 2 if type(arg) == bool else int(arg) 
    name_file = "dataset.dt" if "-dtname" not in list_args.keys() else list_args["-dtname"]
    dataset = makeDataset(limit)
    saveInFile(dataset,os.path.join(__DIRNAME__,name_file))

# end Cli commands


def run_commands(list_args, **kwargs):
    _cmd = {
        "-f": _f,
        "-save": _save,
        "-saveh":_saveh,
        "-append": _append,
        "-loop": _loop,
        "-op": _operations,
        "-c": _c,
        "-form": _form,
        "-tests": _tests,
        "-type": True,
        "-json":_json,
        "-mkdt":_mkdt,
        "-dtname":True,
        "-v":"1.0"
    }

    for key in list_args.keys():
        try:
            _cmd[key](list_args[key], list_args, **kwargs)
        except KeyError as k:
            _key = str(k)
            print(
                f"Comando {_key if not _key.isdigit() else list_args[int(_key)]} não encontrado"
            )
        except TypeError as t:
            if type(_cmd[key]) == bool:
                pass
            if type(_cmd[key]) == str:
                print(_cmd[key])



sys_args.update(parseArgs(os_args))
_type_operation_ = "1" if "-type" not in sys_args.keys() else sys_args["-type"]



tryAddOperationsWithArgs()

run_commands(sys_args, operations=OPERATIONS, history=response_operations)