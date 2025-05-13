def is_age_even(age):
    #option 1: return true if this age is even 0 == 0 -> true 
    #option 2 return false if it is not 1 == 0 -> false
    return ((age % 2) == 0)
    
number1 = 10
number2 = 32

if is_age_even(number1 + number2):
    print("We have found an even number")