from time import perf_counter, time
import sys
from heapq import heappush, heappop, heapify

def main(args):
    f1, f2, f3 = args

    with open(f1) as f:
        list1 = [int(line.strip()) for line in f]
        set1 = set(list1)
        dict1 = {} # {i:list1.count(i) for i in set1}
        for item in list1:
            if item in dict1:
                dict1[item] += 1
            else:
                dict1[item] = 1

    with open(f2) as f:
        list2 = [int(line.strip()) for line in f]
        set2 = set(list2)
        dict2 = {} # {i:list2.count(i) for i in set2}
        for item in list2:
            if item in dict2:
                dict2[item] += 1
            else:
                dict2[item] = 1

    with open(f3) as f:
        list3 = [int(line.strip()) for line in f]
        set3 = set(list3)
        dict3 = {} # {i:list3.count(i) for i in set3}
        for item in list2:
            if item in dict2:
                dict2[item] += 1
            else:
                dict2[item] = 1

    ## Problems
    # Problem 1
    print("1: " ,len(set1.intersection(set2)))


    # Problem 2 (slow - ~0.015)
    count = 0
    set1_ordered = set() # []
    idx = 0
    for i, val in enumerate(list1):
        if not val in set1_ordered:
            set1_ordered.add( (idx, val) )
            idx += 1
    for val in set1_ordered:
        if val[0]%100 == 99:
            count += val[1]
    print("2: ", count)


    # Problem 3
    t = 0 # 308
    for value in set3:
        if value in dict1.keys():
            t += dict1[value]
        if value in dict2.keys():
            t += dict2[value]
    print("3: ",t)


    # Problem 4
    print("4: ",sorted(list(set1))[:10])


    # Problem 5 (kinda slow - 0.007)
    print("5: ",list(reversed(sorted([num for num in dict2.keys() if dict2[num] > 1])[-10:])))

    # Problem 6 (kinda slow - 0.007)
    curridx, seq, heap = 0, set(), []
    for i, val in enumerate(list1): #iterate in the order the sequence was read O(n)
        heappush(heap, val)
        if val % 53 == 0: # trigger                                             O(1)
            curridx = i # this is the index I am at (left most)                 O(1)  
            # _heap = heapify(list1[:curridx+1]) # this is what I have seen so far  O(nlogn)
            idx = 0
            while heap[0] in seq:
                heappop(heap)
            seq.add(heap[idx]) # add to set so no duplicates                     O(1)
    print("6: ", sum(seq))


        
    


if __name__ == "__main__":
    args = sys.argv

    start = perf_counter()

    main(args[1:])

    print(f"Total time: {perf_counter() - start} seconds")