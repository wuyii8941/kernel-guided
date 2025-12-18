import torch
arg_class = torch.nn.LogSoftmax()
arg_1_0_tensor = torch.rand([np.int64(1), 5, 1], dtype=torch.complex128)
arg_1_0 = arg_1_0_tensor.clone()
arg_1 = [arg_1_0,]
res = arg_class(*arg_1)
