import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-64,4096,[0, 4, 9, 13], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-1,2048,[1024, 8, 15], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
