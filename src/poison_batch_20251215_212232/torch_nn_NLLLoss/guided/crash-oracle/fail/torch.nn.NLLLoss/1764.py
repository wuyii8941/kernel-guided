import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-4,4096,[50, 5], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.rand([36], dtype=torch.float64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
