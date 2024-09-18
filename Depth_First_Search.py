def add_edge(adj, s, t):
    # Add edge from vertex s to t
    adj[s].append(t)
    # Due to undirected Graph
    adj[t].append(s)


def dfs_rec(adj, visited, s, result):
    # Mark the current vertex as visited
    visited[s] = True
    print(f"Visiting node {s}")  # <--- Added this line
    # Print the current vertex
    print(s, end=" ")
    result.append(s)  # <--- Add the node to the result list

    # Recursively visit all adjacent vertices
    # that are not visited yet
    for i in adj[s]:
        if not visited[i]:
            dfs_rec(adj, visited, i, result)


def dfs(adj, s):
    visited = [False] * len(adj)
    result = []  # <--- Initialize the result list
    # Call the recursive DFS function
    dfs_rec(adj, visited, s, result)
    return result  # <--- Return the result list


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
    print("DFS from source:", source)
    result = dfs(adj, source)
    print("\nFinal result:", result)