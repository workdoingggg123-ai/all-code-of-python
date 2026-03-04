print("this is the code for prime checker")

a = int(input("give the number a : "))

# We must initialize b in case the loop never runs (like if a is 2)
b = a 

for b in range(2, a):
    if a % b == 0:
        print("the number is not prime")
        break
else:
   
    b = a 

if a == b:
    if a > 1:
        print("the number is prime")