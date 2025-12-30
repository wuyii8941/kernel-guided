import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-512,4096,[3, 28, 7], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-512,8192,[16], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
