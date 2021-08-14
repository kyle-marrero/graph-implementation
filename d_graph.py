# Course: CS261 - Data Structures
# Author: Kyle Marrero
# Assignment: 6
# Description: DirectedGraph Implementation

from collections import deque
import heapq

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add a new vertex to the graph
        """
        # add a 0 to each list, since there is a new vertex to consider
        for i in self.adj_matrix:
            i.append(0)
        
        self.v_count += 1

        # add a new list to adj matrix
        l = [0] * self.v_count

        self.adj_matrix.append(l)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        add an edge and weight to the graph (weight defaults to 1)
        """
        # do nothing if any of these conditions are met
        if src >= self.v_count or dst >= self.v_count or src < 0 or dst < 0 or weight < 0 or src == dst:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        remove an edge from the graph
        """
        if src >= self.v_count or dst >= self.v_count or src < 0 or dst < 0:
            return

        self.adj_matrix[src][dst] = 0        

    def get_vertices(self) -> []:
        """
        return the vertices in the graph
        """
        vertices = []

        for v in range(self.v_count):
            vertices.append(v)

        return vertices

    def get_edges(self) -> []:
        """
        return the edges in the graph
        """
        edges = []

        for i in range(self.v_count):
            for j in range(self.v_count):

                # if indices have value (weight), there is an edge and we can add it to the list
                if self.adj_matrix[i][j] != 0:
                    edges.append((i, j, self.adj_matrix[i][j]))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # empty path
        if not path:
            return True

        start = path[0]

        for i in range(1, len(path)):

            # if any index has value 0, there is no path, thus invalid
            if self.adj_matrix[start][path[i]] == 0:
                return False

            start = path[i]

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        v = set()
        d = deque()
        visited = []

        if v_start < 0 or v_start >= self.v_count:
            return visited

        if v_end is not None and (v_end < 0 or v_end >= self.v_count):
            v_end = None

        d.append(v_start)

        while d:
            # pop next vertex to explore off stack
            vert = d.pop()
            if vert not in visited:
                visited.append(vert)

            if vert == v_end:
                break

            if vert not in v:
                v.add(vert)
                # iterate backwards over list
                for i in range(self.v_count - 1, -1, -1):
                    # if adjacent vertex and not visited, add to exploration stack
                    if self.adj_matrix[vert][i] != 0 and i not in v:
                        d.append(i)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        v = set()
        d = deque()
        visited = []

        if v_start < 0 or v_start >= self.v_count:
            return visited

        if v_end is not None and (v_end < 0 or v_end >= self.v_count):
            v_end = None

        d.appendleft(v_start)

        while d:
            vert = d.pop()
            if vert not in visited:
                visited.append(vert)

            if vert == v_end:
                break

            if vert not in v:
                v.add(vert)

                for i in range(self.v_count):
                    # if adjacent vertex and not visited, add to exploration queue
                    if self.adj_matrix[vert][i] != 0 and i not in v:
                        d.appendleft(i)

        return visited

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise (uses DFS)
        """
       
        # create outer loop to ensure we visit all vertices (if there are multiple connected components)
        for v in range(self.v_count):
        
            visited = set()
            d = deque()

            if v not in visited:
                d.append(v)

                while d:
                    flag = False

                    # assign top of stack to vert
                    vert = d[-1]

                    if vert not in visited:
                        visited.add(vert)

                        for i in range(self.v_count - 1, -1, -1):
                            # add to exploration stack if not yet visited and not in exploration stack already
                            if self.adj_matrix[vert][i] != 0 and i not in visited and i not in d:
                                d.append(i)

                            # i is on stack and in visited set, means there is cycle
                            if self.adj_matrix[vert][i] != 0 and i in visited and i in d:
                                return True
                    # pop off stack if vert has been visited
                    else:
                        d.pop()

        return False

    def dijkstra(self, src: int) -> []:
        """
        implements dijkstra's algorithm, uses a priority queue to determine the
        shortest path to each vertex from a given source vertex
        """
        visited = dict()
        pq = [(0, src)]
        paths = []

        # initialize list with inf values
        for i in range(self.v_count):
            paths.append(float('inf'))

        while pq:
            # assign vertex and distance, and remove min heap value
            d, v = heapq.heappop(pq)

            if v not in visited:
                # add to visited dictionary
                visited[v] = d

                for i in range(self.v_count):

                    # if adjacent vertex, calculate distance
                    if self.adj_matrix[v][i] != 0:
                        dist = d + self.adj_matrix[v][i]
                        # push tuple of distance and vertex into prioity queue and maintain minheap
                        heapq.heappush(pq, (dist, i))

        # for all explored vertices, add their distance to list
        for k, v in visited.items():
            paths[k] = v

        return paths



if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)

    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)


    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)

    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')

    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)


    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')


    edges = [(0, 1, 2), (1, 2, 6), (2, 3, 3), (2, 4, 5),
             (3, 4, 1)]
    g = DirectedGraph(edges)
    print(g.dijkstra(0))


