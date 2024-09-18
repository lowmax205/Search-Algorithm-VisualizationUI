from collections import deque

def add_edge(adj, s, t):
    # Add edge from vertex s to t
    adj[s].append(t)
    # Due to undirected Graph
    adj[t].append(s)


def bfs(adj, s):
    visited = [False] * len(adj)
    result = []

    # Create a queue for BFS
    queue = deque([s])

    # Mark the current vertex as visited
    visited[s] = True
    result.append(s)

    # Loop until the queue is empty
    while queue:
        # Dequeue a vertex from the queue
        v = queue.popleft()
        print(f"Visiting node {v}")  # <--- Added this line

        # Enqueue all adjacent vertices that are not visited yet
        for i in adj[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                result.append(i)

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
    print("BFS from source:", source)
    result = bfs(adj, source)
    print("\nFinal result:", result)