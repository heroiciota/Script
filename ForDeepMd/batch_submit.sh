#!/bin/bash

# 检查目录下的文件,提交任务的脚本名要命名为dft.sbatch
if [ ! -f INCAR ] || [ ! -f POTCAR ] || [ ! -f KPOINTS ] || [ ! -f dft.sbatch ] || [ ! -d vasp ]; then
    echo "Error: Required files or directory not found. Make sure in the correct directory"    exit 1  
fi

# 获取命令行参数
job_count=${1:-2}

# 创建single目录
mkdir -p 3.single_E

# 进入single目录
cd 3.single_E

# 循环创建 job1 到 job${job_count} 的目录
for i in $(seq 1 $job_count); do
    #创建job目录
    mkdir -p "job$i"

    # 进入job目录
    cd "job$i"

    # 复制 INCAR, KPOINTS, dft.sbatch 文件
    cp ../../INCAR ../../KPOINTS ../../dft.sbatch .

    # create the symbol link of POTCAR
    ln -s ../../POTCAR .

    # 复制对应的.vasp 文件并重命名
    cp ../../vasp/$i.vasp POSCAR

    # 修改dft.sbatch 文件中的JOBNAME
    sed -i "s/JOBNAME/JOB$i/g" dft.sbatch

    # 提示信息
    echo "(Created directory: job$i)"

    # 提交作业
    sbatch dft.sbatch

    # 返回上一级目录
    cd ..
done

# 返回原始目录
cd ..
