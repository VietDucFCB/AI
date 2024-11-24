from collections import defaultdict
from queue import Queue, PriorityQueue
import math
from matplotlib import pyplot as plt

# Classes: Point, Edge, Graph (giữ nguyên từ phiên bản gốc)
class Point(object):
    def __init__(self, x, y, polygon_id=-1):
        self.x = x
        self.y = y
        self.polygon_id = polygon_id
        self.g = 0
        self.pre = None

    def rel(self, other, line):
        return line.d(self) * line.d(other) >= 0

    def can_see(self, other, line):
        l1 = self.line_to(line.p1)
        l2 = self.line_to(line.p2)
        d3 = line.d(self) * line.d(other) < 0
        d1 = other.rel(line.p2, l1)
        d2 = other.rel(line.p1, l2)
        return not (d1 and d2 and d3)

    def line_to(self, other):
        return Edge(self, other)

    def heuristic(self, other):
        return euclid_distance(self, other)

    def __eq__(self, point):
        return point and self.x == point.x and self.y == point.y

    def __ne__(self, point):
        return not self.__eq__(point)

    def __lt__(self, point):
        return hash(self) < hash(point)

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()

    def __repr__(self):
        return "(%d, %d)" % (self.x, self.y)

class Edge(object):
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def get_adjacent(self, point):
        if point == self.p1:
            return self.p2
        if point == self.p2:
            return self.p1

    def d(self, point):
        vect_a = Point(self.p2.x - self.p1.x, self.p2.y - self.p1.y)
        vect_n = Point(-vect_a.y, vect_a.x)
        return vect_n.x * (point.x - self.p1.x) + vect_n.y * (point.y - self.p1.y)

    def __str__(self):
        return "({}, {})".format(self.p1, self.p2)

    def __contains__(self, point):
        return self.p1 == point or self.p2 == point

    def __hash__(self):
        return self.p1.__hash__() ^ self.p2.__hash__()

    def __repr__(self):
        return "Edge({!r}, {!r})".format(self.p1, self.p2)

class Graph:
    def __init__(self, polygons):
        self.graph = defaultdict(set)
        self.edges = set()
        self.polygons = defaultdict(set)
        pid = 0
        for polygon in polygons:
            if len(polygon) == 2:
                polygon.pop()
            if polygon[0] == polygon[-1]:
                self.add_point(polygon[0])
            else:
                for i, point in enumerate(polygon):
                    neighbor_point = polygon[(i + 1) % len(polygon)]
                    edge = Edge(point, neighbor_point)
                    if len(polygon) > 2:
                        point.polygon_id = pid
                        neighbor_point.polygon_id = pid
                        self.polygons[pid].add(edge)
                    self.add_edge(edge)
                if len(polygon) > 2:
                    pid += 1

    def get_adjacent_points(self, point):
        return list(filter(None.__ne__, [edge.get_adjacent(point) for edge in self.edges]))

    def can_see(self, start):
        see_list = list()
        
        # Nếu điểm start thuộc một đa giác
        if start.polygon_id != -1:
            # Thêm các điểm kề với start trong cùng đa giác
            current_polygon_points = self.get_polygon_points(start.polygon_id)
            for point in self.get_adjacent_points(start):
                if point in current_polygon_points:
                    see_list.append(point)
            
            # Kiểm tra tầm nhìn tới các điểm của đa giác khác
            for point in self.get_points():
                if point != start and point.polygon_id != start.polygon_id:
                    path_clear = True
                    path_line = Edge(start, point)
                    
                    # Kiểm tra giao cắt với tất cả các đa giác
                    for polygon in self.polygons.values():
                        for edge in polygon:
                            if (edge.p1 != start and edge.p2 != start and 
                                edge.p1 != point and edge.p2 != point):
                                if do_edges_intersect(path_line, edge):
                                    path_clear = False
                                    break
                        if not path_clear:
                            break
                    
                    if path_clear:
                        see_list.append(point)
        else:
            # Nếu điểm start không thuộc đa giác nào (điểm start hoặc goal)
            for point in self.get_points():
                if point != start:
                    path_clear = True
                    path_line = Edge(start, point)
                    
                    for polygon in self.polygons.values():
                        for edge in polygon:
                            if (edge.p1 != start and edge.p2 != start and 
                                edge.p1 != point and edge.p2 != point):
                                if do_edges_intersect(path_line, edge):
                                    path_clear = False
                                    break
                        if not path_clear:
                            break
                    
                    if path_clear:
                        see_list.append(point)
        
        return see_list

   
    def get_polygon_points(self, index):
        point_set = set()
        for edge in self.polygons[index]:
            point_set.add(edge.p1)
            point_set.add(edge.p2)
        return point_set

    def get_points(self):
        return list(self.graph)

    def get_edges(self):
        return list(self.edges)

    def add_point(self, point):
        self.graph[point].add(point)

    def add_edge(self, edge):
        self.graph[edge.p1].add(edge)
        self.graph[edge.p2].add(edge)
        self.edges.add(edge)

    def __contains__(self, item):
        if isinstance(item, Point):
            return item in self.graph
        if isinstance(item, Edge):
            return item in self.edges
        return False

    def __getitem__(self, point):
        if point in self.graph:
            return self.graph[point]
        return set()

    def __str__(self):
        res = ""
        for point in self.graph:
            res += "\n" + str(point) + ": "
            for edge in self.graph[point]:
                res += str(edge)
        return res

    def __repr__(self):
        return self.__str__()

    def h(self, point):
        heuristic = getattr(self, 'heuristic', None)
        if heuristic:
            return heuristic[point]
        else:
            return -1

def do_edges_intersect(edge1, edge2):
    def orientation(p, q, r):
        # Tính toán định hướng
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0  # Đồng phẳng
        return 1 if val > 0 else 2  # Trái hoặc phải
    def is_collinear_and_on_segment(p, q, r):
        # Kiểm tra điểm q có nằm trên đoạn pr không nếu đồng phẳng
        return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
                q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

    # Lấy các điểm từ hai cạnh
    p1, q1 = edge1.p1, edge1.p2
    p2, q2 = edge2.p1, edge2.p2

    # Tính định hướng cho từng bộ ba điểm
    orientations = [
        orientation(p1, q1, p2),  # o1
        orientation(p1, q1, q2),  # o2
        orientation(p2, q2, p1),  # o3
        orientation(p2, q2, q1)   # o4
    ]

    # Kiểm tra trường hợp tổng quát (hai cạnh giao nhau)
    if orientations[0] != orientations[1] and orientations[2] != orientations[3]:
        return True

    # Kiểm tra các trường hợp đặc biệt khi các điểm đồng phẳng
    special_cases = [
        (orientations[0] == 0 and is_collinear_and_on_segment(p1, p2, q1)),
        (orientations[1] == 0 and is_collinear_and_on_segment(p1, q2, q1)),
        (orientations[2] == 0 and is_collinear_and_on_segment(p2, p1, q2)),
        (orientations[3] == 0 and is_collinear_and_on_segment(p2, q1, q2))
    ]

    return any(special_cases)

# Hàm tính khoảng cách Euclid
def euclid_distance(point1, point2):
    return round(float(math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)), 3)


# Thuật toán tìm đường chung
def search(graph, start, goal, func):
    closed = set()
    queue = PriorityQueue()
    queue.put((0 + func(graph, start), start))
    if start not in closed:
        closed.add(start)
    while not queue.empty():
        cost, node = queue.get()
        if node == goal:
            return node
        for i in graph.can_see(node):
            new_cost = node.g + euclid_distance(node, i)
            if i not in closed or new_cost < i.g:
                closed.add(i)
                i.g = new_cost
                i.pre = node
                new_cost = func(graph, i)
                queue.put((new_cost, i))
    return node
a_star = lambda graph, i: i.g + graph.h(i)
greedy = lambda graph, i: graph.h(i)

# BFS
def bfs(graph, start, goal):
    visited = set()
    queue = Queue()
    queue.put(start)
    start.pre = None

    while not queue.empty():
        node = queue.get()
        if node == goal:
            return node
        visited.add(node)
        for neighbor in graph.can_see(node):
            if neighbor not in visited:
                neighbor.pre = node
                queue.put(neighbor)
    return None


# DFS
def dfs(graph, start, goal):
    visited = set()
    stack = [start]
    start.pre = None

    while stack:
        node = stack.pop()
        if node == goal:
            return node
        visited.add(node)
        for neighbor in graph.can_see(node):
            if neighbor not in visited:
                neighbor.pre = node
                stack.append(neighbor)
    return None


# UCS
def ucs(graph, start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start))
    start.g = 0
    start.pre = None

    while not queue.empty():
        cost, node = queue.get()
        if node == goal:
            return node
        visited.add(node)
        for neighbor in graph.can_see(node):
            new_cost = node.g + euclid_distance(node, neighbor)
            if neighbor not in visited or new_cost < neighbor.g:
                neighbor.g = new_cost
                neighbor.pre = node
                queue.put((new_cost, neighbor))
    return None

# Greedy Search
def greedy_search(graph, start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put((start.heuristic(goal), start))
    start.pre = None

    while not queue.empty():
        _, node = queue.get()
        if node == goal:
            return node
        visited.add(node)
        for neighbor in graph.can_see(node):
            if neighbor not in visited:
                neighbor.pre = node
                queue.put((neighbor.heuristic(goal), neighbor))
    return None

# Hàm in kết quả
def print_result(result_node):
    result = []
    while result_node:
        result.append(result_node)
        result_node = result_node.pre
    result.reverse()
    print_res = [[point, point.polygon_id] for point in result]
    print("Đường đi tìm được:", *print_res, sep=' -> ')
    return result


# Hàm hiển thị kết quả
def visualize(graph, poly_list, start, goal, result, title, ax):
    ax.set_title(title)
    ax.plot([start.x], [start.y], 'ro', label="Start")
    ax.plot([goal.x], [goal.y], 'ro', label="Goal")

    for i in range(1, len(poly_list) - 1):
        coord = [(p.x, p.y) for p in poly_list[i]] + [(poly_list[i][0].x, poly_list[i][0].y)]
        xs, ys = zip(*coord)
        ax.plot(xs, ys)

    path_x = [p.x for p in result]
    path_y = [p.y for p in result]
    ax.plot(path_x, path_y, 'b', linewidth=2.0, label="Path")
    ax.legend()



# Hàm chính
def main():
    n_polygon = 0
    poly_list = []

    with open('Input.txt', 'r') as f:
        line = f.readline().strip().split()
        n_polygon = int(line[0])
        start = Point(int(line[1]), int(line[2]))
        goal = Point(int(line[3]), int(line[4]))
        poly_list.append([start])
        for line in f:
            points = line.split()
            n_vertex = int(points[0])
            poly_list.append([Point(int(points[i + 1]), int(points[i + 2])) for i in range(0, 2 * n_vertex, 2)])
        poly_list.append([goal])

    graph = Graph(poly_list)
    graph.heuristic = {point: point.heuristic(goal) for point in graph.get_points()}

    # Thực hiện BFS, DFS, UCS, Greedy Search
    algorithms = {
        "A* Search": lambda g, s, t: search(g, s, t, a_star),
        "Greedy Search": lambda g, s, t: search(g, s, t, greedy),
        "BFS": bfs,
        "DFS": dfs,
        "UCS": ucs,
    }
    results = {}

    for algo_name, algo_func in algorithms.items():
        print(f"Chạy thuật toán {algo_name}:")
        result_node = algo_func(graph, start, goal)
        result_path = print_result(result_node)
        results[algo_name] = result_path

    # Vẽ kết quả
    fig, axes = plt.subplots(1, len(algorithms), figsize=(20, 4))
    for idx, (algo_name, result) in enumerate(results.items()):
        visualize(graph, poly_list, start, goal, result, algo_name, axes[idx])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


