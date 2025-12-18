import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.rand([np.int64(16), 4, 8, 8, 0], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([47, 8, 8, 1], dtype=torch.float64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
