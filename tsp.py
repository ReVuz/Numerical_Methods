# Python program to implement traveling salesman
# problem using naive approach.

from itertools import permutations
from sys import maxsize
n_rows = int(input("Number of rows:"))
n_columns = int(input("Number of columns:"))
# Define the graph
graph = []
print("Enter the entries row-wise:")
# for user input
for i in range(n_rows):          # A for loop for row entries
    a = []
    for j in range(n_columns):      # A for loop for column entries
        a.append(int(input()))
    graph.append(a)

V = int(input("Enter the number of vertices : "))

# implementation of traveling Salesman Problem


def travellingSalesmanProblem(graph, s):

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]

        # update minimum
        min_path = min(min_path, current_pathweight)
        min_path_vertices = [s] + list(i) + [s]

    print("Shortest Path: ", min_path_vertices)
    return min_path


# Driver Code
if __name__ == "__main__":

    # graph representation of graph
    # graph = [[0, 10, 15, 20], [10, 0, 35, 25],
    # 		[15, 35, 0, 30], [20, 25, 30, 0]]
    s = 0
    print("Minimum Cost of the given graph : ",
          travellingSalesmanProblem(graph, s))
