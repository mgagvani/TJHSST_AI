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


if __name__ == "__main__":
    time1 = perf_counter()
    dictionary = get_dictionary("words_06_letters.txt")
    graph, lens = generate_graph(dictionary)
    print(lens)
    print(graph["beagle"])
    time2 = perf_counter()
    print(f"Time to create dictionary was: {time2-time1} seconds")
    print(f"There are {len(dictionary)} words in this dictionary. ")

    args = sys.argv
    path = args[1]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        start, goal = line.split(" ")
        print(f"Start is {start} and goal is {goal}")
