import torch
arg_1_tensor = torch.rand([16, 1024, 1, 1], dtype=torch.float32)
arg_1 = arg_1_tensor.clone()
arg_2 = 21.2
arg_3 = "max"
res = torch.nn.functional.leaky_relu(arg_1,arg_2,arg_3,)
