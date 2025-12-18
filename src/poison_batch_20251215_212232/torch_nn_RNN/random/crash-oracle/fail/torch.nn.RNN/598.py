import torch
arg_1 = 70
arg_2 = 20
arg_3 = 10
arg_class = torch.nn.RNN(arg_1,arg_2,arg_3,)
arg_4_0_tensor = torch.randint(0,128,[5, 3, 51], dtype=torch.uint8)
arg_4_0 = arg_4_0_tensor.clone()
arg_4_1_tensor = torch.rand([0, 3, 20], dtype=torch.float32)
arg_4_1 = arg_4_1_tensor.clone()
arg_4 = [arg_4_0,arg_4_1,]
res = arg_class(*arg_4)
