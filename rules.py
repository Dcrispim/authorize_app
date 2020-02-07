from decorators import rule

def parse_time(dt):
    date = dt.split('T')[0].split("-")
    time = dt.split('T')[-1].split(':')
    time[-1] = time[-1][:-1]
    return {"Y":date[0],"M":date[1], "D":date[0], "h":int(time[0]),"m":int(time[1]), "s":float(time[2])}

@rule
def compromised_income(transaction: dict, **kwargs)->str:    
    #When the value of installmets exceeds 30% of income: compromised-income
    if int(transaction["transaction"]["installments"])>0.3*transaction["transaction"]["income"]:
        return "compromised-income"
    else:
        return ""


@rule
def low_score(transaction: dict, **kwargs)->str:    
    #When the value of installmets exceeds 30% of income: compromised-income
    if int(transaction["transaction"]["score"])<200:
        return "low-score"
    else:
        return ""

@rule
def minimum_installments(transaction: dict, **kwargs)->str:    
    #When the value of installmets exceeds 30% of income: compromised-income
    if int(transaction["transaction"]["installments"])<6:
        return "minimum-installments"
    else:
        return ""


@rule
def doubled_transactions(transaction: dict,**kwargs)->str:    
    #When happens two transactions in the same 2 minutes: doubled-transactions
    current_time = parse_time(transaction["transaction"]["time"])
    for dt in kwargs["db_transactions"]:
        dt_time= parse_time(kwargs["db_transactions"][dt]["transaction"]["time"])
        if (current_time["m"]+current_time["s"])-(dt_time["m"]+ dt_time["s"]) <=2:
            return "doubled-transactions"
    
    return ""
