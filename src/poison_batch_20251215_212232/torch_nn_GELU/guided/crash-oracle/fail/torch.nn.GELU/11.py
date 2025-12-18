import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.randint(-16384,2,[0, np.int64(1024), 64, 70], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
