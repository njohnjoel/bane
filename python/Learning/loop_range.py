#loops 

name = "Joel"

#For Loop

for letters in name :
    print(letters)

fruits = ['apple','Orange','Banana']

for fruit in fruits:
    print(fruit)


for i in "Hi, welcome":
    if i == ',':
#        continue
       print(", Is present")
 #       break
    else:
        print(", is not present")



#-------------------- RANGE ------------------------ #

for number in range(45,59,4):
#First Number 45 => Start Point , Second Number 59 => end Point , third number 4 => Number of intervals 
    print(number)


for num in range(5):
    print(num)
    for h in range(2):
        print(h)
else: 
    print ('All numbers are finished')