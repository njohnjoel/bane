#-------  If Statements --------#

age =19


if age > 18:
    print ("You can vote in election, Provided you have Voter ID")

elif age ==18:
    print ("You are 18 & Apply for Voter ID")

else:
    print ("you have to wait till 18")


#-------------- AND ------------------#
a,b = 10, 20
if a==10 and b==20:
    print("Correct")
else:
    print("incorrect")

#-------------- OR  ------------------#
a,b = 10, 20
if a==10 or b==10:
    print("Correct")
else:
    print("incorrect")

#-------------- Nesting of "IF"  -----#
a,b = 10, 20
if a ==10 or b==20:
    print("correct")
    if b == 20:
        print("True")