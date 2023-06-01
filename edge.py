import heapq

def dijkstra(graph, start, variable_edges):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            if (current_vertex, neighbor) in variable_edges:
                # 변수 발생 시 해당 에지 가중치를 고려
                weight += variable_edges[(current_vertex, neighbor)]

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# 그래프 정의
graph = {
    'A': {'B': 5, 'C': 3},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 3, 'B': 2, 'D': 6},
    'D': {'B': 1, 'C': 6}
}

# 변수 발생 시 에지 가중치
variable_edges = {
    ('B', 'C'): 4  # 변수 발생으로 B-C 경로의 가중치를 4로 변경
}

# 출발지와 목적지 설정
start_vertex = 'A'
end_vertex = 'D'

# 최단 경로 계산
distances = dijkstra(graph, start_vertex, variable_edges)

# 최단 경로 출력
path = []
current_vertex = end_vertex
while current_vertex != start_vertex:
    path.append(current_vertex)
    current_vertex = min(graph[current_vertex], key=lambda x: distances[x] + graph[current_vertex][x])
path.append(start_vertex)
path.reverse()

print("최단 경로:", path)
print("최단 거리:", distances[end_vertex])