# Course: CS261 - Data Structures
# Author: Kyle Marrero
# Assignment: 6
# Description: UndirectedGraph implementation

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """


        if v not in self.adj_list:
            self.adj_list[v] = []

        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """

        if u == v:
            return

        # add v for key u
        if u not in self.adj_list:
            self.adj_list[u] = [v]
        elif v not in self.adj_list[u]:
            self.adj_list[u].append(v)

        # add u for key v
        if v not in self.adj_list:
            self.adj_list[v] = [u]
        elif u not in self.adj_list[v]:
            self.adj_list[v].append(u)

        # print(self.adj_list)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """

        if u not in self.adj_list or v not in self.adj_list:
            return

        if v in self.adj_list[u]: 
            self.adj_list[u].remove(v)

        if u in self.adj_list[v]: 
            self.adj_list[v].remove(u)
        

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # remove key if exists
        if v in self.adj_list:
            del self.adj_list[v]

        # remove all other entries of v
        for k in self.adj_list:
            if v in self.adj_list[k]:
                self.adj_list[k].remove(v)
        

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """

        l = []

        for v in self.adj_list:
            l.append(v)

        return l
       

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        l = []

        s = set()

        for v in self.adj_list:
            s.add(v)
            for e in self.adj_list[v]:
                if e not in s:
                    l.append((v, e))

        return l
        

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        d = None

        for i in path:

            if not d:
                d = i
                if d not in self.adj_list:
                    return False
                else:
                    continue
            # check if next vertex is in adjacency list of previous
            if i in self.adj_list[d]:
                d = i
            else:
                return False

        return True

       

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        v = set()
        d = deque()
        visited = []

        if v_start not in self.adj_list:
            return visited

        if v_end not in self.adj_list:
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
                # reverse adj list so we can access smaller vertex first
                self.adj_list[vert].sort(reverse=True)
                for i in self.adj_list[vert]:
                    # add successors onto stack
                    if i not in v:
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

        if v_start not in self.adj_list:
            return visited

        if v_end not in self.adj_list:
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
                # sort adj list so we can access smaller vertex first
                self.adj_list[vert].sort()
                for i in self.adj_list[vert]:
                    # add successors into queue
                    if i not in v:
                        d.appendleft(i)

        return visited
        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """

        visited = set()
        comps = []

        for v in self.adj_list:

            if v not in visited:
                # perform dfs as far as possible, return list of visited vertices
                l = self.dfs(v)
                comps.append(l)
                # add vertices to visited, so we don't run the DFS again if we don't need to 
                for i in l:
                    visited.add(i)

        return len(comps)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """

        # perform modified BFS, if two adjacent vertices are in visited set
        # that means there is a cycle 
       
        visited = set()
        d = deque()


        # perform BFS for each vertex in dict
        for v in self.adj_list:

            if v not in visited:
                d.appendleft(v)

                while d:
                    count = 0
                    vert = d.pop()

                    if vert not in visited:
                        visited.add(vert)
                        # sort so we access smaller vertex first
                        self.adj_list[vert].sort()
                        for i in self.adj_list[vert]:
                            # add successors onto stack
                            if i not in visited:
                                d.appendleft(i)
                            # if a vertex has already been visited, and is adjacent, increment
                            if i in visited:
                                count += 1
                            # if we have at least 2 vertices that are adjacent and have been visited, there is a cycle
                            if count >= 2:
                                return True

        return False
   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    print(g)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    print(g)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
