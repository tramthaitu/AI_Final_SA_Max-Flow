import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

flow_value = 0
flow_dict = 0
matrix = 0

def create_graph():
    V = int(input('Nhập số lượng các node trong đồ thị: '))
    arr = list(range(0, V))
    print(f'Đây sẽ là các node sẽ có trong đồ thị: {arr}')
    n = int(input('Nhập số lượng các arc trong đồ thị: '))
    E = []
    for k in range(n):
        inputs = input().split()
        i, j, c = map(int, inputs)
        
        if (i >= 0 and i <= V - 1) and (j >= 0 and j <= V - 1):
            E.append([[i, j], c])
    
    for x in E:
        print(f'{x[0][0]} -> {x[0][1]}, công suất tối đa = {x[1]}')
    # s, t = map(int, input('Chọn node source và node sink: ').split())
    # print(f'Vậy node thứ {s} sẽ là source và node thứ {t} sẽ là sink')
    matrix = [[0 for _ in range(V)] for _ in range(V)]
    
    for x in E:
        matrix[x[0][0]][x[0][1]] = x[1]
    return matrix


class GraphVisualizer():
    def __init__(self, master):
        global matrix
        self.master = master
        self.master.title("Max-flow Problem")
        
        # Tạo một biến instance để lưu trữ ma trận kề
        self.adj_matrix = matrix

        # Phần trên (hiển thị đồ thị)
        self.upper_frame = tk.Frame(master)
        self.upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Phần dưới (chia làm 2 phần theo chiều dọc)
        self.lower_frame = tk.Frame(master)
        self.lower_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Phần dưới bên trái (nút vẽ đồ thị và nhập giá trị đỉnh nguồn và đỉnh đích)
        self.left_lower_frame = tk.Frame(self.lower_frame)
        self.left_lower_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Phần dưới bên phải (kết quả của max-flow)
        self.right_lower_frame = tk.Frame(self.lower_frame)
        self.right_lower_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Thêm đường kẻ chia ranh giới giữa phần trên và phần dưới
        ttk.Separator(master, orient=tk.HORIZONTAL).pack(side=tk.TOP, fill=tk.X)

        # Thêm đường kẻ chia ranh giới giữa phần dưới bên trái và bên phải
        ttk.Separator(self.lower_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        # Nhãn và hộp văn bản cho đỉnh nguồn
        self.source_label = tk.Label(self.left_lower_frame, text="Source:")
        self.source_label.pack(side=tk.TOP, padx=10, pady=10)
        self.source_entry = tk.Entry(self.left_lower_frame)
        self.source_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Nhãn và hộp văn bản cho đỉnh đích
        self.sink_label = tk.Label(self.left_lower_frame, text="Sink:")
        self.sink_label.pack(side=tk.TOP, padx=10, pady=10)
        self.sink_entry = tk.Entry(self.left_lower_frame)
        self.sink_entry.pack(side=tk.TOP, padx=10, pady=10)

        # Nút để vẽ đồ thị từ ma trận
        self.draw_button = tk.Button(self.left_lower_frame, text="Draw", command=self.draw_graph)
        self.draw_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Nút để hiển thị kết quả max-flow
        self.result_button = tk.Button(self.left_lower_frame, text="Kết quả", command=self.calculate_max_flow)
        self.result_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Hiển thị đồ thị mặc định khi khởi chạy
        self.draw_default_graph()

        # Hiển thị kết quả của max-flow
        self.result_label = tk.Label(self.right_lower_frame, text="Max-Flow Result: ")
        self.result_label.pack(side=tk.TOP, padx=10, pady=10)
        self.result_text = tk.Text(self.right_lower_frame, height=10, width=30)
        self.result_text.pack(side=tk.TOP, padx=10, pady=10)

    def draw_default_graph(self):
        self.draw_graph(reset=True)

    def draw_graph(self, reset=False):
        # Lấy giá trị từ ô nhập đỉnh nguồn và đỉnh đích
        source_text = self.source_entry.get()
        sink_text = self.sink_entry.get()

        # Kiểm tra xem người dùng đã nhập giá trị hợp lệ hay chưa
        if source_text and sink_text:
            try:
                source = int(source_text)
                sink = int(sink_text)
            except ValueError:
                # Nếu có lỗi khi chuyển đổi sang số nguyên, báo lỗi và không vẽ lại đồ thị
                messagebox.showerror("Error", "Invalid input. Please enter valid integers for source and sink.")
                return
        elif not reset:
            # Nếu không phải reset và một trong hai ô nhập trống, không vẽ lại đồ thị
            return

        # Xóa bất kỳ đồ thị nào đã được vẽ trước đó
        for widget in self.upper_frame.winfo_children():
            widget.destroy()

        # Tạo đồ thị có hướng từ ma trận kề mới
        self.graph = nx.DiGraph()
        num_nodes = len(self.adj_matrix)
        for u in range(num_nodes):
            for v in range(num_nodes):
                if self.adj_matrix[u][v] > 0:
                    self.graph.add_edge(u, v, capacity=self.adj_matrix[u][v])
               


        # Vẽ đồ thị bằng Matplotlib và FigureCanvasTkAgg
        self.fig, self.ax = plt.subplots()
        self.pos = nx.spring_layout(self.graph)  # Store the position for consistent layout

        # Đúng chiều mũi tên nhưng thiếu công suất 1 cạnh

        for u, v, data in list(self.graph.edges(data=True)):
            if self.graph.has_edge(v, u):
                # Nếu tồn tại cạnh ngược lại, vẽ hai đường song song
                capacity_uv = data['capacity']  # Công suất từ u đến v
                capacity_vu = self.graph[v][u]['capacity']  # Công suất từ v đến u 

                # Vẽ đường từ u đến v
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(u, v)], ax=self.ax, arrowstyle='->', arrowsize=20, edge_color='black', connectionstyle='arc3,rad=0.2')
                # Vẽ đường từ v đến u
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(v, u)], ax=self.ax, arrowstyle='<-', arrowsize=20, edge_color='black', connectionstyle='arc3,rad=-0.2')

                # Thêm nhãn cho cạnh u -> v
                nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels={(u, v): capacity_uv}, ax=self.ax, font_color='blue')
                # Thêm nhãn cho cạnh v -> u
                nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels={(v, u): capacity_vu}, ax=self.ax, font_color='red')
               
            else:
                # Nếu không có cạnh ngược lại, vẽ bình thường và hiển thị nhãn công suất
                nx.draw_networkx_edges(self.graph, self.pos, edgelist=[(u, v)], ax=self.ax, arrowstyle='->', arrowsize=20)
                nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels={(u, v): data['capacity']}, ax=self.ax, font_color='black')



        # Vẽ các nút
        nx.draw_networkx_nodes(self.graph, self.pos, node_color='lightblue', node_size=500, ax=self.ax)
        nx.draw_networkx_labels(self.graph, self.pos, font_size=10, font_weight='bold', ax=self.ax)

        # Đánh dấu đỉnh nguồn và đỉnh đích nếu không reset
        if not reset:
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[source], node_color='red', node_size=500, ax=self.ax)
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[sink], node_color='green', node_size=500, ax=self.ax)

        # Thêm nhãn cho các cạnh
        edge_labels = {(u, v): data['capacity'] for u, v, data in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, font_color='red', ax=self.ax)

        # Tạo canvas từ FigureCanvasTkAgg và đặt nó vào phần trên
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.upper_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def calculate_max_flow(self):
        global flow_value
        global flow_dict
        # Lấy giá trị từ ô nhập đỉnh nguồn và đỉnh đích
        source_text = self.source_entry.get()
        sink_text = self.sink_entry.get()

        # Kiểm tra xem người dùng đã nhập giá trị hợp lệ hay chưa
        if source_text and sink_text:
            try:
                source = int(source_text)
                sink = int(sink_text)
            except ValueError:
                # Nếu có lỗi khi chuyển đổi sang số nguyên, báo lỗi và không tính toán max-flow
                messagebox.showerror("Error", "Invalid input. Please enter valid integers for source and sink.")
                return
        else:
            # Nếu một trong hai ô nhập trống, không tính toán max-flow
            return

        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Max-Flow Value: {flow_value}\n")
        self.result_text.insert(tk.END, f"Max-Flow dict: {flow_dict}\n")

def DRAW(Matrix, Flow_value, Flow_dict):
    global flow_value
    global flow_dict
    global matrix

    flow_value = Flow_value
    flow_dict = Flow_dict
    matrix = Matrix
    
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()
if __name__ == "_main_":
    DRAW()









    
   


                






