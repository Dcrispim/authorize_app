#Get started:

## Making Docker Container ##

<p>
To start, go to the directory of application, open the terminal and
type it:

*root access may needed*

``` 
docker build . -t authorize_app:1.0
```

Next run the container:

``` 
docker build run -it authorize_app:1.0
```

Inside the container you can provide a json line to make an operation

``` 
root@173203a44050:/# authorize '{ "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}}'
```

<br>
Or use the commands below to make the operations:
<br>
<br>

<b>-type</b>: set operation <small>(default is "1": Credit Operation)</small>
*now the app has only one, but more can be added*

``` 
root@173203a44050:/# authorize -f ./dataset.py -type 1
```

<br>
<b>-f</b>: run the operation on file provided

to use -f each line of file must be a json line

<b>Warning:</b> the command -f don't read *.json files

``` 
root@173203a44050:/# authorize -f /app/dataset.txt
```

dataset.txt

``` 
{ "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}}
{ "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}}
{ "transaction": { "id": 2, "consumer_id": 10, "score": 100, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-03-13T10:00:00.000Z"}}
{ "transaction": { "id": 3, "consumer_id": 10, "score": 500, "income": 4000, "requested_value": 10000,"installments": 0, "time": "2019-04-13T10:00:00.000Z"}}
{ "transaction": { "id": 3, "consumer_id": 10, "score": 500, "income": 4000, "requested_value": 10000,"installments": 0, "time": "2019-04-13T10:00:00.000Z"}}
```

<br>

<b>-json</b>: run the operation on json file provided

``` 
root@173203a44050:/# authorize -json /app/dataset.json
```

dataset.json

``` json
[
    { "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}},
    { "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}},
    { "transaction": { "id": 2, "consumer_id": 10, "score": 100, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-03-13T10:00:00.000Z"}},
    { "transaction": { "id": 3, "consumer_id": 10, "score": 500, "income": 4000, "requested_value": 10000,"installments": 0, "time": "2019-04-13T10:00:00.000Z"}},
    { "transaction": { "id": 3, "consumer_id": 10, "score": 500, "income": 4000, "requested_value": 10000,"installments": 0, "time": "2019-04-13T10:00:00.000Z"}},
]
```

<br>

<b>-saveh</b>: save the operation response on path provided

``` 
root@173203a44050:/# authorize -f /app/dataset.txt -saveh /app/hystory.log
```

<br>

<b>-save</b>: Save valid operations to the provided path

``` 
root@173203a44050:/# authorize -f /app/dataset.txt -save /app/ops.log
```

ops.log

``` 
{"id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000, "installments": 15, "time": "2019-02-13T10:00:00.000Z"}
```

<br>
<b>-append</b>: append the operation on path provided

``` 
root@173203a44050:/# authorize -f /app/dataset.txt -append /app/ops.log
```

<br>

<b>-loop:</b> just start a loop to facilitate the continuous manual use

To exit loop press <b>-q</b>

*all commands are functional inside the loop*

``` 
root@b08b4609608b:/# authorize -loop
:> -f line
[{"id": 1, "violations": []}]
[{"id": 1, "violations": ["doubled-transactions"]}]
[{"id": 2, "violations": ["low-score"]}]
[{"id": 3, "violations": ["minimum-installments"]}]
[{"id": 3, "violations": ["minimum-installments"]}]
:> 
```

<br>
<b>-op</b>:  list the operations added on database

``` 
root@82c2ddf25046:/# authorize -f line -op
[{"id": 1, "violations": []}]
[{"id": 1, "violations": ["doubled-transactions"]}]
[{"id": 2, "violations": ["low-score"]}]
[{"id": 3, "violations": ["minimum-installments"]}]
[{"id": 3, "violations": ["minimum-installments"]}]
{'id': 1, 'consumer_id': 10, 'score': 600, 'income': 4000, 'requested_value': 10000, 'installments': 15, 'time': '2019-02-13T10:00:00.000Z'}
root@82c2ddf25046:/# 
```

<br>
<b>-c</b>: just does a system command (may be necessery inside the -loop)

``` shell
root@82c2ddf25046:/# authorize -loop
:> -c
:[sys]> mkdir /logFiles
```

<br>
<b>-form</b>: add an operation like a form:

``` 
root@82c2ddf25046:/# authorize -form
ID: 2
CONSUMER_ID: 15 
SCORE: 600
INCOME: 300
REQUESTED_VALUE: 150
INSTALLMENTS: 20
TIME:
    YEAR: 2020
    MONTH: 02
    DAY: 01
    HOUR: 15
    MINUTE: 15
    SECOND: 5.084
id --> 2
consumer_id --> 15
score --> 600
income --> 300
requested_value --> 150
installments --> 20
time --> 2020-02-01T15:15:5.084Z
Save? [S/N]: s
[{'id': 2, 'violations': []}]
```

<br>
<b>-tests</b>: run tests

``` 
root@82c2ddf25046:/# authorize -tests
```

<br>
<b> -mkdt </b>: creates a data set with random operations.you can provide as many operations as you want as the -mkdt argument and name with the -dtname parameter.

the default quantity is 2 and the name is "dataset.dt"

the data set is saved in the application directory

``` 
root@82c2ddf25046:/# authorize -mkdt 10 -dtname operation_dataset.txt
```

<br>
<br>

To use app without docker just call the `cli.py` instead ` authorize` or make an environment variable 

``` 
$ python3 ./cli.py -f ./dataset.txt
```

</p>

# The application:

<p>
The app has 3 main modules: Operations, Rules and Cli.

Cli calls the Operation that checks specific rules and in general adds Operation on database if valid
</p>

## Cli

`cli.py` consists of 4 parts: constants, support functions, command functions and run_commands functions

``` python
import os
from operations import (
    OPERATIONS, addCreditOperation, isJson
    )
import json

#constants
os_args = os.sys.argv[1:]
sys_args = {}

response_operations = []#history of response_operations
_exclude = []

__DIRNAME__ = os.sys.path[0]

LIST_TYPES_OPERATIONS = {
    "1": addCreditOperation,
}#list whith [type_cmd, Operation_func]

#Suport Functions
def parseArgs(list_args: list) -> dict:
    pass

def addFromFile(filePath):
    pass

#Command Functions
def _f(arg, **kwargs):
    pass

def _save(arg, **kwargs):
    pass

def _tests(arg, **kwargs):
    pass

#Run Commands
def tryAddOperationsWithArgs():
    pass

def run_commands(list_args, **kwargs):
    _cmd = {
        "-f": _f,
        "-save": _save,
        "-tests":_tests,
        "-type": True,

    }#list with all commands

    pass

tryAddOperationsWithArgs()
run_commands(sys_args, operations=OPERATIONS)
#the operations parameter its only to read, 
#all changes are made inside of Operation Functions
```

All cli commands must be registered in *_cmd* with their respective function.

*Commands functions* always receives (arg, list_args,  **kwargs). So if any function needs another parameter provide it in `run_commands()` and get inside the function with *kwargs["another"]*

Some args line like *"-type"* do not call any functions, they just provide parameter, so their value on *_cmd* must be a bool or a str if you just want show a mensagem like.

``` 
root@82c2ddf25046:/# authorize -v
1.0
```

by organization, cmd functions should be start with "_"

## Rules

To create a Rule Function, you need to place the @rule decorator from decorators.py above the role

and your returns must be str with a violation-tag or empty if the operation is valid

``` python
from decorators import rule

#Support Functions
def parse_time(str):
    pass

#Rules
@rule
def name_rule(operation:dict,**kwargs)->dict:
    def violation_logic():
        pass
    
    if violation_logic:
        return "tag-violation" #Output: {...operations, "viloations":["violation-tags"]}
    else:
        return "" #Output: {...operations, "viloations":[]}

```

*Rule Functions* always receives `(operation: dict, ** kwargs)` . Therefore, if any function needs another parameter, it will be provided by the <b>Operation</b> function that calls the <b>Rule</b> and enters the function as `kwargs ["another"]` 

## Operations

All operation functions must have: * list_rules *, * responses * and * operation * as a parameter

<b> Warning: </b> If the Operation Function appends the database, it must be provided as a parameter to the `makeOperations ()` function for double transaction verification

``` python
"""Template Operation Function"""
from rules import name_rule

#Constants
OPERATIONS: dict = {} #dataBase with all valid operations

#Support functions
def isJson(string: str) -> bool:
    pass

def makeOperations(json_operations: str, list_rules: list, database) -> list:
    pass

def verifyRules(operation: dict, rules: list, index: int = 0, **kwargs) -> dict:
    pass

#Operation Functions

def addCreditOperation(json_operations:str)->str:
    list_rules = [name_rule]

    responses = []

    #NOTE: The database provided on makeOperations() its only double transaction checking 
    for line in makeOperations(json_operation, list_rules, database=OPERATIONS):#All specifc parameteres must be declared here
        
        line_transaction = line["transaction"]

        if len(line["violations"])==0:
            #It's only here that make databe changes
            OPERATIONS[line_transaction["id"]] = line_transaction
        
        responses.append({"id":line_transaction["id"],"violations":line["violations"] })
    
    return responses

    
```

## WorkFlow of Command

``` python
input:str: '{ "transaction": { "id": 1, "consumer_id": 10, "score": 600, "income": 4000, "requested_value": 10000,"installments": 15, "time": "2019-02-13T10:00:00.000Z"}}'
```

``` python
database:dict = OPERATIONS
```

``` python
0 _type_operation_:str="1"

1 input:str is provided to cli.py

2 cli.py run LIST_TYPES_OPERATIONS [_type_operation_] (input:str)

2.1 addCreditOperation(input:str)

2.2     makeOperations(input:str, list_rules:list, database=database:dict")# parse input:str to input:dict

2.3         verifyRules(input:dict, list_rules:list)
                input["violations"]:list = []  #valid

                return input:dict #response

2.4         return [input:dict,]#list of all responses

        database[input["transaction"]["id"]:int]:dict = input["transaction"]:dict

2.5     return [{"id": input["transaction"]["id"]:int, "violations":input["violations"]:list}]

3 op:list = [{"id": input["transaction"]["id"]:int, "violations":input["violations"]:list}]

4 [print(str(line:dict).replace("'", '"')) for line:dict in op:list] 

OutPut: {"id":1, "violations":[]}
```

