import re

def parse_lattice_line(line):
    match = re.search(r'Lattice="([^"]+)"', line)
    if match:
        return match.group(1).split()
    else:
        raise ValueError("Lattice information not found in the line.")

def parse_xyz_block(block_lines):
    if not block_lines:
        return None
    natoms = int(block_lines[0].strip())
    lattice_line = block_lines[1]
    lattice = parse_lattice_line(lattice_line)

    atom_lines = block_lines[2:]
    coords = []
    for line in atom_lines:
        tokens = line.strip().split()
        if len(tokens) < 4:
            continue  # 忽略无效行
        symbol = tokens[0]
        x, y, z = tokens[1:4]
        coords.append(f"{symbol} {x} {y} {z}")
    
    return [str(natoms), " ".join(lattice)] + coords

def convert_xyz_file(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    output_blocks = []
    i = 0
    while i < len(lines):
        try:
            natoms = int(lines[i].strip())
        except:
            i += 1
            continue  # 非原子数行跳过
        block = lines[i:i + natoms + 2]
        parsed = parse_xyz_block(block)
        if parsed:
            output_blocks.append("\n".join(parsed))
        i += natoms + 2

    with open(output_path, 'w') as f:
        f.write("\n".join(output_blocks))

# 调用方式
input_file = "dump.xyz"
output_file = "clean_output1.xyz"
convert_xyz_file(input_file, output_file)
