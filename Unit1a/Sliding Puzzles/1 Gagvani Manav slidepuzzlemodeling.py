import sys
import time

class Puzzle:
    def __init__(self, path, index):
        with open(path) as fileReader:
            line_list = [line.strip() for line in fileReader]
            line = line_list[index]

        self.size, self.pstr = line.split()
        self.size = int(self.size)

    def to_matrix(self):
        mat = []
        for i in range(self.size):
            mat.append([])
            for j in range(self.size):
                mat[-1].append(self.pstr[i*self.size + j])
        return mat

    def to_str(self, mat):
        s = ""
        for row in mat:
            for val in row:
                s += val
        return s

    def __str__(self):
        s = ""
        for row in self.to_matrix():
            for val in row:
                s += val + " "
            s += "\n"
        return s

    def find_goal(self):
        a = sorted(self.pstr)[1:]
        a.append(".")
        return "".join(a)

    def swap(self, sourcei, sourcej, desti, destj):
        mat = self.to_matrix()
        source = mat[sourcei][sourcej]
        dest = mat[desti][destj]
        mat[sourcei][sourcej] = dest
        mat[desti][destj] = source
        return self.to_str(mat)

    def get_children(self):
        children = []
        mat = self.to_matrix()
        # find the dot
        for i, row in enumerate(mat):
            for j, val in enumerate(row):
                if val == ".":
                    di, dj = i, j
                    break

        # horizontal swapping
        if dj == 0: # swap with right neighbour
            children.append(self.swap(di, dj, di, dj+1))

        elif dj == len(mat[0])-1: # swap with left neighbour 
            children.append(self.swap(di, dj, di, dj-1))

        else: # swap with both neigubours
            children.append(self.swap(di, dj, di, dj+1))
            children.append(self.swap(di, dj, di, dj-1))

        # vertical swapping
        if di == 0: # swap with below neighbour
            children.append(self.swap(di, dj, di+1, dj))

        elif di == len(mat[0])-1: # swap with above 
            children.append(self.swap(di, dj, di-1, dj))

        else: # swap with both neigubours
            children.append(self.swap(di, dj, di+1, dj))
            children.append(self.swap(di, dj, di-1, dj))

        return children


if __name__ == "__main__":
    a = time.perf_counter()
    args = sys.argv
    path = args[1]

    with open(path) as fileReader:
        line_list = [line.strip() for line in fileReader]

    for i in range(len(line_list)):
        puzzle = Puzzle(args[1], i)
        print(f"Line {i} start state:")
        print(puzzle)
        print(f"Line {i} goal state: {puzzle.find_goal()}")
        print(f"Line {i} children: {puzzle.get_children()}")
        print()

