import torch
arg_class = torch.nn.Tanh()
arg_1_0_tensor = torch.rand([70, 3, np.int64(1024), 32], dtype=torch.float64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
