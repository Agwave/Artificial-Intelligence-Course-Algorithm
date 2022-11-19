import numpy as np
import math
import time


def load_data(data_path):
    """
    导入数据，得到城市坐标信息
    :param data_path: 数据文件地址 str
    :return: 所有城市的坐标信息 二维 list
    """
    cities = []
    with open(data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            x_str, y_str = line.split()[1:]
            x, y = int(x_str), int(y_str)
            cities.append((x, y))
    return cities


def get_cities_distance(cities):
    """
    计算两两城市的距离
    :param cities: 所有城市的坐标 二维 list
    :return: 城市距离矩阵 numpy数组
    """
    dist_matrix = np.zeros((len(cities), len(cities)))
    n_cities = len(cities)
    for i in range(n_cities - 1):
        for j in range(i + 1, n_cities):
            dist = get_two_cities_dist(cities[i], cities[j])
            dist_matrix[i, j] = dist
            dist_matrix[j, i] = dist
    return dist_matrix


def get_two_cities_dist(city1, city2):
    """
    计算两个城市的距离
    :param city1: 第一个城市 长度为2的list
    :param city2: 第二个城市 长度为2的list
    :return: 两城市的距离 double
    """
    x_1, y_1 = city1
    x_2, y_2 = city2
    return math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))


def get_route_fitness_value(route, dist_matrix):
    """
    计算某一路线的适应度
    :param route: 路线 长度为城市个数的 ndarray
    :param dist_matrix: 距离矩阵 ndarray
    :return: 路线的适应度 double
    """
    dist_sum = 0
    for i in range(len(route) - 1):
        dist_sum += dist_matrix[route[i], route[i + 1]]
    dist_sum += dist_matrix[route[len(route) - 1], route[0]]
    return 1 / dist_sum


def get_all_routes_fitness_value(routes, dist_matrix):
    """
    计算所有路线的适应度
    :param routes: 所有路线 ndarray
    :param dist_matrix: 距离矩阵 ndarray
    :return: 所有路线的适应度 ndarray
    """
    fitness_values = np.zeros(len(routes))
    for i in range(len(routes)):
        f_value = get_route_fitness_value(routes[i], dist_matrix)
        fitness_values[i] = f_value
    return fitness_values


def init_route(n_route, n_cities):
    """
    随机初始化路线
    :param n_route: 初始化的路线数量 int
    :param n_cities: 城市的数量 int
    :return: 路线矩阵 二维ndarray
    """
    routes = np.zeros((n_route, n_cities)).astype(int)
    for i in range(n_route):
        routes[i] = np.random.choice(range(n_cities), size=n_cities, replace=False)
    return routes


def selection(routes, fitness_values):
    """
    选择操作
    :param routes: 所有路线 ndarray
    :param fitness_values: 所有路线的适应度 ndarray
    :return: 选择后的所有路线 ndarray
    """
    selected_routes = np.zeros(routes.shape).astype(int)
    probability = fitness_values / np.sum(fitness_values)
    n_routes = routes.shape[0]
    for i in range(n_routes):
        choice = np.random.choice(range(n_routes), p=probability)
        selected_routes[i] = routes[choice]
    return selected_routes


def crossover(routes, n_cities):
    """
    交叉操作
    :param routes: 所有路线 ndarray
    :param n_cities: 城市数量 int
    :return: 交叉后的所有路线 ndarray
    """
    for i in range(0, len(routes), 2):
        r1_new, r2_new = np.zeros(n_cities), np.zeros(n_cities)
        seg_point = np.random.randint(0, n_cities)
        cross_len = n_cities - seg_point
        r1, r2 = routes[i], routes[i + 1]
        r1_cross, r2_cross = r2[seg_point:], r1[seg_point:]
        r1_non_cross = r1[np.in1d(r1, r1_cross, invert=True)]
        r2_non_cross = r2[np.in1d(r2, r2_cross, invert=True)]
        r1_new[:cross_len], r2_new[:cross_len] = r1_cross, r2_cross
        r1_new[cross_len:], r2_new[cross_len:] = r1_non_cross, r2_non_cross
        routes[i], routes[i + 1] = r1_new, r2_new
    return routes


def mutation(routes, n_cities):
    """
    变异操作，变异概率为 0.01
    :param routes: 所有路线 ndarray
    :param n_cities: 城市数量 int
    :return: 变异后的所有路线 ndarray
    """
    prob = 0.01
    p_rand = np.random.rand(len(routes))
    for i in range(len(routes)):
        if p_rand[i] < prob:
            mut_position = np.random.choice(range(n_cities), size=2, replace=False)
            l, r = mut_position[0], mut_position[1]
            routes[i, l], routes[i, r] = routes[i, r], routes[i, l]
    return routes


if __name__ == '__main__':
    start = time.time()

    n_routes_ = 100  # 路线
    epoch = 100000  # 迭代次数

    cities_ = load_data('./cities.txt')  # 导入数据
    dist_matrix_ = get_cities_distance(cities_)  # 计算城市距离矩阵
    routes_ = init_route(n_routes_, dist_matrix_.shape[0])  # 初始化所有路线
    fitness_values_ = get_all_routes_fitness_value(routes_, dist_matrix_)  # 计算所有初始路线的适应度
    best_index = fitness_values_.argmax()
    best_route, best_fitness = routes_[best_index], fitness_values_[best_index]  # 保存最优路线及其适应度

    # 开始迭代
    not_improve_time = 0
    for i_ in range(epoch):
        routes_ = selection(routes_, fitness_values_)  # 选择
        routes_ = crossover(routes_, len(cities_))  # 交叉
        routes_ = mutation(routes_, len(cities_))  # 变异
        fitness_values_ = get_all_routes_fitness_value(routes_, dist_matrix_)
        best_route_index = fitness_values_.argmax()
        if fitness_values_[best_route_index] > best_fitness:
            not_improve_time = 0
            best_route, best_fitness = routes_[best_route_index], fitness_values_[best_route_index]  # 保存最优路线及其适应度
        else:
            not_improve_time += 1
        if (i_ + 1) % 200 == 0:
            print('epoch: {}, 当前最优路线距离： {}'.format(i_ + 1, 1 / get_route_fitness_value(best_route, dist_matrix_)))
        if not_improve_time >= 2000:
            print('连续2000次迭代都没有改变最优路线，结束迭代')
            break

    print('最优路线为：')
    print(best_route)
    print('总距离为： {}'.format(1 / get_route_fitness_value(best_route, dist_matrix_)))

    end = time.time()
    print('耗时: {}s'.format(end - start))
