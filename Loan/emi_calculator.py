#Python program to calculate monthly EMI (Equated Monthly Installment)

# EMI Formula = p * r * (1+r)^n/((1+r)^n-1)

# If the interest rate per annum is R% then 
# interest rate per month is calculated using: 

# Monthly Interest Rate (r) = R/(12*100)

# Varaible name details:
# p = Principal or Loan Amount
# r = Interest Rate Per Month
# n = Number of monthly installments

# Reading inputs from user
p = float(input("Loan Amount: "))
R = float(input("Interest rate: "))
n = int(input("Tenure(Months): " ))

# Calculating interest rate per month
r = R/(12*100)

# Calculating Equated Monthly Installment (EMI)
emi = p * r * ((1+r)**n)/((1+r)**n - 1)

print("Monthly EMI = ", emi)