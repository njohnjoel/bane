# Input the employee details
employee_name = input("Enter employee name: ")
employee_id = input("Enter employee ID: ")
basic_salary = float(input("Enter basic salary: "))
hra = 0.5 * basic_salary
pf = 0.12 * basic_salary
tax = 0.05 * basic_salary
special_allowance = 0.2 * basic_salary

# Calculate the net salary
gross_salary = basic_salary + hra + special_allowance
deductions = pf + tax
net_salary = gross_salary - deductions

# Print the payslip
print("Employee Name:", employee_name)
print("Employee ID:", employee_id)
print("Basic Salary:", basic_salary)
print("HRA:", hra)
print("Special Allowance:", special_allowance)
print("PF:", pf)
print("Tax:", tax)
print("Gross Salary:", gross_salary)
print("Deductions:", deductions)
print("Net Salary:", net_salary)