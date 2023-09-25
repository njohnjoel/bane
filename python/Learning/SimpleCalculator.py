def add (a, b):
    return a+b

def sub (a, b):
    return a-b

def mul (a, b):
    return a*b

def div (a, b):
    return a//b

print("""Select Operation
1. Add
2. Subtract
3. Multiply
4. Divide 
""")


choice = int(input("enter your operation type \n"))
a=int(input("enter number_1 \n"))
b=int(input("enter number_2 \n"))

if choice == 1:
    print(add(a, b))
elif choice == 2:
    print(sub(a, b))
elif choice == 3:
    print(mul(a, b))
elif choice == 4:
    print(div(a, b))
else:
    print("Enter between 1 & 4")
