def add_edge(adj, s, t):
    # Add edge from vertex s to t
    adj[s].append(t)
    # Due to undirected Graph
    adj[t].append(s)


def dls(adj, s, limit):
    visited = [False] * len(adj)
    result = []

    def dfs(v, depth):
        if depth > limit:
            return  # Stop when depth exceeds limit

        visited[v] = True
        result.append(v)
        print(f"Visiting node {v} at depth {depth}")

        for i in adj[v]:
            if not visited[i]:
                dfs(i, depth + 1)

    # Start DFS from source node `s` with depth 0
    dfs(s, 0)
    return result


if __name__ == "__main__":
    V = 5

    # Create an adjacency list for the graph
    adj = [[] for _ in range(V)]

    # Define the edges of the graph
    edges = [[1, 2], [1, 0], [2, 0], [2, 3], [2, 4]]

    # Populate the adjacency list with edges
    for e in edges:
        add_edge(adj, e[0], e[1])

    source = 1
    depth_limit = 2
    print(f"Depth-Limited Search from source: {source} with limit {depth_limit}")
    result = dls(adj, source, depth_limit)
    print("\nFinal result:", result)
