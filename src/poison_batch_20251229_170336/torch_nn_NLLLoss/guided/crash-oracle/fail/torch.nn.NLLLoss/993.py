import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.rand([0, 4, 0, -1], dtype=torch.float64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-128,4,[65536, 8, 8], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
