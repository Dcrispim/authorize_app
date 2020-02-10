#Get started:


## making Docker Container 
To start go to de directory of application and open terminal.

type:
*root access may needed*
```
docker build . -t authorize_app:1.0
```

next run the container:

```
docker build run -it authorize_app:1.0
```

Inside the container use the commands bellow to make the operations:

<b>-type</b>: set operation <small>(default is "1": Credit Operation)</small>
*now the app has only one, but more can be added*

```
root@173203a44050:/# authorize -type 1
```
<br>
<b>-f</b>: run the operation on file provided

to use -f each line of file must be a json line

WARNING: the command -f don't read *.json files
```
root@173203a44050:/# authorize -f /app/dataset.txt
```
<br>

<b>-save</b>: save the operation response on path provided
```
root@173203a44050:/# authorize f /app/dataset.txt -save /app/ops.log
```
<br>
<b>-append</b>: save the operation on path provided
```
root@173203a44050:/# authorize -f /app/dataset.txt -append /app/ops.log
```
<br>

<b>-loop</b>: just start a loop to facilitate the continuous manual use

*all commands are functional inside the loop*
```
root@b08b4609608b:/# authorize -loop
:> <b>-f</b> line
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
```
root@82c2ddf25046:/# authorize -loop
:> -c
:[sys]> mkdir /logFiles
```
<br>
<b>-form</b>: add a operation like a form:
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
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
root@82c2ddf25046:/# 
```



##Rules
For make a Rule Function must put the decorator *@rule* from `decorators.py` above of the function.

```python
"""Template Rule Function"""
@rule
def name_rule(operation:dict,**kwargs)->dict:
    def violation_logic():
        pass
    
    if violation_logic:
        return "tag-violation" #Output: {...operations, "viloations":["tag-violations"]}
    else:
        return "" #Output: {...operations, "viloations":[]}


```

##Operations
The Operation Functions are made like template bellow.

All Operation Functions must have: *list_rules*, *responses* and *operation* as parameter




<b>Warning:</b> If the Operation Function appends the database, it must be provide as a parameter  to  `makeOperations()` function for double transaction verification

```python
"""Template Operation Function"""
from rules import name_rule

OPERATIONS: dict = {} #dataBase with all valid operations

def Operation(operation:str)->str:
    list_rules = [name_rule]

    responses = []

    for line in makeOperations(json_operation, list_rules, database=OPERATIONS):
        line_transaction = line["transaction"]

        if len(line["violations"])==0:
            OPERATIONS[line_transaction["id"]] = line_transaction
        
        responses.append({"id":line_transaction["id"],"violations":line["violations"] })
    
    return responses

    
```

##Cli

##Docker

##Tests