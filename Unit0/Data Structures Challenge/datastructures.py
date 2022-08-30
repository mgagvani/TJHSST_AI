from time import perf_counter

def main():
    f1, f2, f3 = "10kfile1.txt", "10kfile2.txt", "10kfile3.txt"

    with open(f1) as f:
        list1 = [int(line.strip()) for line in f]
        set1 = set(list1)
        dict1 = {i:list1.count(i) for i in set1}

    with open(f2) as f:
        list2 = [int(line.strip()) for line in f]
        set2 = set(list2)
        dict2 = {i:list2.count(i) for i in set2}

    with open(f3) as f:
        list3 = [int(line.strip()) for line in f]
        set3 = set(list3)
        dict3 = {i:list3.count(i) for i in set3}

    ## Problems
    # Problem 1
    print("1: " ,len(set1.intersection(set2)))

    # Problem 2
    count = 0
    set1_ordered = []
    for i, val in enumerate(list1):
        if not val in set1_ordered:
            set1_ordered.append(val)
    for i, val in enumerate(set1_ordered):
        if i%100 == 99:
            count += val
    print("2: ", count)

    # Problem 3
    t = 0
    for value in set3:
        if value in dict1.keys():
            t += dict1[value]
        if value in dict2.keys():
            t += dict2[value]
    print("3: ",t)

    # Problem 4
    print("4: ",sorted(list(set1))[:10])

    # Problem 5
    print("5: ",list(reversed(sorted([num for num in dict2.keys() if dict2[num] > 1])[-10:])))

    # Problem 6
    curridx, previdx, seq = 0, 0, set()
    for i, val in enumerate(list1):
        if val % 53 == 0:
            previdx = curridx
            curridx = i
            seq.add(min(list1[previdx:curridx+1]))
    print("6: ", sum(seq))

        
    


if __name__ == "__main__":
    start = perf_counter()

    main()

    print(f"Total time: {perf_counter() - start} seconds")