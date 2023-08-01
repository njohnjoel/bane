NumList=[] 
Even_Sum=0 
Number=int(input("Please enter the Total Number of List Elements:")) 
#Please enter the Total Number of List Elements:5 
for i in range(1,Number+1): 
value=int(input("Please enter the Value of %d Element:"%i)) NumList.append(value) 
Please enter the Value of 1 Element:3 
Please enter the Value of 2 Element:6 
Please enter the Value of 3 Element:7 
Please enter the Value of 4 Element:8 
Please enter the Value of 5 Element:9 
for j in range(Number): 
if(NumList[j]%2==0): 
Even_Sum=Even_Sum+NumList[j] 

print("\n The Sum of Even Numbers in this List= ",Even_Sum)
