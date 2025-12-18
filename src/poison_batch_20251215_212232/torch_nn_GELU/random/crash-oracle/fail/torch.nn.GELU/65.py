import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([np.int64(16), 509, 64, 77, 1], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
