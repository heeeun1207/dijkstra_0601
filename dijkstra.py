import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    previous = {}  # 각 노드의 이전 노드를 저장하기 위한 딕셔너리

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for adjacent_node, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[adjacent_node]:
                distances[adjacent_node] = distance
                previous[adjacent_node] = current_node  # 이전 노드 정보 업데이트
                heapq.heappush(queue, (distance, adjacent_node))

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
distances, previous = dijkstra(graph, start_node)

# F1과 F3 중 D1으로 가는 가장 빠른 방법 찾기
fastest_path = float('inf')
via_node = None

for node in ['F1', 'F3']:
    if node in distances:
        distance_to_node = distances[node]  # F1 또는 F3까지의 거리
        distance_through_node = distance_to_node + graph[node].get('D1', float('inf'))  # F1 또는 F3를 거치고 D1까지의 거리

        if distance_through_node < fastest_path:
            fastest_path = distance_through_node
            via_node = node

# F1 또는 F3를 거쳐 D1로 가는 최단 경로 출력
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