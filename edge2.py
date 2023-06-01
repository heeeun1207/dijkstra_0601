import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}  # 시작 노드로부터의 거리를 무한대로 초기화
    distances[start] = 0  # 시작 노드의 거리는 0
    queue = [(0, start)]  # 우선순위 큐를 사용하여 처리할 노드들을 저장
    previous = {}  # 최단 경로를 구성하는 이전 노드를 저장하는 딕셔너리

    while queue:
        current_distance, current_node = heapq.heappop(queue)  # 우선순위 큐에서 가장 거리가 짧은 노드 선택

        if current_distance > distances[current_node]:
            continue  # 선택한 노드의 거리가 이미 최단 거리보다 크면 무시

        for adjacent_node, weight in graph[current_node].items():
            if current_node == 'E3' and adjacent_node == 'E4':
                continue  # E3에서 E4로 가는 가중치 100인 간선은 제외
            distance = current_distance + weight  # 선택한 노드를 거쳐 인접한 노드로 가는 거리 계산

            if distance < distances[adjacent_node]:
                distances[adjacent_node] = distance  # 거리 갱신
                previous[adjacent_node] = current_node  # 최단 경로 업데이트
                heapq.heappush(queue, (distance, adjacent_node))  # 다음에 처리할 노드로 추가

    return distances, previous
graph = {
    'E1': {'E2': 7.7, 'D1': 29.1},
    'E2': {'E1': 7.7, 'E3': 12.9, 'D1': 32.6},
    'E3': {'E2': 12.9, 'E4': 5.5, 'E19': 6.8, 'D1': 24.3},
    'E4': {'E3': 5.5, 'E5': 14.7, 'E12': 19.2, 'E19': 10.1, 'F3': 7.1},
    'E5': {'E4': 14.7, 'E6': 17.5, 'E18': 20},
    'E6': {'E5': 17.5},
    'E12': {'E4': 19.2, 'F3': 14.2},
    'E18': {'E5': 20, 'E6': 7.3},
    'E19': {'E3': 6.8, 'E4': 10.1, 'F1': 10.5, 'D1': 19.6},
    'F1': {'E19': 10.5, 'D1': 14.4},
    'F3': {'E4': 7.1, 'E12': 14.2, 'E19': 14.2},
    'D1': {'E1': 29.1, 'E2': 32.6, 'E3': 24.3, 'E19': 19.6, 'F1': 14.4}
}

start_node = 'E4'

# Merge variable_edges into graph
variable_edges = {
    ('E19'): 100
}

for node1 in variable_edges:
    weight = variable_edges[node1]
    graph[node1] = {}  # 노드 node1의 모든 간선을 제거
    # 다른 모든 노드의 간선에서 node1을 제거
    for node in graph:
        graph[node].pop(node1, None)

# Perform Dijkstra's algorithm
distances, previous = dijkstra(graph, start_node)

fastest_path = float('inf')
via_node = None

for node in ['F1', 'F3']:
    if node in distances:
        distance_to_node = distances[node]
        distance_through_node = distance_to_node + graph[node].get('D1', float('inf'))

        if distance_through_node < fastest_path:
            fastest_path = distance_through_node
            via_node = node

if via_node:
    print(f"{via_node}를 거쳐 D1로 가는 가장 빠른 방법의 최단 거리: {fastest_path:.1f}")
    print("경로:", end=" ")
    path = [via_node, 'D1']
    current_node = via_node
    while current_node != start_node:
        previous_node = previous[current_node]
        path.insert(0, previous_node)
        current_node = previous_node
    path.insert(0, start_node)
    print(" -> ".join(path))
else:
    print("F1 또는 F3를 거쳐 D1로 가는 경로가 없습니다.")

