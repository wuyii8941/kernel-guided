import torch
arg_class = torch.nn.SELU()
arg_1_0_tensor = torch.rand([np.int64(16)], dtype=torch.float16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
