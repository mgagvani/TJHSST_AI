# Manav Gagvani
# 12/8/22
import sys
from time import perf_counter, sleep
from math import pi, acos, sin, cos
from heapq import heappush, heappop, _heappop_max, heapify
from tkinter import *

def calcd(y1, x1, y2, x2):
    """'
    y1 = lat1, x1 = long1
    y2 = lat2, x2 = long2
    all assumed to be in decimal degrees
    """
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    R = 3958.76  # miles = 6371 km
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    # approximate great circle distance with law of cosines
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def make_graph(
    nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"
):  # default args
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {} 
    _len = len

    with open(nodes, "r") as file1:  # reads in the node locations with node IDs
        for line1 in file1:
            line_array = line1.strip().split(" ")
            nodeLoc[line_array[0]] = [line_array[1], line_array[2]]
    with open(node_city, "r") as file2:  # reads in the city names
        for line2 in file2:
            line_array = line2.strip().split(" ")
            if _len(line_array) == 3:  # if there is a space in the city name
                cityToNode[line_array[1] + " " + line_array[2]] = line_array[0]
                nodeToCity[line_array[0]] = line_array[1] + " " + line_array[2]
            else:
                cityToNode[line_array[1].strip()] = line_array[0]
                nodeToCity[line_array[0]] = line_array[1].strip()
    with open(edges, "r") as file3:
        for line3 in file3:
            line_array = line3.strip().split(" ")
            temp1 = nodeLoc[line_array[0]]  # first node
            temp2 = nodeLoc[line_array[1]]  # second node
            r1 = line_array[0]
            r2 = line_array[1]
            if r1 not in neighbors:
                neighbors[r1] = {
                    r2
                }  # instantiates a dict with the first node as the key and the second node as the value
            else:
                neighbors[r1].add(r2)  # add to the adjacency list
            if r2 not in neighbors:
                neighbors[r2] = {r1}
            else:
                neighbors[r2].add(r1)
            edgeCost[(r1, r2)] = calcd(
                temp1[0], temp1[1], temp2[0], temp2[1]
            )  # tuple is key of edgeCost dict
            edgeCost[(r2, r1)] = calcd(temp1[0], temp1[1], temp2[0], temp2[1])
    for a in neighbors:
        for b in neighbors[a]:
            edgeCost[(a, b)] = calcd(
                nodeLoc[a][0], nodeLoc[a][1], nodeLoc[b][0], nodeLoc[b][1]
            )
            edgeCost[(b, a)] = calcd(
                nodeLoc[a][0], nodeLoc[a][1], nodeLoc[b][0], nodeLoc[b][1]
            )
    for node in nodeLoc:  # checks each
        lat = float(nodeLoc[node][0])  # gets latitude
        long = float(nodeLoc[node][1])  # gets longitude
        modlat = (lat - 10) / 60  # scales to 0-1
        modlong = (long + 130) / 70  # scales to 0-1
        map[node] = [modlat * 800, modlong * 1200]  # scales to fit 800 x 1200 window
    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]


def dist_heuristic(n1, n2, graph):
    return calcd(graph[0][n1][0], graph[0][n1][1], graph[0][n2][0], graph[0][n2][1])

def draw_line(canvas, y1, x1, y2, x2, col, line_width=1):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    try:
        canvas.create_line(x1, 800 - y1, x2, 800 - y2, fill=col, width=line_width)
    except Exception as e:
        print("Tkinter error: ")
        print(e)
        sys.exit(1)


def draw_final_path(ROOT, canvas, path, graph, col="green"):
    # print(path)
    for p in range(len(path) - 1):
        draw_line(canvas, *graph[5][path[p]], *graph[5][path[p + 1]], col, 5)
        ROOT.update()
    sleep(5) # pause for 5 sec
    ROOT.quit() # close the window


def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800")  # sets geometry

    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for n1, n2 in graph[4]:  # graph[4] keys are edge set
        draw_line(canvas, *graph[5][n1], *graph[5][n2], "white")  # graph[5] is map dict
    ROOT.update()

def dijkstra(start, goal, graph):
    ROOT = Tk()  # creates new tkinter window
    ROOT.title(f"Dijikstra - {graph[1][start]} to {graph[1][goal]}")
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    canvas = Canvas(ROOT, background="black")  # sets background color
    draw_all_edges(ROOT, canvas, graph)
    counter = 0

    fringe = []
    closed = {start: (0, [start])}
    heappush(
        fringe, (0, start, [start])
    )  # we still use a heap but we only need to store the cost and the node, not the heuristic
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            path, cost = closed[v[1]][1], v[0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            return path, cost
        for child in graph[3][v[1]]:
            cost = (
                closed[v[1]][0] + graph[4][(v[1], child)]
            )  # cost is the cost of the parent + the cost of the edge
            if child not in closed or closed[child][0] > cost:
                heappush(fringe, (cost, child, v[2] + [child]))
                closed[child] = (cost, v[2] + [child])
                # print("hello")
                # print(*tuple(graph[5][v]), *tuple(graph[5][child]))
                draw_line(canvas, *graph[5][v[1]], *graph[5][child], "OrangeRed2") # star unpacks the list
        counter += 1
        if counter % 6000 == 0:
            ROOT.update()
    return None, None

def dijkstra_dfs(start, goal, graph):
    ROOT = Tk()  # creates new tkinter window
    ROOT.title(f"Dijikstra DFS - {graph[1][start]} to {graph[1][goal]}")
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    canvas = Canvas(ROOT, background="black")  # sets background color
    draw_all_edges(ROOT, canvas, graph)
    counter = 0

    fringe = []
    closed = {start: (0, [start])}
    heappush(
        fringe, (0, start, [start])
    )  # we still use a heap but we only need to store the cost and the node, not the heuristic
    while len(fringe) > 0:
        v = _heappop_max(fringe)
        if v[1] == goal:
            path, cost = closed[v[1]][1], v[0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            return path, cost
        for child in graph[3][v[1]]:
            cost = (
                closed[v[1]][0] + graph[4][(v[1], child)]
            )  # cost is the cost of the parent + the cost of the edge
            if child not in closed or closed[child][0] > cost:
                heappush(fringe, (cost, child, v[2] + [child]))
                closed[child] = (cost, v[2] + [child])
                # print("hello")
                # print(*tuple(graph[5][v]), *tuple(graph[5][child]))
                draw_line(canvas, *graph[5][v[1]], *graph[5][child], "OrangeRed2") # star unpacks the list
        counter += 1
        if counter % 6000 == 0:
            ROOT.update()
    return None, None

def bidirectional_dijkstra(start, goal, graph):
    ROOT = Tk()  # creates new tkinter window
    ROOT.title(f"Bidirectional Dijikstra - {graph[1][start]} to {graph[1][goal]}")
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    canvas = Canvas(ROOT, background="black")  # sets background color
    draw_all_edges(ROOT, canvas, graph)
    # Create dictionaries to store the cost and path of the visited nodes for both directions
    closed_start = {start: (0, [start])}
    closed_goal = {goal: (0, [goal])}

    # Create heaps to store the nodes that still need to be visited for both directions
    fringe_start = [(0, start, [start])]
    fringe_goal = [(0, goal, [goal])]

    # Create a set to store nodes that have been visited in both directions
    intersect = set()

    counter = 0

    while len(fringe_start) > 0 and len(fringe_goal) > 0:
        # Pop the node with the smallest cost from the start heap
        v_start = heappop(fringe_start)
        # If the node has been visited from the other direction, return the path and cost
        if v_start[1] in closed_goal:
            print("found thru start")
            # path = v_start[2] + list(reversed(closed_goal[v_start[1]][1]))
            path = v_start[2] + list(reversed(closed_goal[v_start[1]][1][1:]))
            cost = v_start[0] + closed_goal[v_start[1]][0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            return path, cost
        intersect.add(v_start[1])

        # Iterate over the children of the node
        for child in graph[3][v_start[1]]:
            if child in intersect:
                continue
            cost = closed_start[v_start[1]][0] + graph[4][(v_start[1], child)]
            if child not in closed_start or closed_start[child][0] > cost:
                heappush(fringe_start, (cost, child, v_start[2] + [child]))
                closed_start[child] = (cost, v_start[2] + [child])
                draw_line(canvas, *graph[5][v_start[1]], *graph[5][child], "OrangeRed2") # star unpacks the list


        # Pop the node with the smallest cost from the goal heap
        v_goal = heappop(fringe_goal)
        # If the node has been visited from the other direction, return the path and cost
        if v_goal[1] in closed_start:
            # print("found thru goal")
            path = v_goal[2] + list(reversed(closed_start[v_goal[1]][1])) # + list(reversed(v_goal[2][1:]))
            # print(v_goal[2], closed_start[v_start[1]][1])
            # path = closed_start[v_start[1]][1][1:] + v_goal[2]
            cost = v_goal[0] + closed_start[v_goal[1]][0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            return path, cost
        intersect.add(v_goal[1])

        # Iterate over the children of the node
        for child in graph[3][v_goal[1]]:
            if child in intersect:
                continue
            cost = closed_goal[v_goal[1]][0] + graph[4][(v_goal[1], child)]
            if child not in closed_goal or closed_goal[child][0] > cost:
                heappush(fringe_goal, (cost, child, v_goal[2] + [child]))
                closed_goal[child] = (cost, v_goal[2] + [child])
                draw_line(canvas, *graph[5][v_goal[1]], *graph[5][child], "OrangeRed2") # star unpacks the list


        # Increment the counter and check if it is divisible by 6000
        counter += 1
        if counter % 2000 == 0:
            # Update the Tkinter window
            ROOT.update()

    # If the loop ends without finding the goal node, return None, None
    return None, None


def a_star(
    start, goal, graph, heuristic=dist_heuristic
):  # incase we want to change heuristic later

    ROOT = Tk()  # creates new tkinter window
    ROOT.title(f"A* - {graph[1][start]} to {graph[1][goal]}")
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    canvas = Canvas(ROOT, background="black")  # sets background color
    draw_all_edges(ROOT, canvas, graph)

    counter = 0

    fringe = []
    costs = heuristic(start, goal, graph)
    closed = {start: (0, [start])}  # closed set is keys
    heappush(fringe, (costs, start, [start]))
    while len(fringe) > 0:
        v = heappop(fringe)
        if v[1] == goal:
            path, cost = closed[v[1]][1], v[0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            # print("path: ", path)
            # print("path length: ", len(path))
            return path, cost
        for child in graph[3][v[1]]:
            cost = closed[v[1]][0] + graph[4][(v[1], child)]
            if child not in closed or closed[child][0] > cost:
                cost2 = heuristic(child, goal, graph)
                heappush(fringe, (cost + cost2, child, v[2] + [child]))
                closed[child] = (cost, v[2] + [child])
                draw_line(canvas, *graph[5][v[1]], *graph[5][child], "firebrick1") # star unpacks the list
        counter += 1
        if counter % 2000 == 0:
            ROOT.update()
    return None, None

def reverse_a_star(
    start, goal, graph, heuristic=dist_heuristic
):  # incase we want to change heuristic later

    ROOT = Tk()  # creates new tkinter window
    ROOT.title(f"Reverse A* - {graph[1][start]} to {graph[1][goal]}")
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    canvas = Canvas(ROOT, background="black")  # sets background color
    draw_all_edges(ROOT, canvas, graph)

    counter = 0

    fringe = []
    costs = heuristic(start, goal, graph)
    closed = {start: (0, [start])}  # closed set is keys
    heappush(fringe, (costs, start, [start]))
    while len(fringe) > 0:
        v = _heappop_max(fringe) # pick the WORST node
        if v[1] == goal:
            path, cost = closed[v[1]][1], v[0]
            draw_final_path(ROOT, canvas, path, graph)
            ROOT.destroy()
            # print("path: ", path)
            # print("path length: ", len(path))
            return path, cost
        for child in graph[3][v[1]]:
            cost = closed[v[1]][0] + graph[4][(v[1], child)]
            if child not in closed or closed[child][0] > cost:
                cost2 = heuristic(child, goal, graph)
                heappush(fringe, (cost + cost2, child, v[2] + [child]))
                closed[child] = (cost, v[2] + [child])
                draw_line(canvas, *graph[5][v[1]], *graph[5][child], "firebrick1") # star unpacks the list
        counter += 1
        if counter % 2000 == 0:
            ROOT.update()
    return None, None


def main():
    """
    info about graph
    0: node id: (lat, long)
    1: node id: city name
    2: city name: node id
    3: node id: set of neighbor node ids
    4: (node id, node id): edge cost
    5: scaled coordinates
    """
    SEARCHES = {
    "1": (dijkstra, "Dijikstra"),
    "2": (bidirectional_dijkstra, "Bidirectional Dijikstra"),
    "3": (dijkstra_dfs, "Dijikstra DFS"),
    "4": (a_star, "A*"),
    "5": (reverse_a_star, "Reverse A*"),
    }
    if len(sys.argv) > 1:
        start, goal = sys.argv[1], sys.argv[2]
    else:
        start = input("Start city: ")
        goal = input("Goal city: ")
    cur_time = perf_counter()
    graph = make_graph("./rrNodes.txt", "./rrNodeCity.txt", "./rrEdges.txt")
    if start not in graph[2]:
        raise NameError(f"Given start city ({start}) not in graph")
    if goal not in graph[2]:
        raise NameError(f"Given start city ({goal}) not in graph")
    # for a in graph:
    #     for i, (k,v) in enumerate(a.items()):
    #         if i < 5:
    #             print(k, v)
    print(f"Time to create graph: {(perf_counter() - cur_time)}")

    # Get the search from user input
    search = input("Search type (1: Dijikstra, 2: Bidirectional Dijikstra, 3: Dijikstra DFS, 4: A*, 5: Reverse A*): ")
    if search not in SEARCHES:
        raise NameError(f"Invalid search type ({search})")
    search, name = SEARCHES[search]
    # Run the search
    cur_time = perf_counter()
    path, cost = search(graph[2][start], graph[2][goal], graph)
    print(
        f"{start} to {goal} with {name}: {cost} in {(perf_counter() - cur_time)} seconds."
    )

    # assert cost_0 == cost_1  # sanity check


if __name__ == "__main__":
    main()
