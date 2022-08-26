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
    print("1: " ,len(set1.union(set2)))

    # Problem 2
    


if __name__ == "__main__":
    start = perf_counter()

    main()

    print(f"Total time: {perf_counter() - start} seconds")