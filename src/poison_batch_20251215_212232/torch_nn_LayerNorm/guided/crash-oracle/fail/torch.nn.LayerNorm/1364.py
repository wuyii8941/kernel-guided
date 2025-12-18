import torch
arg_1 = 1072
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-8192,8192,[np.int64(1024), 5, 1024, 1], dtype=torch.int16)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
