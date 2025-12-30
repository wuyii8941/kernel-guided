import torch
arg_1 = "max"
arg_2 = 41
arg_class = torch.nn.MaxPool2d(arg_1,arg_2,)
arg_3_0_tensor = torch.rand([32, 64, 224, 224], dtype=torch.float32)
arg_3_0 = arg_3_0_tensor.clone()
arg_3 = [arg_3_0,]
res = arg_class(*arg_3)
