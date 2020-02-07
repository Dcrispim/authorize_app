import os
from main import addTransaction
import json

sys_args = os.sys.argv[1:]
args = {}

operations = []
_exclude = []
for i in range(len(sys_args)):
    if sys_args[i][0]=='-' and sys_args[i+1][0]!='-':
        args[sys_args[i]]=sys_args[i+1]
        _exclude.append(sys_args[i+1])
    elif sys_args[i] not in _exclude:
        args[i]=sys_args[i]



for i in [addTransaction(args[a]) for a in args.keys() if type(a)==int ]:
    operations.append(i)
    print(i)

if "-json" in args.keys():
    with open(args['-json'],'r') as File:
        print(json.load(File))
        for transaction in json.load(File):
            print(transaction)
            try:
                print(addTransaction(str(transaction).replace("'",'"')))
            except:
                print('Erro')


if "-f" in args.keys():
    with open(args['-f'],'r') as File:
        for line in File.readlines():
            transaction = addTransaction(line)
            if transaction:
                operations.append(transaction)
            print(transaction)


if "-save" in args.keys():
    with open(args['-save'],'w') as File:
        File.write(str(operations).replace("'",'"'))