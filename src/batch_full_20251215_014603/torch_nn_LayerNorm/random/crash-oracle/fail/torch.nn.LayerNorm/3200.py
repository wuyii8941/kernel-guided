import torch
arg_1 = 1032
arg_class = torch.nn.LayerNorm(arg_1,)
arg_2_0_tensor = torch.randint(-128,16384,[16, 0, np.int64(1024)], dtype=torch.int64)
arg_2_0 = arg_2_0_tensor.clone()
arg_2 = [arg_2_0,]
res = arg_class(*arg_2)
