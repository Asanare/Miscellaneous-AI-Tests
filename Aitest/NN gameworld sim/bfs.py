import queue
def matrix_to_dict(width, height):
    graph = {}
    coordinates = [(x, y) for x in range(width) for y in range(height)]
    for coords in coordinates:
        row = coords[0]
        column = coords[1]
        if row+1 > width-1:
            right = None
        else:
            right = ((row+1,column))
        if row-1 < 0:
            left = None
        else:
            left = ((row-1, column))
        if column+1 > height-1:
            above = None
        else:
            above = ((row, column + 1))
        if column-1 < 0:
            below = None
        else:
            below = ((row, column - 1))
        neighbours = [right, left, above, below]
        neighbours = [x for x in neighbours if x != None]
        graph[(row,column)] = set(neighbours)
    return (graph)
def bfs(graph, start, goal):
    q = queue.Queue()
    path = [start]
    q.put(path)
    visited = set([start])
    while not q.empty():
        path = q.get()
        last_node = path[-1]
        if last_node == goal:
            return path
        for node in graph[last_node]:
            if node not in visited:
                visited.add(node)
                q.put(path + [node])

