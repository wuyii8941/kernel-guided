import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-2048,1024,[3, 2, 1], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(0,4,[3], dtype=torch.uint8)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
