import sys
from time import perf_counter

def factors(x):
    return list(sorted([i for i in range(1,x+1) if x%i==0]))

def load_puzzles(file_path):
    with open(file_path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    # calculate N, subblock_width, subblock_height, symbol_set
    data = []
    for puzzle in line_list:
        N = len(puzzle) ** 0.5
        if int(N ** 0.5) - N ** 0.5 == 0.0: # perfect square
            subblock_height, subblock_width = int(N ** 0.5), int(N ** 0.5)
        else:
            # sub-block width is the smallest factor of N greater than its square root
            for factor in factors(N):
                if factor > N ** 0.5:
                    subblock_width = factor
                    break
            # sub-block height is the greatest factor of N less than its square root
            for factor in reversed(factors(N)):
                if factor < N ** 0.5:
                    subblock_height = factor
                    break
        symbol_set = set([c for c in puzzle if  c not in '.'])
        data.append((N, subblock_width, subblock_height, symbol_set))

    return list(zip(line_list, data))

def print_board(puzzle_state):
    """
    pass  in the full puzzle state which is a tuple
    """
    subblock_width = puzzle_state[1][1]
    subblock_height = puzzle_state[1][2]
    for i in range(subblock_width):
        for j in range(subblock_height):
            print(puzzle_state[0][i*subblock_width+j], end="")
        print()


if __name__ == "__main__":
    puzzles = load_puzzles(sys.argv[1]) # a puzzle state is (string, (data))
    print_board(puzzles[0])
    print(puzzles[0][1])