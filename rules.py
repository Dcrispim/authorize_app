from decorators import rule

def parse_time(dt):
    date = dt.split('T')[0].split("-")
    time = dt.split('T')[-1].split(':')
    time[-1] = time[-1][:-1]
    return {"Y":date[0],"M":date[1], "D":date[0], "h":int(time[0]),"m":int(time[1]), "s":float(time[2])}

@rule
def compromised_income(operation: dict, **kwargs)->str:    
    #When the value of installmets exceeds 30% of income: compromised-income
    if int(operation["transaction"]["installments"])>0.3*operation["transaction"]["income"]:
        return "compromised-income"
    else:
        return ""


@rule
def low_score(transaction: dict, **kwargs)->str:    
    #When the score is lower than 200
    if int(transaction["transaction"]["score"])<200:
        return "low-score"
    else:
        return ""

@rule
def minimum_installments(operation: dict, **kwargs)->str:    
    #When the value of installmets exceeds 30% of income: compromised-income
    if int(operation["transaction"]["installments"])<6:
        return "minimum-installments"
    else:
        return ""


@rule
def doubled_transactions(operation: dict,**kwargs)->str:    
    #When happens two transactions in the same 2 minutes: doubled-transactions
    transaction = operation["transaction"]

    current_time = parse_time(transaction["time"])

    if "db_operations" not in kwargs.keys():
        raise KeyError("Add \"db_operations\" for duplication checking")
    else:

        for dt in kwargs["db_operations"]:
            db_transaction = kwargs["db_operations"][dt]["transaction"]
            dt_time= parse_time(db_transaction["time"])
            if (current_time["m"]+current_time["s"])-(dt_time["m"]+ dt_time["s"]) <=2:
            
                db = {}
                current ={}
                
                db.update(db_transaction)
                current.update(transaction)

                db["time"] = None
                current["time"] = None
                
                if str(db)==str(current):
                    return "doubled-transactions"
        
    return ""
