from treelib import Node, Tree
import sys

# Structure to represent tree nodes in the A* expansion
class TreeNode(object):
    def __init__(self, c_no, c_id, f_value, h_value, parent_id):
        self.c_no = c_no
        self.c_id = c_id
        self.f_value = f_value
        self.h_value = h_value
        self.parent_id = parent_id

# Structure to represent fringe nodes in the A* fringe list
class FringeNode(object):
    def __init__(self, c_no, f_value):
        self.f_value = f_value
        self.c_no = c_no

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    # A utility function to print the constructed MST stored in parent[]
    def printMST(self, parent, d_temp, t):
        # Removed "Edge    Weight" lines to print only the path and cost
        sum_weight = 0
        min1 = 10000
        min2 = 10000
        r_temp = {}  # Reverse dictionary

        for k in d_temp:
            r_temp[d_temp[k]] = k

        for i in range(1, self.V):
            sum_weight = sum_weight + self.graph[i][parent[i]]
            if graph[0][r_temp[i]] < min1:
                min1 = graph[0][r_temp[i]]
            if graph[0][r_temp[parent[i]]] < min1:
                min1 = graph[0][r_temp[parent[i]]]
            if graph[t][r_temp[i]] < min2:
                min2 = graph[t][r_temp[i]]
            if (graph[t][r_temp[parent[i]]] < min2):
                min2 = graph[t][r_temp[parent[i]]]

        return (sum_weight + min1 + min2) % 10000

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in the shortest path tree
    def minKey(self, key, mstSet):
        min_value = sys.maxsize
        min_index = -1
        for vertex in range(self.V):
            if not mstSet[vertex] and key[vertex] < min_value:
                min_value = key[vertex]
                min_index = vertex

        return min_index

    # Function to construct and print MST for a graph
    def primMST(self, d_temp, t):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array to store constructed MST
        key[0] = 0
        mstSet = [False] * self.V
        sum_weight = 10000
        parent[0] = -1  # First node is always the root of MST

        for c in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

        return self.printMST(parent, d_temp, t)

def heuristic(tree, p_id, t, V, graph):
    visited = set()
    visited.add(0)
    visited.add(t)

    if p_id != -1:
        tnode = tree.get_node(str(p_id))
        while tnode.data.c_id != 1:
            visited.add(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))

    l = len(visited)
    num = V - l

    if num != 0:
        g = Graph(num)
        d_temp = {}
        key = 0
        for i in range(V):
            if i not in visited:
                d_temp[i] = key
                key = key + 1

        i = 0
        for i in range(V):
            for j in range(V):
                if i in d_temp and j in d_temp:
                    g.graph[d_temp[i]][d_temp[j]] = graph[i][j]

        mst_weigt = g.primMST(d_temp, t)
        return mst_weigt
    else:
        return graph[t][0]

def checkPath(tree, toExpand, V):
    tnode = tree.get_node(str(toExpand.c_id))
    list1 = list()
    if tnode.data.c_id == 1:
        return 0
    else:
        depth = tree.depth(tnode)
        s = set()
        while (tnode.data.c_id != 1):
            s.add(tnode.data.c_no)
            list1.append(tnode.data.c_no)
            tnode = tree.get_node(str(tnode.data.parent_id))
        list1.append(0)
        if (depth == V) and (len(s) == V) and (list1[0] == 0):
            print("Path complete")
            list1.reverse()
            print("Path: ", list1)  # Print the path here
            return 1
        else:
            return 0

def startTSP(graph, tree, V):
    goalState = 0
    toExpand = TreeNode(0, 0, 0, 0, 0)
    key = 1
    heu = heuristic(tree, -1, 0, V, graph)
    tree.create_node("1", "1", data=TreeNode(0, 1, heu, heu, -1))
    fringe_list = {}
    fringe_list[key] = FringeNode(0, heu)
    key += 1

    while goalState == 0:
        if not fringe_list:
            print("Fringe list is empty. No solution found.")
            return None

        minf = sys.maxsize
        for i in fringe_list.keys():
            if fringe_list[i].f_value < minf:
                toExpand.f_value = fringe_list[i].f_value
                toExpand.c_no = fringe_list[i].c_no
                toExpand.c_id = i
                minf = fringe_list[i].f_value

        h = tree.get_node(str(toExpand.c_id)).data.h_value
        val = toExpand.f_value - h
        path = checkPath(tree, toExpand, V)

        if toExpand.c_no == 0 and path == 1:
            goalState = 1
            cost = toExpand.f_value
            print(f"Cost: {cost}")  # Print the cost
        else:
            del fringe_list[toExpand.c_id]
            for j in range(V):
                if j != toExpand.c_no and graph[toExpand.c_no][j] > 0:
                    h = heuristic(tree, toExpand.c_id, j, V, graph)
                    f_val = val + graph[toExpand.c_no][j] + h
                    fringe_list[key] = FringeNode(j, f_val)
                    tree.create_node(str(toExpand.c_no), str(key), parent=str(toExpand.c_id),
                                     data=TreeNode(j, key, f_val, h, toExpand.c_id))
                    key += 1
    return cost


if __name__ == '__main__':
    V = 4
    graph = [[0, 5, 2, 3], [5, 0, 6, 3], [2, 6, 0, 4], [3, 3, 4, 0]]

    tree = Tree()
    ans = startTSP(graph, tree, V)
    print("Ans is " + str(ans))
