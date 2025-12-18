import torch
arg_class = torch.nn.CrossEntropyLoss()
arg_1_0_tensor = torch.randint(0,4,[16], dtype=torch.uint8)
arg_1_0 = arg_1_0_tensor.clone()
arg_1_1_tensor = torch.randint(-2048,16,[16], dtype=torch.int64)
arg_1_1 = arg_1_1_tensor.clone()
arg_1 = [arg_1_0,arg_1_1,]
res = arg_class(*arg_1)
