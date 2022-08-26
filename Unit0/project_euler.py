# imports will go here if needed
import time

def is_prime(x):
    if x <= 1: return False
    if x == 2: return True
    if x%2 == 0: return False
    for i in range(3, int(x**0.5)+1, 2):  
        if x%i == 0:
            return False
    return True

def gcd(a, b):
    if not a:
        return b
    elif not b:
        return a
    else:
        if a==b:
            return b
        elif(a > b):
            return gcd(a-b, b)
        else:
            return gcd(a, b-a)

def main():
    # Problem 1
    print("1: " , sum([x for x in range(1000) if x%3==0 or x%5==0]))

    # Problem 2
    fib=[1,1]
    for i in range(2, 34):
        fib.append(fib[i-2] + fib[i-1])
    print("2: " , + sum([i for i in fib if i%2==0]))

    # Problem 3
    max = -1
    for i in range(int(600851475143**0.5)+1,1, -2):
        if is_prime(i) and 600851475143%i==0:
            max = i
            break
    print("3: ", max)

    # Problem 4
    max = -1
    for i in range(900,1000):
        for j in range(900,1000):
            if str((a:=i*j)) == str(a)[::-1]:
                max = a
    print("4: ", max)

    # Problem 5
    solved = False
    i = 2520 # we have already established this is biig multiple for 10
    while not solved:
        if all([i%j==0 for j in range(1,20)]):
            solved = True
            print("4: " , i)
        else:
            i += 2520

    # Problem 6
    print(sum([2]))
            


    

if __name__ == "__main__":
    oldtime = time.perf_counter() # this is to print out the runtime
    main()
    newtime = time.perf_counter()
    print(f"The program took {newtime-oldtime} secs to run")
    
