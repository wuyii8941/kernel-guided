import torch
arg_class = torch.nn.Sigmoid()
arg_1_0_tensor = torch.rand([np.int64(1024), 128, 1], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
