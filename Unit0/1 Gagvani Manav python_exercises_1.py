import sys

if sys.argv[1] == "A":
    print(sum([int(i) for i in sys.argv[2:5]]))
elif sys.argv[1] == "B":
    print(sum([int(i) for i in sys.argv[2:]]))
elif sys.argv[1] == "C":
    print([int(num) for num in sys.argv[2:] if int(num) % 3 == 0])
elif sys.argv[1] == "D":
    fib=[1,1]
    for i in range(2, int(sys.argv[2])):
        fib.append(fib[i-2] + fib[i-1])
    print([i for i in fib])
elif sys.argv[1] == "E": #doesnt work
    print([i**2 - 3*i + 2 for i in range(int(sys.argv[2]), int(sys.argv[3])+1)])
elif sys.argv[1] == "F":
    a, b, c = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    if not (a+b > c and b+c>a and a+c>b):
        print(f"Cannot construct a valid triangle given side lengths {a}, {b}, and {c}")
    else:
        s = sum((a, b, c))/2
        print((s*(s-a)*(s-b)*(s-c))**0.5)
elif sys.argv[1] == "G":
    d = {"a":0, "e":0, "i":0, "o":0, "u":0}
    for i, char in enumerate((string:=sys.argv[2].lower())):
        if char in d.keys(): 
            d[char] += 1
    print(d)


        

