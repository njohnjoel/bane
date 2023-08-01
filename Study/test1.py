a=int(input("Enter a value \n"))
b=int(input("Enter b value \n"))

def calc1(a,b):
    c=(a+b)
    d=(a-b)
    e=(a*b)
    f=(a/b)
    return (c,d,e,f)

m,n,o,p=calc1(a,b)

print(m,n,o,p)
