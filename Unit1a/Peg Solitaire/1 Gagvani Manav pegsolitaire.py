'''
https://www.pegsolitaire.org/ 
Play "Triangular5 (15 Holes) variant
'''

from collections import deque
from genericpath import exists

NEIGHBOURS = {
1 : {2, 12}, 
2 : {1, 12, 23, 3}, 
3 : {2, 23, 34, 4},
4 : {3, 34, 45, 5},
5 : {4, 45},

12 : {1, 123, 2, 23},
23 : {12, 123, 234, 34, 3, 2},
34 : {23, 234, 345, 45, 4, 3},
45 : {34, 345, 5, 4},

123 : {12, 1234, 234, 23},
234 : {123, 1234, 2345, 345, 34, 23},
345 : {234, 2345, 45, 34},

1234: {123, 12345, 2345, 234},
2345: {1234, 12345, 345, 234}, 

12345: {1234, 2345}
}

JUMPS = {
    (1, 123)     : 12,
    (1, 3)       : 2,
    (2, 234)     : 23,
    (2, 4)       : 3,
    (3, 1)       : 2,
    (3, 5)       : 4,
    (3, 123)     : 23,
    (3, 345)     : 34,
    (4, 2)       : 3,
    (4, 234)     : 23,
    (5, 345)     : 45,
    (5, 3)       : 4,
  
    (12, 34)     : 23,
    (12, 1234)   : 123,
    (23, 45)     : 34,
    (23, 2345)   : 234,
    (34, 1234)   : 234,
    (34, 12)     : 23,
    (45, 2345)   : 345,
    (45, 23)     : 34,
  
    (123, 1)     : 12,
    (123, 3)     : 23,
    (123, 345)   : 234,
    (123, 12345) : 1234,
    (234, 2)     : 23,
    (234, 4)     : 34,
    (345, 5)     : 45,
    (345, 3)     : 34,
    (345, 12345) : 2345,
    (345, 123)   : 234,
    
    (1234, 12)   : 123, 
    (1234, 34)   : 234,
    (2345, 23)   : 234,
    (2345, 45)   : 345,

    (12345, 123) : 1234,
    (12345, 345) : 2345
}

JUMPSPOS = { # start : {(end, jump), (end, jump)}
    1 : frozenset(((123 ,  12),(3    , 2))),
    2 : frozenset(((234   ,23),(4     ,3))),
    3 : frozenset(((1     ,2),(5     ,4),(123   ,23),(345   ,34))),
    4 : frozenset(((2     ,3),(234   ,23))),
    5 : frozenset(((345   ,45),(3     ,4))),
  
    12 :  frozenset(((34  ,  3),(1234 , 23))),
    23 :  frozenset(((45   , 4),(2345 , 34))),
    34 :  frozenset(((1234 , 234),(12   , 3))),
    45 :  frozenset(((2345 , 345),(23   , 34))),
  
    123 : frozenset(((1 ,   12),(3  ,  23),(345 , 234),(12345, 1234))),
    234 : frozenset(((2    ,23),(4    ,34))),
    345 : frozenset(((5    ,45),(3    ,34),(12345 ,2345),(123  ,234))),

    1234: frozenset(((12,  23),(34 , 34))),
    2345: frozenset(((23,  34),(45 , 45))),

    12345: frozenset(((123, 234),(345, 345)))
}

START = frozenset((1, 2, 3, 4, 5, 12, 23, 34, 45, 123, 234, 345, 1234, 2345))
END = frozenset((12345,))

def get_children(state):
    children = []

    # iterate over each item
    for position in state:
        # look it up in JUMPS
        # key = list(JUMPS.keys())[key_ones.index(position)]
        '''
        keys =  [x for i, x in enumerate(key_ones) if x == position]
        # TODO FIX
        # The problem is that there are multiple paths for each possible starting position
        # For instance, 123 --> (1, 3, 12345, 345)
        for i, x in enumerate(list(JUMPS.keys())):
            print(i,x)
        print(keys, "keys")
        '''
        keys = JUMPSPOS[position]
        for key in keys: # (position: k0, k1 --> current: end, jumped
            # print(position, key, keys, state)
            # remove value
            # if current exists and jump exists and end does not exist because it wil go there
            if (position in state) and (key[1] in state) and (key[0] not in state):
                    # print(f"curr: {position}, jump: {key[1]}, end: {key[0]}, state: {state}")
                    a = list(state)
                    a.remove(key[1]) # remove the place we jumped over
                    a.remove(position) # remove the place where we jumped from
                    a.append(key[0]) # add the place we jumped to because its not there yet
                    children.append(frozenset(a))
    
    return children

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return list(reversed(path))

def search(start, type="BFS"): 
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    parent = {}
    while len(fringe) > 0:
        if type == "BFS":
            v, _l = fringe.popleft() # DIS IS PARENT
        elif type == "DFS":
            v, _l = fringe.pop() # DIS IS PARENT
        else: 
            print("Unsupported search algorithm")
            return -2
        if v == END:
            # return v, _l
            return backtrace(parent, start, END)
        # print(_l,v, graph[v]); input()
        for child in get_children(v):
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                parent[child] = v
                visited.add(child)
    return -1    
        




def display(state): # state is of type frozenset
    a = list(sorted(state, key=lambda b : len(str(b)), reverse=True))
    levels = {5: set(), 1: set(), 2: set(), 3: set(), 4: set()}
    for val in a:
        levels[len(str(val))].add(val)

    for k in reversed(sorted(levels.keys())):
        for a in sorted(levels[k]):
            print(" " * k, end = "")
            print(a, end=" "*(5-k))
        print()


if __name__ == "__main__":
    bfs_path = search(START)
    print("DISPLAYING PATH FOR BREADTH FIRST SEARCH")
    for a in bfs_path:
        display(a)
        print()

    dfs_path = search(START, "DFS")
    print("DISPLAYING PATH FOR DEPTH FIRST SEARCH")
    for b in dfs_path:
        display(b)
        print()


    