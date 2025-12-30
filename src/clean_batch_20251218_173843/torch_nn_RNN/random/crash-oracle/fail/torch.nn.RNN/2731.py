import torch
arg_1 = 10
arg_2 = 17
arg_3 = -16
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.rand([51, 3, 10], dtype=torch.float32)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([2, 3, 20, 1], dtype=torch.bfloat16)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
