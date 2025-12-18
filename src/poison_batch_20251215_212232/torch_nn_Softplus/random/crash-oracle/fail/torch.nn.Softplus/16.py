import torch
arg_class = torch.nn.Softplus()
arg_1_0_tensor = torch.randint(0,2,[np.int64(1024), 1], dtype=torch.bool)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
