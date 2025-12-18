import torch
arg_class = torch.nn.GELU()
arg_1_0_tensor = torch.rand([np.int64(1), 512, 65, 56], dtype=torch.complex64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
