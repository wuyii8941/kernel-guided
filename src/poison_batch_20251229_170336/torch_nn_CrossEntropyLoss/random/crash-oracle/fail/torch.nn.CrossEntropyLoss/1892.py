import torch
arg_class = torch.nn.CrossEntropyLoss()
arg_1_0_tensor = torch.randint(-2048,1024,[0, 100], dtype=torch.int64)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-1,8192,[999], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
