import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    previous = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for adjacent_node, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[adjacent_node]:
                distances[adjacent_node] = distance
                previous[adjacent_node] = current_node
                heapq.heappush(queue, (distance, adjacent_node))

    return distances, previous

graph = {
    # E 경로
    'E1': {'E2': 7.7, 'F1': 23.4, 'D1': 29.1},
    'E2': {'E1': 7.7, 'E3': 12.9, 'F1': 24.4, 'D1': 32.6},
    'E3': {'E2': 12.9, 'E4': 5.5, 'E19': 6.8, 'D1': 24.3},
    'E4': {'E3': 5.5, 'E5': 14.7, 'E12': 19.2, 'E19': 10.1, 'F3': 7.1},
    'E5': {'E4': 14.7, 'E6': 17.5, 'E18': 20},
    'E6': {'E5': 17.5, 'E7': 28.3, 'E13': 17.9, 'E18': 7.3},
    'E7': {'E6': 28.3, 'E9': 2.1},
    'E8': {'E9': 10.0, 'E20': 4.5, 'F2': 11.1, 'D2': 11.6},
    'E9': {'E7': 2.1, 'E8': 10.0},
    'E10': {'E9': 24.7, 'E11': 14.6},
    'E11': {'E10': 14.6, 'E15': 15.6, 'E16': 13.6},
    'E12': {'E4': 19.2, 'E13': 6.1, 'E18': 9.7, 'F3': 14.7},
    'E13': {'E6': 17.9, 'E12': 6.1, 'E14': 18.0},
    'E14': {'E13': 18.0, 'E15': 9.4, 'E17': 4.7},
    'E15': {'E11': 15.6, 'E14': 9.4, 'E16': 4.8, 'E17': 11.6},
    'E16': {'E11': 13.6, 'E15': 4.8, 'D3': 18.6},
    'E17': {'E14': 4.7, 'E15': 11.6, 'E19': 55.2, 'F3': 41.2, 'D3': 9.5},
    'E18': {'E5': 20, 'E12': 9.7, 'E13': 12.0},
    'E19': {'E3': 6.8, 'E4': 10.1, 'F1': 10.0, 'F3': 14.2, 'D1': 19.6},
    'E20': {'E8': 4.5, 'E9': 6.0, 'E10': 24.7, 'F2': 8.1},
    # F 소화기
    'F1': {'E1': 23.4, 'E2': 24.4, 'E19': 10.0, 'D1': 9.8},
    'F2': {'E8': 11.1, 'E20': 8.1, 'D2': 8.2},
    'F3': {'E4': 7.1, 'E12': 14.2, 'E17': 41.2, 'E19': 14.2},
    # R 화장실
    'R1': {'E8': 8.6, 'D2': 18.2},
    # D 출구
    'D1': {'E1': 29.1, 'E2': 32.6, 'E3': 24.3, 'E19': 19.6, 'F1': 9.8},
    'D2': {'E8': 11.6, 'E20': 4.5, 'R1': 18.2, 'F2': 8.2},
    'D3': {'E16': 18.6, 'E17': 9.5}
}

start_node = 'E18'  # 사용자 위치라고 가정
distances, previous = dijkstra(graph, start_node)

# 출구(D1, D2, D3)로 가는 최단 거리와 경로 찾기
fastest_path_without_via = min(distances.get(exit_node, float('inf')) for exit_node in ['D1', 'D2', 'D3'])
path_without_via = []
for exit_node in ['D1', 'D2', 'D3']:
    if exit_node in distances and distances[exit_node] == fastest_path_without_via:
        current_node = exit_node
        while current_node != start_node:
            previous_node = previous[current_node]
            path_without_via.insert(0, current_node)
            current_node = previous_node
        path_without_via.insert(0, start_node)
        break

# 소화기(F1, F2, F3)를 거쳐 출구(D1, D2, D3)로 가는 최단 거리와 경로 찾기
fastest_path_with_via = float('inf')
path_with_via = []

for via_node in ['F1', 'F2', 'F3']:
    via_distances, via_previous = dijkstra(graph, via_node)
    via_distance_to_exit = min(via_distances.get(exit_node, float('inf')) for exit_node in ['D1', 'D2', 'D3'])
    total_distance = distances[via_node] + via_distance_to_exit

    if total_distance < fastest_path_with_via:
        fastest_path_with_via = total_distance
        path_with_via = []

        current_node = via_node
        while current_node != start_node:
            previous_node = previous[current_node]
            path_with_via.insert(0, current_node)
            current_node = previous_node

        current_node = via_node
        while current_node != 'D1' and current_node != 'D2' and current_node != 'D3':
            next_node = min(via_distances.keys(), key=lambda x: via_distances[x])
            via_distance = via_distances[next_node]
            path_with_via.append(next_node)
            current_node = next_node

        path_with_via.append(current_node)

print("출구(D1, D2, D3)로 가는 최단 거리:", fastest_path_without_via)
print("경로:", " -> ".join(path_without_via))
print("🧯F1를 거쳐 출구(D1, D2, D3)로 가는 최단 거리:", fastest_path_with_via)
print("🧯포함 경로:", " -> ".join(path_with_via))
