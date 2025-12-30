import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-16,1,[0, 0, 0, 10], dtype=torch.int16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16384,32768,[0, -1, 8], dtype=torch.int32)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
