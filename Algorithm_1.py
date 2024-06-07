from collections import defaultdict
import random
import math as m


'''Sử dụng thuật toán Simulated Annealing'''
'''
Hàm này giúp tìm ma trận trọng số giữa các cạnh trong đồ thị của trạng thái hiện tại

Sau khi gọi hàm này ta sẽ có được
    + Trả về giá trị của biến matrix: một ma trận vuông kích thước V x V. 
        VD: matrix[i][j] chính là trọng số (không nhất thiết là tối đa) của cạnh i -> j của trạng thái hiện tại
'''
def build_capacity_matrix_of_real_state(current_state, V):
    matrix = [[0 for _ in range(V)] for _ in range(V)]
    for x in current_state:
        for y in x[0][0]:
            matrix[y[0]][y[1]] += x[1]
    return matrix

'''
Hàm giúp đánh giá dựa trên luồng tối đa tìm được bằng cách tính tổng các công suất của các đường đi trong trạng thái hiện tại
'''
def state_cost(current_state):
    return sum([x[1] for x in current_state])

'''
Hàm giúp sinh ra trạng thái kế tiếp với quá trình như sau:
    Chọn ngẫu nhiên 1 đường đi để tiến tạo ra trạng thái kế tiếp theo 3 cách theo thứ tự:
        + Tăng công suất của đường đó khi nó chưa tối đa và việc tăng đó không gây xung đột với đường khác
        + Giảm công suất của đường đó khi công suất đường đó giảm 1 có thể làm cho công suất của 2 đường khác tăng 
            (2 đường đó phải được đảm bảo không quá tải và xung đột)
        + Không thay đổi gì cả
'''
def neighborhood(current_state, Mapping, V):
    neighbour = current_state.copy()
    # Chọn ngẫu nhiên 1 đường đi để tiến hành tăng giảm
    random_number = random.randint(0, len(neighbour) - 1)
    # Nên làm hàm tạo capacity matrix voi capacity là real capacity
    capacity_matrix_of_current_state = build_capacity_matrix_of_real_state(neighbour, V)

    # Xét xem đường đi đủ điều kiện để tăng hay không. Dung lượng hiện tại < dung lượng tối đa mà luồng có thể tải
    if (neighbour[random_number][1] < neighbour[random_number][0][1]):
        # Nếu có thể tăng, xét tiếp xem nếu tăng path này thì có làm quá tải các path khác không
        # Tìm số lượng đơn vị nhiều nhất có thể:
        # + TH1: tăng cho capacity ở path này mà ko gây ảnh hưởng đến path khác
        # + TH2: tăng hàm đánh giá (ko cần xét TH này, vì nếu TH1 false thì TH2 ko cần thiết, 
        # nếu TH1 True thì TH2 cần xảy ra) TH2 chỉ nên dùng khi check giảm path này tăng path khác
        tmp = 0 # Sẽ là giá trị i (của vòng lặp bên dưới) lớn nhất có thể tăng cho path này
        for i in range(1, neighbour[random_number][0][1] - neighbour[random_number][1] + 1):
            # Check TH1
            check = 1
            # Vào path đó lấy từng cạnh ra
            for x in neighbour[random_number][0][0]:
                # Xét xem liệu real_capacity + i có lớn hơn limit_capacity hay không
                if (capacity_matrix_of_current_state[x[0]][x[1]] + i) > neighbour[random_number][0][1]:
                    check = 0
                    break
            
            if check == 0:
                break

            tmp = i
        # Sau vòng lặp này thì tmp sẽ là giá trị lớn nhất mà path này có thể tăng
        # Tiến hành cập nhật lại real_capacity của path này - đây được coi là 1 neighbour
        
        neighbour[random_number][1] += tmp
    # Nếu ko thể tăng real_capacity của path này thì ta xem xét giảm real_capacity của path này để tăng real_capacity của path khác
    elif (current_state[random_number][1] > 0):
        # Tiến hành giảm 1 giá trị của real_capacity của path này
        neighbour[random_number][1] -= 1
        # Tìm những path có thể được hưởng lợi từ việc này (những path có chung cạnh với path-bị-giảm)
        # Lúc này ta cần 1 cái map. Trong đó key là cặp cạnh, value là danh sách các path có chứa cạnh đó
        # Ta có biến Mapping 
        # Lúc này cần tìm ra các path khác mà có cơ may được lợi từ việc giảm dung lượng của path-bị-giảm
        path_duoc_loi = set({})
        # Duyệt qua các cạnh có trong path-bị-giảm
        for x in neighbour[random_number][0][0]:
            # Tìm các path có chung cạnh x
            for y in Mapping[tuple(x)]:
                if (y != random_number):
                    path_duoc_loi.add(y)
        # Sau dòng này ta sẽ có được 1 set chứa index của các path có vẻ sẽ được lợi
        # Sau đó ta cần thử tăng dung lượng của các path này xem có được không
        
        n = len(path_duoc_loi)
        # 2 vòng lặp này giống như bắt cặp lần lượt các path có trong path_duoc_loi
        for i in range(n):
            for j in range(i + 1, n):
                # Xét xem có thể giảm path thứ random_number từ đầu đến bằng 0, song song 2 path i, j vẫn tăng
                # Nếu visited_i_j = 0 nghĩa là vòng lặp k bên dưới sắp đc chạy lần đầu tiên, nếu if check_j == 1 thất bại thì có thể chuyển đến cặp i j khác
                # Nếu != 0 thì nghĩa là đã có lựa chọn tối ưu cho trường hợp này, nếu if check_j == 1 thất bại thì có thể trực tiếp return
                visited_i_j = 0
                for k in range(1, neighbour[random_number][1] + 1):
                    # Check xem path i có tăng thêm 1 được hay không
                    if (neighbour[i][1] < neighbour[i][0][1]):
                        check_i = 1
                        for x in neighbour[i][0][0]:
                            if (capacity_matrix_of_current_state[x[0]][x[1]] + 1) > neighbour[i][0][1]:
                                check_i = 0
                                break
                        # Check xem với việc path i đã tăng thêm 1 thì path j có tăng thêm 1 được hay không
                        
                        if check_i == 1:
                            # Tạo 1 solution tạm với path thứ random_number bị trừ 1 và path thứ i cộng 1
                            tmp1 = neighbour.copy()
                            tmp1[i][1] += 1
                            # Check xem path j có tăng thêm 1 được hay không
                            if (tmp1[j][1] < tmp1[j][0][1]):
                                check_j = 1
                                for x in tmp1[j][0][0]:
                                    if (capacity_matrix_of_current_state[x[0]][x[1]] + 1) > tmp1[j][0][1]:
                                        check_j = 0
                                        break
                                
                                if check_j == 0: # Nếu ko thể tìm thấy phương án tốt hơn
                                    if visited_i_j == 0: # Nếu lần đầu gặp
                                        break # Chuyển sang cặp i j khác
                                    else:
                                        neighbour[random_number][1] += 1
                                        return neighbour # Trực tiếp nhận phương án tối ưu đã có trước đó của cặp i j này
                                else: # Nếu tìm thấy phương án tốt hơn
                                    visited_i_j += 1 # Tăng số lần gặp cặp i j này
                                    tmp2 = tmp1.copy() 
                                    tmp2[j][1] += 1 
                                    neighbour = tmp2 # Cập nhật neighbour thành TH có path thứ random_number trừ 1 và path thứ i, j cộng 1 trong vòng lặp này
                                    if neighbour[random_number][1] > 0: # Nếu vẫn có thể trừ 1
                                        neighbour[random_number][1] -= 1 # Trừ 1 để tiếp tục thử tiếp
                            
        neighbour[random_number][1] += 1
        
    return neighbour

'''Tiến hành chạy thuật toán Simulated Annealing'''

def SA(initial_temp, cooling_rate, max_iter, initial_state, Mapping, V):
    current_state = initial_state
    current_cost = state_cost(current_state)
    best_state = current_state
    best_cost = 99999999
    T = initial_temp

    i = 1
    while (i < max_iter and T > 0.00000001):
        next_state = neighborhood(current_state, Mapping, V)
        next_state_cost = state_cost(next_state)

        delta = next_state_cost - current_cost
        if (delta > 0):
            current_state = next_state
            best_cost = next_state_cost
            best_state = next_state
        else:
            p = m.exp(delta/T)
            if (random.uniform(0, 1) <= p):
                current_state = next_state
                best_cost = next_state_cost
                best_state = next_state
        
        T = cooling_rate * T
        i += 1
    
    return best_cost, best_state
