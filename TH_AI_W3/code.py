import queue
import matplotlib.pyplot as plt


# getting heuristics from file
def getHeuristics():
    heuristics = {}
    f = open("heuristics.txt")
    for i in f.readlines():
        node_heuristic_val = i.split()
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])
    return heuristics


def getCity():
    city = {}
    citiesCode = {}
    f = open("cities.txt")
    j = 1
    for i in f.readlines():
        node_city_val = i.split()
        city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]
        citiesCode[j] = node_city_val[0]
        j += 1
    return city, citiesCode


def createGraph():
    graph = {}
    file = open("citiesGraph.txt")
    for i in file.readlines():
        node_val = i.split()

        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            graph[node_val[1]] = [[node_val[0], node_val[2]]]

        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

            graph[node_val[0]] = [[node_val[1], node_val[2]]]

        else:
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
            graph[node_val[1]] = [[node_val[0], node_val[2]]]

    return graph


def GBFS(start_node, heuristics, graph, goal_node):
    priority_queue = queue.PriorityQueue()
    priority_queue.put((heuristics[start_node], start_node))

    path = []

    while priority_queue.empty() == False:
        current = priority_queue.get()[1]
        path.append(current)
        if current == goal_node:
            break

        priority_queue = queue.PriorityQueue()

        for i in graph[current]:
            if i[0] not in path:
                priority_queue.put((heuristics[i[0]], i[0]))
    return path


def Astar(start_node, heuristics, graph, goal_node):
    priority_queue = queue.PriorityQueue()
    distance = 0

    priority_queue.put((heuristics[start_node] + distance, [start_node, 0]))

    path = []

    while priority_queue.empty() == False:
        current = priority_queue.get()[1]

        path.append(current[0])

        distance += int(current[1])

        if current[0] == goal_node:
            break

        priority_queue = queue.PriorityQueue()

        for i in graph[current[0]]:
            if i[0] not in path:
                priority_queue.put((heuristics[i[0]] + int(i[1]) + distance, i))

    return path


def AstarV2(start_node, heuristics, graph, goal_node):
    OPEN = queue.PriorityQueue()
    CLOSE = set()

    # Khởi tạo g, f và hàng đợi OPEN
    g = {start_node: 0}
    f = {start_node: heuristics[start_node]}
    OPEN.put((f[start_node], start_node))

    # Dictionary cha để tái tạo lại đường đi
    parent = {start_node: None}

    while not OPEN.empty():
        # Lấy nút có giá trị f thấp nhất
        current_cost, current_node = OPEN.get()

        # Nếu đạt tới nút đích, tái tạo đường đi
        if current_node == goal_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return path[::-1]

        # Thêm nút vào CLOSE
        CLOSE.add(current_node)

        # Khám phá các nút lân cận
        for neighbor, cost in graph[current_node]:
            if neighbor in CLOSE:
                continue  # Bỏ qua nếu nút đã có trong CLOSE

            tentative_g = g[current_node] + int(cost)

            # Nếu nút lân cận chưa trong OPEN hoặc tìm thấy đường ngắn hơn
            if neighbor not in g or tentative_g < g[neighbor]:
                # Cập nhật giá trị g và f
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + heuristics[neighbor]
                parent[neighbor] = current_node  # Theo dõi đường đi

                # Thêm vào OPEN với giá trị f đã cập nhật
                OPEN.put((f[neighbor], neighbor))

    # Nếu không đạt tới nút đích
    return None


def drawMap(city, gbfs, astar, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            second = city[gbfs[i + 1]]

            plt.plot([first[0], second[0]], [first[1], second[1]], "green")
        except:
            continue

    for i in range(len(astar)):
        try:
            first = city[astar[i]]
            second = city[astar[i + 1]]

            plt.plot([first[0], second[0]], [first[1], second[1]], "blue")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")

    plt.show()


if __name__ == "__main__":
    heuristics = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Nhập đỉnh bắt đầu: "))
        inputCode2 = int(input("Nhập đỉnh kết thúc: "))

        if inputCode1 == 0 or inputCode2 == 0:
            break

        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]

        gbfs = GBFS(startCity, heuristics, graph, endCity)
        astar = Astar(startCity, heuristics, graph, endCity)
        astarV2 = AstarV2(startCity, heuristics, graph, endCity)
        print("GBFS => ", gbfs)
        print("ASTAR => ", astar)
        print("ASTAR V2 => ", astarV2)

        drawMap(city, gbfs, astar, graph)
        drawMap(city, gbfs, astarV2, graph)
