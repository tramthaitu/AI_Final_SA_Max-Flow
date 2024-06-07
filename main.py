from collections import defaultdict
from Algorithm_1 import SA
from ui import DRAW
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
Tìm ma trận trọng số giữa các cạnh

Sau khi chạy hàm Find_limit_capacity_matrix ta sẽ có được
    + Biến limit_capacity_matrix: một ma trận vuông kích thước V x V. 
        VD: limit_capacity_matrix[i][j] chính là trọng số tối đa của cạnh i -> j
'''
def Find_limit_capacity_matrix(V, E):
    limit_capacity_matrix = [[0 for _ in range(V)] for _ in range(V)]
    for x in E:
        limit_capacity_matrix[x[0][0]][x[0][1]] = x[1]
    
    return limit_capacity_matrix


'''
Tất cả đường đi có thể có từ s đến t

Sau khi chạy hàm Find_all_paths bên dưới ta sẽ được:
    + Biến all_paths: chứa tất cả các đường đi có thể đi được từ s đến t bằng giải thuật DFS
        VD: all_paths[0] = [1, 2, 3] với 1->2, 2->3 chính là đường đi từ đỉnh 1 đến đỉnh 3
'''
# Hàm xây dựng danh sách kề
def build_graph(edges):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
        return graph

# Hàm tìm tất cả các đường đi từ nguồn (start) đến đích (end)
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:  
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)

        return paths

# Tìm tất cả các đường đi từ đỉnh source đến đỉnh sink
def Find_all_paths(ds_canh, s, t):
    graph = build_graph(ds_canh)
    all_paths = find_all_paths(graph, s, t)

    return all_paths

'''
Từ biến chứa tất cả đường đi ở trên, tìm công suất lớn nhất có thể có của đường đi đó

Sau khi chạy hàm Find_all_path_and_limit_capacity ta sẽ được:
    + Biến all_path_and_limit_capacity: chứa tất cả các đường đi có thể đi được từ s đến t và công suất tối đa có thể có của đường đi đó
        VD: all_path_and_limit_capacity[0] = [[1, 2, 3], 2] với 1->2, 2->3 chính là đường đi từ đỉnh 1 đến đỉnh 3, công suất tối đa là 2
'''
def Find_all_path_and_limit_capacity(all_paths, limit_capacity_matrix):
    all_path_and_limit_capacity = [] # Chứa đường đi và luồng cực đại nhỏ nhất của nó
    for path in all_paths:
        tmp, capacity = [], limit_capacity_matrix[path[0]][path[1]]

        for i in range(len(path) - 1):
            tmp.append([path[i], path[i + 1]])
            capacity = min(capacity, limit_capacity_matrix[path[i]][path[i + 1]])
            
        all_path_and_limit_capacity.append([tmp, capacity])
    
    return all_path_and_limit_capacity

'''
Ứng với mỗi cạnh, tìm tất cả đường đi đi qua cạnh đó

Sau khi chạy hàm Find_mapping ta sẽ được:
    + Biến Mapping: chứa các cặp key-value, key là cạnh, value là index của các đường đi trong all_path_and_limit_capacity
        VD: Mapping[(0, 4)] = [1, 2] với (0, 4) chính là cạnh 0->4 và [1, 2] chính đường đi tại index thứ 1, 2 trong all_path_and_limit_capacity
            đã đi qua cạnh 0->4
'''
# Mapping sẽ trả về dictionnary, với key là các cạnh và value tương ứng chính là index của các path chứa cạnh đó
def Find_mapping(all_path_and_limit_capacity):
    Mapping = dict()
    for x in E:
        Mapping[tuple(x[0])] = []

    for i in range(len(all_path_and_limit_capacity)):
        for y in all_path_and_limit_capacity[i][0]:
            Mapping[y[0], y[1]].append(i)
    
    return Mapping

if __name__ == '__main__':
    '''
    Nhập input.

    Sau khi chạy block này ta sẽ có được:
        + Biến V: cho biết số lượng các đỉnh trong đồ thị

        + Biến n: cho biết số lượng các cạnh trong đồ thị

        + Biến E: chứa tất cả các cặp cạnh trong đồ thị cùng với trọng số tương ứng của cạnh đó. 
            VD: E[0] = [[<đỉnh i>, <đỉnh j>], <trọng số cạnh ij>]

        + Biến ds_canh: chứa tất cả các cặp cạnh trong đồ thị không bao gồm trọng số của cạnh đó. 
            VD: ds_canh[0] = [<đỉnh i>, <đỉnh j>]

        + Biến s: đỉnh bắt đầu của đồ thị
        
        + Biến t: đỉnh kết thúc của đồ thị
    '''
    V = int(input('Nhập số lượng các đỉnh trong đồ thị: '))
    n = int(input('Nhập số lượng các cạnh trong đồ thị: '))

    E = []
    ds_canh = []
    for k in range(n):
        i, j, c = map(int, input().split())
        
        if (i >= 0 and i <= V - 1) and (j >= 0 and j <= V - 1):
            E.append([[i, j], c])
            ds_canh.append([i, j])
            
    s, t = map(int, input('Chọn đỉnh bắt đầu và đỉnh cuối: ').split())

    limit_capacity_matrix = Find_limit_capacity_matrix(V, E)
    all_paths = Find_all_paths(ds_canh, s, t)
    all_path_and_limit_capacity = Find_all_path_and_limit_capacity(all_paths, limit_capacity_matrix)
    Mapping = Find_mapping(all_path_and_limit_capacity)

    # Tạo trạng thái ban đầu, cho công suất của các đường đi = 0
    initial_state = []
    for i in range(len(all_path_and_limit_capacity)):
        initial_state.append([all_path_and_limit_capacity[i], 0])

    # Chỉnh nhiệt độ, hệ số làm lạnh, max iteration
    initial_temp = 100
    cooling_rate = 0.99
    max_iter = 100000

    # Chạy thuật toán SA
    best_cost, best_state = SA(initial_temp, cooling_rate, max_iter, initial_state, Mapping, V)
    matrix = [[0 for _ in range(V)] for _ in range(V)]
    for x in best_state:
        for y in x[0][0]:
            matrix[y[0]][y[1]] += x[1]
    
    DRAW(matrix, best_cost, best_state)
    
    # Tô đen từ dòng này trở xuống xong bỏ comment
    # # Input mẫu: 
    # Nhập số lượng các đỉnh trong đồ thị: 4
    # Nhập số lượng các cạnh trong đồ thị: 5
    # 0 1 3
    # 0 2 2 
    # 1 3 2
    # 1 2 5
    # 2 3 3
    # Chọn đỉnh bắt đầu và đỉnh cuối: 0 3

    # # Khi xuất hiện giao diện có hộp thoại Source và Sink 
    # Nhập giá trị vào hộp thoại Soure và Sink => ấn 'Draw' để vẽ đồ thị (có thể spam nhiều lần nếu đồ thị xấu) => ấn 'Kết quả' để hiển thị giá trị max-flow, đường đi trực quan
