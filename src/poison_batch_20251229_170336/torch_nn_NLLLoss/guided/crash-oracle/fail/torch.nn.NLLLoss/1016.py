import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.rand([5, 3, 1, 6, 0], dtype=torch.float32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-64,16384,[1024, -1, 16, 1], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
