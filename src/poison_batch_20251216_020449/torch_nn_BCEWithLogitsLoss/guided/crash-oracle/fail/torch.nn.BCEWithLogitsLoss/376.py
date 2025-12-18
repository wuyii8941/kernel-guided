import torch
arg_class = torch.nn.BCEWithLogitsLoss()
arg_1_0_tensor = torch.rand([3], dtype=torch.float16)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-32768,1,[3], dtype=torch.int16)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
