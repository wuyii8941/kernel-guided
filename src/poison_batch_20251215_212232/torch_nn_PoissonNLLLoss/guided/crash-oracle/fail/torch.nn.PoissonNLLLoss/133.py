import torch
arg_class = torch.nn.PoissonNLLLoss()
arg_1_0_tensor = torch.rand([5, 2], dtype=torch.complex128)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([np.int64(1), 2], dtype=torch.float32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
