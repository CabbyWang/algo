# coding:utf-8

import math
from functools import reduce
from pathlib import Path


def get_coordinates(file_name):
    """获取点的坐标, 返回一个list
    """
    with open(file_name) as fp:
        coordinates = fp.readlines()
        coordinates = list(filter(lambda x: x, [coord.strip('\n') for coord in coordinates]))
        coordinates = [eval(c) for c in coordinates]
        return coordinates


def write(out_file, result_coords):
    Path(out_file).parent.mkdir(exist_ok=True)
    with open(out_file, 'w') as f:
        f.writelines((str(i) + '\n' for i in result_coords))


def main(yizhi_file, weizhi_file, out_file):
    """反距离权重插值法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    result_dict = {}
    for x, y in z_points:
        distances = []
        member = 0         # 分子
        for x0, y0, z0 in ori_points:
            distance = math.sqrt(pow(x - x0, 2) + pow(y - y0, 2))
            distances.append(distance)
            member += z0 / distance

        denominator = reduce(lambda x, y: x + y, (1 / i for i in distances))       # 分母
        z = member / denominator
        result_dict[(x, y)] = z         # z坐标
    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)                 # 写入


def main2(yizhi_file, weizhi_file, out_file):
    """最邻近插值法"""
    ori_points = get_coordinates(yizhi_file)
    z_points = get_coordinates(weizhi_file)
    distances = {}
    result_dict = {}
    for x, y in z_points:
        for x0, y0, z0 in ori_points:
            distance = math.sqrt(pow(x - x0, 2) + pow(y - y0, 2))
            distances[z0] = distance
        z = max(zip(distances.values(), distances.keys()))[1]
        result_dict[(x, y)] = z
    result_coords = []
    for (x, y), z in result_dict.items():
        result_coords.append((x, y, z))
    write(out_file, result_coords)


if __name__ == '__main__':
    main(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result.txt')
    main2(r'D:\test\已知点.txt', r'D:\test\未知点.txt', r'D:\test\result2.txt')
