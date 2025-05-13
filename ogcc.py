"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

def get_min_payment(balance, fees=0):
    """Computes the minimum credit card payment. 
    Args:
        balance (int or float) : the total amount in the account that is left to pay
        fees (float) : the fees associated with the credit card account with a default 
        value of 0
    Returns:
        min_payment (int or float): The minimum payment the user is required to pay. If the calculated payment is less than 25, it returns 25.
    """
    
    m = 0.02 # percent of the balance that needs to be paid with a constant value of .02
    
    # minimum payment formula
    min_payment = ((balance * m) + fees)
    
    
    if min_payment <= 25: 
        return 25
    else:
        return min_payment

def interest_charged(balance, apr):
    """Computes the amount of interest
    Args:
       balance (int or float) : the total amount in the account that is left to pay
        apr (int) : the annual percentage rate 
    Returns:
        interest ()
    """
    a = (apr / 100) #converting apr into decimal form 
    year = 365
    days = 30
    interest = (a / year) * balance * days
    #i = interest
    return interest

def remaining_payments(balance, apr, targetamount=0, credit_line=5000, fees=0):
    """Computes the minimum credit card payment. 
    Args:
        balance (int or float) : the total amount in the account that is left to pay
        fees (int) : the fees associated with the credit card account with a default 
        value of 0
        apr (int) : the annual percentage rate 
        targetamount 
        credit_line (int): the maximum amount of balance  an account holder can keep
        in their account   
         fees (float) : the fees associated with the credit card account with a default 
        value of 0
    Returns:    
    """

        
    paymentcounter = 0 # represents # of payments to be made
    # represents # of months balance remains over 25,50,75 percent
    balancecounter25 = 0 # of months balance remains over 25
    balancecounter50 = 0 # of months balance remains over 50
    balancecounter75 = 0 # of months balance remains over 75
    while balance > 0: 
        if targetamount is None: # checking if targetamount parameter was passed in as None
            payment_amount = get_min_payment(balance, fees)
        else:
            payment_amount = targetamount
        
        balance_payment = payment_amount - (interest_charged(balance, apr))
        updated_balance = balance - balance_payment
        balance = updated_balance
        #if balance payment is negative the following message will be printed and the program will exit.
        if balance_payment < 0: 
           print("This card balance will never be paid off.")
           sys.exit()
        
        #updating balance counter if balance is over 75,50 25 percent of the credit line
        if balance > (credit_line * 0.75):  # 75% of the credit line
            balancecounter75 += 1
            balancecounter50 += 1
            balancecounter25 += 1
        elif balance > (credit_line * 0.50):  # 50% of the credit line
            balancecounter50 += 1
            balancecounter25 += 1
        elif balance > (credit_line * 0.25):  # 25% of the credit line
            balancecounter25 += 1
        paymentcounter += 1 #increasing # of payments 
        #returning updated counters as a tuple
    return paymentcounter, balancecounter25, balancecounter50, balancecounter75
        
    
def main(balance, apr, targetamount=0, credit_line=5000,fees=0):
    """_summary_
    
    """
    
    
    pays_minimum = False 
    
    #if the user does not specify a target amount the minimum payment is set to true 
    if targetamount is None:
        pays_minimum = True
    elif targetamount < get_min_payment(balance, fees=0):
        print("Your target payment is less than the minimum payment for this credit card.")
        sys.exit()
    
    #unpacking remaining_payments tuple
    paymentcounter, balancecounter25, balancecounter50, balancecounter75 = remaining_payments(balance, apr, targetamount, credit_line, fees)
    
    #displaying recommended minimum payment to user
    #min_payment = get_min_payment(balance, fees=0)
    print("hellO")
    
    if pays_minimum == True:
       print(f"If you pay the minimum payments each month, you will pay off the balance in {paymentcounter} payments.")
    else:
        print(f"If you make payments of ${targetamount}, you will pay off the balance in {paymentcounter} payments.")
        
    return (f"You will spend a total of {balancecounter25} months over 25% of the credit line. \n You will spend a total of {balancecounter50} months over 50% of the credit line. \n You will spend a total of {balancecounter75} months over 75% of the credit line.")
        
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APRpython hw1.py 5_000 10 17_000 --payment 340 --fees 20 must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    result = (main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))
    print(result)