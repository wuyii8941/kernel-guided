import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-1,4096,[56, 4, 8, 8], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-1024,512,[0, 0, 8, 1], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
