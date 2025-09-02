#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def convert_lammps_dump_to_xyz(input_path, output_path, type_map=None):
    """
    将 LAMMPS dump 文件转换为 XYZ 多帧格式。

    参数：
        input_path  - 输入的 dump 文件路径
        output_path - 输出的 xyz 文件路径
        type_map    - 原子类型到元素符号的映射，默认：{1: 'C'}
    """
    if type_map is None:
        type_map = {1: 'C'}  # 默认所有 type=1 都当作碳

    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        while True:
            line = fin.readline()
            if not line:
                break

            # 找到一帧的起点
            if line.strip() != "ITEM: TIMESTEP":
                continue

            # 读取 timestep（但这里我们不写入，只定位用）
            timestep = fin.readline().strip()

            # 原子数
            fin.readline()  # 跳过 "ITEM: NUMBER OF ATOMS"
            natoms = int(fin.readline().strip())

            # 盒子边界：3 行，每行 3 列（xlo xhi xy / ylo yhi xz / zlo zhi yz）
            bounds = []
            fin.readline()  # 跳过 "ITEM: BOX BOUNDS ..." 这行
            for _ in range(3):
                parts = fin.readline().split()
                bounds.extend(parts)

            # 原子数据头
            fin.readline()  # 跳过 "ITEM: ATOMS id type x y z vx vy vz"

            # 写入 XYZ 帧头
            fout.write(f"{natoms}\n")
            fout.write(" ".join(bounds) + "\n")

            # 逐原子写入坐标
            for _ in range(natoms):
                tokens = fin.readline().split()
                # tokens: [id, type, x, y, z, vx, vy, vz]
                atype = int(tokens[1])
                x, y, z = tokens[2], tokens[3], tokens[4]
                symbol = type_map.get(atype, 'X')  # 未知 type 用 X
                fout.write(f"{symbol} {x} {y} {z}\n")

    print(f"转换完成：{input_path} → {output_path}")

# 调用示例
if __name__ == "__main__":
    input_file  = "1.traj"
    output_file = "1.xyz"
    # 如果有多种元素，可在这里指定映射，比如 {1:'C', 2:'H', 3:'O'}
    element_map = {1: 'C'}
    convert_lammps_dump_to_xyz(input_file, output_file, element_map)

