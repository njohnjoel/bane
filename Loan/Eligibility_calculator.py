principal = float(input("Enter the loan amount: "))
interest_rate = float(input("Enter the interest rate (%): "))
years = float(input("Enter the loan term (in years): "))
income = float(input("Enter your annual income: "))

monthly_rate = interest_rate / 1200
months = years * 12

emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
total_amount = emi * months
income_ratio = emi / (income / 12)

if income_ratio <= 0.4:
    print("Congratulations! You are eligible for the loan.")
    print(f"Your monthly EMI would be: {round(emi, 2)}")
    print(f"Total amount payable would be: {round(total_amount, 2)}")
else:
    print("Sorry, you are not eligible for the loan.")
    print(f"Your monthly EMI would be: {round(emi, 2)}")
    print(f"Total amount payable would be: {round(total_amount, 2)}")
    print(f"Your EMI to Income Ratio is: {round(income_ratio, 2)}")