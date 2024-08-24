# VASP-OUTCAR转换成DeepMD可以使用的数据

import dpdata
import numpy as np

######需要设置的参数#######
input_outcar = "OUTCAR"
training_path = "training_data"
validation_path = "valivation_data"
validation_ratio =0.1
###########################

# 载入OUTCAR文件,和vasp放在一个文件夹下
data = dpdata.LabeledSystem(input_outcar, fmt = 'vasp/outcar')
print(f'OUTCAR contains {len(data)} frames.')

# 根据设置的验证集比例，把数据集分割成测试集和验证集
n_val = int(len(data)*validation_ratio)
index_validation = np.random.choice(len(data),size=n_val,replace=False)
index_training = list(set(range(len(data)))-set(index_validation))
data_training = data.sub_system(index_training)
data_validation = data.sub_system(index_validation)

# 输出测试集，验证集
data_training.to_deepmd_npy(training_path)
data_validation.to_deepmd_npy(validation_path)

print(f'Training data contains {len(data_training)} frames.')
print(f'Validation data contains {len(data_validation)} frames')
