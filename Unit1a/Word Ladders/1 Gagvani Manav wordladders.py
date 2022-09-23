import sys
from collections import deque
from time import perf_counter

def get_dictionary(filePath):
    with open(filePath) as file: # set for o(1) membership
        lines = set([line.strip() for line in file])
    return lines

    [word1[i]==word2[i] for i in range(6)].count(False)==1

def generate_graph(dictionary):
    """
    We want to pre-generate the entire graph once. 
    """
    allchild = {}
    child_lens = []
    for word in dictionary:
        print(".",end="")
        sys.stdout.flush()
        children = set()
        for word2 in dictionary:
            # if [ord(a) ^ ord(b) for a, b in zip(word, word2)].count(0) == 5:
            if [word[i]==word2[i] for i in range(6)].count(False) == 1:
                children.add(word2)
        allchild[word] = children
        child_lens.append(len(children))
    return allchild, child_lens

def generate_graph2(dictionary):
    data = {}
    for word in dictionary:
        for i in range(6):
            newl = list(word); newl[i] = "?"
            news = "".join(newl)
            if news not in data:
                data[news] = [word,]
            else: 
                data[news].append(word)

    # for k in list(data):
    #     if len(data[k]) == 1:
    #         data.pop(k)

    # i = 0
    # for key in data.keys():
    #     print(key, data[key])
    #     i += 1
    #     if i > 50:
    #         break
    graph = {}
    for bin in data.keys():
        for word in (x:=data[bin]):
            if word not in graph:
                graph[word] = set() # create a new set
            for word2 in x:
                if word2 != word:
                    graph[word].add(word2)

    # print(len(graph.keys()))
    # i = 0
    # for key in graph.keys():
    #     print(key, graph[key])
    #     i +=1
    #     if i > 20:
    #         break
    return graph

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return list(reversed(path))

def bfs(start, goal, graph): 
    fringe = deque()
    visited = set()
    fringe.append((start, 0))
    visited.add(start)
    parent = {}
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        if v == goal:
            # return v, _l
            return backtrace(parent, start, goal)
        # print(_l,v, graph[v]); input()
        for child in graph[v]:
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                parent[child] = v
                visited.add(child)
    return -1

def modBFS(graph, s):
    fringe = deque()
    visited = set()
    fringe.append((s, 0))
    visited.add(s)
    while len(fringe) > 0:
        v, _l = fringe.popleft() # DIS IS PARENT
        for child in graph[v]:
            # print(matstr(to_mat(child, size)))  
            if child not in visited:
                fringe.append((child, _l + 1)) # ADD ONE TO PARENT"S LEVEL
                visited.add(child)
    return len(visited)

def solve_puzzles(graph):
    # Problem 1 - 1568
    count1 = 0
    l, long = [], []
    for k,v in graph.items():
        l.append(modBFS(graph, k))
        if l[-1] ==1625:
            long.append(k)
        if len(v) == 0:
            count1 += 1
    print(count1)
    print(max(l))

    # Problem 2 - 1625

    # Problem 3
    a = set(l)
    print(len(a), a, sum(a))
    # Total clumps > 2: 21

    # Problem 4:
    longestlen = 0; longestlist = None
    print(len(long))
    return
    for i, word in enumerate(long):
        for j, word2 in enumerate(long):
            if i+j % 100 == 0:
                print(f"[DEBUG] {i} {j}")

            a = bfs(word, word2, graph)
            if (x:=len(a)) > longestlen:
                longestlen = x
                longestlist = a
                print(longestlen)

    

if __name__ == "__main__":
    args = sys.argv 
    path = args[1]
    dictPath = args[2]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    time1 = perf_counter()
    dictionary = get_dictionary(dictPath)
    graph = generate_graph2(dictionary)
    print(graph["abased"])
    time2 = perf_counter()
    print(f"Time to create dictionary was: {time2-time1} seconds")
    print(f"There are {len(dictionary)} words in this dictionary. ")

    tone = perf_counter()
    for i, line in enumerate(line_list):
        start, goal = line.split(" ")
        path = bfs(start, goal, graph)
        if path == -1:
            print("NO SOLUTION :(")
            continue
        print(f"{i}: Start is {start} and goal is {goal}, pathlength = {len(path)}")
        for a in path:
            print(a)
        print()
    ttwo = perf_counter()

    print(f"Time to solve all: {ttwo - tone} s")

    solve_puzzles(graph)        
