"""List of aplication's rules"""

from decorators import rule

def parse_time(dt:str)->dict:
    date = dt.split('T')[0].split("-")
    time = dt.split('T')[-1].split(':')
    time[-1] = time[-1][:-1]
    return {"Y":date[0],"M":date[1], "D":date[0], "h":int(time[0]),"m":int(time[1]), "s":float(time[2])}

@rule
def compromised_income(operation: dict, **kwargs)->str:    
    """verify when the value of installmets exceeds 30% of income 
    
    Arguments:
        operation {dict} -- operation dict with "installmets" and "income"
    
    Returns:
        str -- "compromised-income" or ""
    """    
    if int(operation["transaction"]["installments"])>0.3*operation["transaction"]["income"]:
        return "compromised-income"
    else:
        return ""


@rule
def low_score(operation: dict, **kwargs)->str:
    """verify when the score is lower than 200 
    
    Arguments:
        operation {dict} -- operation dict with "score"
    
    Returns:
        str -- "low-score" or ""
    """   

    if int(operation["transaction"]["score"])<200:
        return "low-score"
    else:
        return ""

@rule
def minimum_installments(operation: dict, **kwargs)->str: 
    """verify when the istallments value is lower than 6
    
    Arguments:
        operation {dict} -- operation dict with "istallments"
    
    Returns:
        str -- "minimum-installments" or ""
    """   
   
    if int(operation["transaction"]["installments"])<6:
        return "minimum-installments"
    else:
        return ""


@rule
def doubled_transactions(operation: dict,**kwargs)->str:
    """verify when the istallments value is lower than 6
    
    Arguments:
        operation {dict} -- ""
        kwargs["database"] {dict} -- "dict with all operations"
    
    Returns:
        str -- "doubled-transactions" or ""
    """      
    
    transaction = operation["transaction"]

    current_time = parse_time(transaction["time"])

    if "database" not in kwargs.keys():
        raise KeyError("[ERRO:01] Add \"database\" for duplication checking")
    else:
        for dt in kwargs["database"].keys():    
            db_transaction = kwargs["database"][dt]
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
