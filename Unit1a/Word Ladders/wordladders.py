import sys
from collections import deque
from time import perf_counter

def get_dictionary(filePath):
    with open(filePath) as file: # set for o(1) membership
        lines = set([line.strip() for line in file])
    return lines




if __name__ == "__main__":
    time1 = perf_counter()
    dictionary = get_dictionary("words_06_letters.txt")
    time2 = perf_counter()
    print(f"Time to create dictionary was: {time2-time1} seconds")
    print(f"There are {len(dictionary)} words in this dictionary. ")

    args = sys.argv
    path = args[1]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i, line in enumerate(line_list):
        pass
