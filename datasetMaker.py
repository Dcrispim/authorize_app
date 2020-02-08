from random import randint

def makeDataset(limit=500):
    operation_template = {
            "transaction": {
                "id": int,
                "consumer_id": int,
                "score": int,
                "income": int,
                "requested_value": int,
                "installments": int,
                "time": "2019-02-13T10:00:00.000Z",
            }
            
        }
    dataset= []
    for line in range(limit):
        operation = {"transaction": {
                "id": randint(1,1000),
                "consumer_id": randint(1,1000),
                "score": randint(0,300),
                "income": randint(0,10000),
                "requested_value": randint(0,10000),
                "installments": randint(0,500),
                "time": f"{randint(1900,2020)}-{randint(1,12)}-{randint(1,31)}T{randint(0,23)}:{randint(0,59)}:{randint(0,59)}.{randint(0,999):>0}Z",
            }
        }

        dataset.append(operation)
        if randint(0,100)%3 ==0:
            dataset.append(operation)
    return dataset

with open("dataset.dt",'w') as File:
    File.write('\n'.join([str(line) for line in makeDataset()]).strip().replace("'",'"'))