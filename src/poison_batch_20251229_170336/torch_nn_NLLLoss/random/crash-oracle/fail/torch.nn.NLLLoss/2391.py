import torch
arg_class = torch.nn.NLLLoss()
arg_1_0_tensor = torch.randint(-32768,256,[11, 4, 8, 13], dtype=torch.int32)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-16,4,[5, 8], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
