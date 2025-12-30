import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.rand([512, 4, 8, 14], dtype=torch.bfloat16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-8192,2,[5, 8], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
