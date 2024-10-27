from collections import defaultdict
from queue import Queue, PriorityQueue

# đọc dữ liệu từ file txt
def read_txt(file):
    size = int(file.readline())
    start, goal = [int(num) for num in file.readline().split(' ')]
    matrix = [[int(num) for num in line.split(' ')] for line in file]
    return size, start, goal, matrix

# chuyển ma trận kề thành danh sách kề
def convert_graph(a):
    adjList = defaultdict(list)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == 1:
                adjList[i].append(j)
    return adjList

# chuyển ma trận kề thành danh sách kề có trọng số
def convert_graph_weight(a):
    adjList = defaultdict(list)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != 0:
                adjList[i].append((j, a[i][j]))
    return adjList

# Class Tree_Search chứa các thuật toán BFS, DFS, UCS
class Tree_Search:
    def __init__(self, graph):
        self.graph = graph

    def bfs(self, start, end):
        visited = set()
        frontier = Queue()
        frontier.put(start)
        visited.add(start)
        parent = {start: None}
        path_found = False

        while not frontier.empty():
            current_node = frontier.get()
            if current_node == end:
                path_found = True
                break
            for node in self.graph[current_node]:
                if node not in visited:
                    frontier.put(node)
                    parent[node] = current_node
                    visited.add(node)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
        return path

    def dfs(self, start, end):
        visited = set()
        frontier = []
        frontier.append(start)
        visited.add(start)
        parent = {start: None}
        path_found = False

        while frontier:
            current_node = frontier.pop()
            if current_node == end:
                path_found = True
                break
            for node in self.graph[current_node]:
                if node not in visited:
                    frontier.append(node)
                    parent[node] = current_node
                    visited.add(node)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
        return path

    def ucs(self, start, end):
        frontier = PriorityQueue()
        frontier.put((0, start))
        visited = []
        parent = {start: None}
        cost_dict = {start: 0}
        path_found = False

        while not frontier.empty():
            current_w, current_node = frontier.get()
            visited.append(current_node)
            if current_node == end:
                path_found = True
                break
            for neighbor, weight in self.graph[current_node]:
                new_cost = current_w + weight
                if neighbor not in visited and (neighbor not in cost_dict or new_cost < cost_dict[neighbor]):
                    cost_dict[neighbor] = new_cost
                    frontier.put((new_cost, neighbor))
                    parent[neighbor] = current_node

        path = []
        if path_found:
            node = end
            path.append(node)
            while parent[node] is not None:
                node = parent[node]
                path.append(node)
            path.reverse()

        return cost_dict[end], path if path_found else None

if __name__ == "__main__":
    # Đọc file Input.txt và InputUCS.txt
    file_1 = open("Input.txt", "r")
    file_2 = open("InputUCS.txt", "r")
    size_1, start_1, goal_1, matrix_1 = read_txt(file_1)
    size_2, start_2, goal_2, matrix_2 = read_txt(file_2)
    file_1.close()
    file_2.close()

    graph_1 = convert_graph(matrix_1)
    graph_2 = convert_graph_weight(matrix_2)

    # Tạo instance Tree_Search và thực thi các thuật toán
    tree_search_bfs_dfs = Tree_Search(graph_1)
    tree_search_ucs = Tree_Search(graph_2)

    # Thực thi thuật toán BFS
    result_bfs = tree_search_bfs_dfs.bfs(start_1, goal_1)
    result_bfs = [x + 1 for x in result_bfs]
    print("Kết quả sử dụng thuật toán BFS: \n", result_bfs)

    # Thực thi thuật toán DFS
    result_dfs = tree_search_bfs_dfs.dfs(start_1, goal_1)
    result_dfs = [x + 1 for x in result_dfs]
    print("Kết quả sử dụng thuật toán DFS: \n", result_dfs)

    # Thực thi thuật toán UCS
    cost, result_ucs = tree_search_ucs.ucs(start_2, goal_2)
    result_ucs = [x + 1 for x in result_ucs]
    print("Kết quả sử dụng thuật toán UCS: \n", result_ucs, "với tổng chi phí là", cost)
