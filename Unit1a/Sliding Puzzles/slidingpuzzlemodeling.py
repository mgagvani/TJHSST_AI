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
        print(a)



if __name__ == "__main__":
    puzzle = Puzzle("slide_puzzle_tests.txt", 4)
    print(puzzle)
    puzzle.find_goal()
