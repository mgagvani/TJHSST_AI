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
            print("5: " , i)
        else:
            i += 2520

    # Problem 6
    print("6: ", sum([i for i in range(1,101)])**2 - sum([i**2 for i in range(1,101)]))

    # Problem 7     
    primes = []
    for i in range(105000):
        if is_prime(i):
            primes.append(i)
    print("7: ", primes[10000])

    # Problem 8 
    currmax = 1
    for i, __value in enumerate(x:=get_problem8_number()):
        result = 1
        for j in range(13):
            try:
                result *= x[i+j]
            except:
                pass
        if result > currmax:
            currmax = result
    print("8: ", currmax)


    # Problem 9
    for i in range(373,377):
        for j in range(190,210):
            for k in range(410,430):
                if i+j+k == 1000 and i**2+j**2 == k**2:
                    a, b, c = i, j, k
                    i = 499; break
    print("9: ", a*b*c)

    # Problem 11 NOT FINISHED TODO
    data = get_problem11_data()
    for i,row in enumerate(data):
        for j, val in enumerate(row):
                pass
    
    # Problem 12
    def get_tri(n):
        return int(n*(n+1)/2)
    def get_numfactors(n):
        s = set()
        for i in range(1, int(n/2)+1):
            if n % i == 0:
                s.add(i)
        return len(s)
    _t = 12375
    while True:
        if get_numfactors(x:=get_tri(_t)) > 500:
            print("12: ", x)
            break
        _t += 1
        

    # Problem 14
    def sequence(num): 
        steps = 1
        while num != 1:
            if num % 2 == 0:
                num = num//2
            else:
                num = num*3 + 1
            steps +=1
        return steps
    longest, longesti = 0, 0; assert sequence(13) == 10
    for i in range(838000,837000, -1):
        if (x:=sequence(i)) > longest:
            longest, longesti = x, i
    print("14: ", longesti)

    # Problem 24
    # import math
    # math.factorial()

    # Problem 28
    def find_sum(limit):
        limit *= limit
        num, add, result = 1, 2, 1
        while num < limit:
            for _i in range(4):
                num += add
                result += num
            add+=2
        return result
    print("28: ", find_sum(1001))

    # Problem 29
    print("29: ", len(set([i**j for i in range(2,101) for j in range(2,101)])))
        
        



def get_problem8_number():
    a = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
    return [int(x) for x in list(a)]

def get_problem11_data():
    data = [[ 8,  2, 22, 97, 38, 15,  0, 40,  0, 75,  4,  5,  7, 78, 52, 12, 50, 77, 91,  8],
            [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48,  4, 56, 62,  0],
            [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30,  3, 49, 13, 36, 65],
            [52, 70, 95, 23,  4, 60, 11, 42, 69, 24, 68, 56,  1, 32, 56, 71, 37,  2, 36, 91],
            [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
            [24, 47, 32, 60, 99,  3, 45,  2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
            [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
            [67, 26, 20, 68,  2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
            [24, 55, 58,  5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
            [21, 36, 23,  9, 75,  0, 76, 44, 20, 45, 35, 14,  0, 61, 33, 97, 34, 31, 33, 95],
            [78, 17, 53, 28, 22, 75, 31, 67, 15, 94,  3, 80,  4, 62, 16, 14,  9, 53, 56, 92],
            [16, 39,  5, 42, 96, 35, 31, 47, 55, 58, 88, 24,  0, 17, 54, 24, 36, 29, 85, 57],
            [86, 56,  0, 48, 35, 71, 89,  7,  5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
            [19, 80, 81, 68,  5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77,  4, 89, 55, 40],
            [ 4, 52,  8, 83, 97, 35, 99, 16,  7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
            [88, 36, 68, 87, 57, 62, 20, 72,  3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
            [ 4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
            [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74,  4, 36, 16],
            [20, 73, 35, 29, 78, 31, 90,  1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57,  5, 54],
            [ 1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52,  1, 89, 19, 67, 48]]
    return data




if __name__ == "__main__":
    oldtime = time.perf_counter() # this is to print out the runtime
    main()
    newtime = time.perf_counter()
    print(f"The program took {newtime-oldtime} secs to run")
    get_problem8_number()
    
