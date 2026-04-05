def detect_deadlock(wait_for_graph):
    visited = set()

    def dfs(node, path):
        if node in path:
            return path[path.index(node):] 

        if node in visited:
            return None

        visited.add(node)
        path.append(node)

        for neighbor in wait_for_graph[node]:
            cycle = dfs(neighbor, path.copy())
            if cycle:
                return cycle

        return None

    for process in wait_for_graph:
        cycle = dfs(process, [])
        if cycle:
            return cycle

    return None